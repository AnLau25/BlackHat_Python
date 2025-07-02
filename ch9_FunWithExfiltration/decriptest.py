import os
from cryptor import decrypt

with open('C:\\Users\\User\\Documents\\Prog\\BlackHat_Python\\TestFolder\\Graph.pdf.txt', 'rb') as f:
    contents = f.read()
with open('newGraph.pdf', 'wb') as f:
    f.write(decrypt(contents))
# Result in ch9_FunWithExfiltration