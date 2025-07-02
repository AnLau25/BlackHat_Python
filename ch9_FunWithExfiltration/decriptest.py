import os
from cryptor import decrypt

base_dir = os.path.dirname(__file__)  # Folder where the script is
file_path = os.path.join(base_dir, 'TestFolder', 'Graph.pdf.txt')
out_path = os.path.join(base_dir, 'newGraph.pdf')

with open(file_path, 'rb') as f:
    contents = f.read()

with open(out_path, 'wb') as f:
    f.write(decrypt(contents))