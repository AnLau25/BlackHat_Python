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
  

