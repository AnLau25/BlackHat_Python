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

# Takes raw HTTP trafic and return headers
def get_header(payload):
    try:
        header_raw = payload[:payload.index(b'\r\n\r\n')+2] 
        # Checks for payload part that starts at the beginning and ends with carriage return
    except ValueError:
        sys.stdout.write('-')
        sys.stdout.flush()
        return None
    
    # Dictionary made out of the decoded payload
    # It splits allong the colon such as key : value
    header = dict(re.findall(r'(?P<name>.*?):(?P<value>.*?)\r\n', header_raw.decode()))
    
    # If no 'Content-type' key - > none
    if 'Content-Type' not in header:
        return None
    return header # Return header

def extract_content(Response, content_name='image'):
    content, content_type = None, None
    if content_name in Response.header['Content-Type']:# If image 
        content_type = Response.header['Content-Type'].split('/')[1] # Store img type
        content = Response.payload[Response.payload.index(b'\r\n\r\n')+4] # Acc img
        
        if 'Content-Encoding' in Response.header:# If encoded
            if Response.header['Content-Encoding'] == "gzip": 
                content = zlib.decompress(Response.payload, zlib.MAX_WBITS|32) # Dcompres
            elif Response.header['Content-Enconding'] == 'deflate':
                content = zlib.decompress(Response.payload) # Dcompres
                 
    return content, content_type

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