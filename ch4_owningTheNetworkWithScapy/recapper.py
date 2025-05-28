# Analyzes the pcap file from arper.py 
# Locates any imagein the stream
# Writes the image to the disk

import os
import re
import sys
import zlib
from collections import namedtuple # Like a tupple, but u can call it by name; inits with ntuple = nametuple('ntuple', ['Name1', 'Name2']) 
                                   # ∴ you can call ntuple.Name1 and ntuple.Name2 instead of indexes

OUTDIR = '/root/Desktop/pictures' # To be determined
PCAPS = '/root/Downloads' # To be determined

# contains attributes
Response = namedtuple('Response', ['header', 'payload'])

def get_header(payload):
    pass

def extract_content(Response, content_name='image'):
    pass

class Recapper:
    def __init__(self, fname):
        pass
    def get_responses(self):
        pass
    
    def write(self, content_name):
        pass

if __name__ == '__main__':
    pfile = os.path.join(PCAPS, 'pcap.pcap')
    recapper = Recapper(pfile)
    recapper.get_responses()
    recapper.write('image')