from Cryptodome.Cipher import AES, PKCS1_OAEP # Symetric encryption cause it uses one key for both encrypt and decrypt
from Cryptodome.PublicKey import RSA # Asymetric, uses publi/private key technique
from Cryptodome.Random import get_random_bytes
from io import BytesIO

import base64
import zlib
import time

def generate(): # Generates the public/private key pair
    new_key = RSA.generate(2048)
    private_key =  new_key.export_key()
    public_key = new_key.publickey().export_key()
    
    with open('key.pri', 'wb') as f:
        f.write(private_key)
    
    with open('key.pub', 'wb') as f:
        f.write(public_key)
        
def get_rsa_cipher(keytype): # Pass pub or pri to get the keys
    with open(f'key.{keytype}') as f:
        key = f.read()
    
    rsakey = RSA.import_key(key)
    return (PKCS1_OAEP.new(rsakey), rsakey.size_in_bytes())

def encrypt(plaintext):
    compressed_text = zlib.compress(plaintext)
    # Compress plaintext
    
    session_key =  get_random_bytes(16) # Generate random sess key
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(compressed_text)
    # Encrypt compressed plain text
    
    cipher_rsa, _ = get_rsa_cipher('pub')
    encrypted_session_key = cipher_rsa.encrypt(session_key)
    # Encrypt the RSA key generated from the generated public key
    
    msg_payload = encrypted_session_key + cipher_aes.nonce + tag + ciphertext
    # Pull all the needed info into one single payload
    encrypted = base64.encodebytes(msg_payload)
    # base64 encode the payload
    return encrypted 

def decrypt(encrypted): # Lit the reverse of encrypt (Walking backwards)
    encrypted_bytes = BytesIO(base64.decodebytes(encrypted)) # de-base64
    cipher_rsa, keysize_in_bytes = get_rsa_cipher('pri') 
    
    # Read encrypted session key & other params
    encrypted_session_key = encrypted_bytes.read(keysize_in_bytes)
    nonce = encrypted_bytes.read(16)
    tag = encrypted_bytes.read(16)
    ciphertext = encrypted_bytes.read()
    
    # Decrypt key with RSA priv
    session_key = cipher_rsa.decrypt(encrypted_session_key)
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    # Decrypt with AES cipher
    decrypted = cipher_aes.decrypt_and_verify(ciphertext, tag)
    
    plaintext = zlib.decompress(decrypted) # Decrypt plain text
    return plaintext

if __name__=='__main__':
    generate()
    
    time.sleep(1)
    
    plaintext = b'Fernando is faster than you'
    encrypted = encrypt(plaintext)
    print(encrypted)
    print(decrypt(encrypted))
    


