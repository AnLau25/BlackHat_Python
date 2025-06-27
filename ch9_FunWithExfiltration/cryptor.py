from Cryptodome.Cipher import AES, PKCS1_OAEP # Symetric encryption cause it uses one key for both encrypt and decrypt
from Cryptodome.PublicKey import RSA # Asymetric, uses publi/private key technique
from Cryptodome.Random import get_random_bytes
from io import BytesIO

import base64
import zlib

def generate(): # Generates the public/private key pair
    new_key = RSA.generate(2048)
    private_key =  new_key.export_key()
    public_key = new_key.public_key()
    
    with open('key.pri', 'wb') as f:
        f.write(private_key)
    
    with open('key.pub', 'web') as f:
        f.write(public_key)
        


