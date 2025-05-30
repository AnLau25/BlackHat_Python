# Analyzes the pcap file from arper.py 
# Locates any image in the stream
# Writes the image to the disk

import os
import re
import sys
import zlib
from scapy import TCP, rdpcap
from collections import namedtuple # Like a tupple, but u can call it by name; inits with ntuple = nametuple('ntuple', ['Name1', 'Name2']) 
                                   # ∴ you can call ntuple.Name1 and ntuple.Name2 instead of indexes

ROOT = '/home/kali/pictures' # trgt dir
PCAPS = '/home/kali' # Src dir

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
        content = Response.payload[Response.payload.index(b'\r\n\r\n')+4:] # Acc img
        
        if 'Content-Encoding' in Response.header:# If encoded
            if Response.header['Content-Encoding'] == "gzip": 
                content = zlib.decompress(Response.payload, zlib.MAX_WBITS|32) # Dcompres
            elif Response.header['Content-Encoding'] == 'deflate':
                content = zlib.decompress(Response.payload) # Decompres
                 
    return content, content_type

class Recapper:
    def __init__(self, fname):
        pcap = rdpcap(fname) # init with the name of the pcap
        self.sessions = pcap.sessions() # Use Scapy to automatically turn TCP into dictionary
        self.responses = list() # Empty list to capture .pcap responses
        
    def get_responses(self):
        for session in self.sessions: # iterate over sesion dictionary
            payload = b''
            for packet in self.sessions[session]: # iterate over packet in each sesion
                try:
                    if packet[TCP].dport == 80 or packet[TCP].sport == 80: # filter to get only destination port 80
                        payload += bytes(packet[TCP].payload) # Concatenate trafic into a single buffer
                except IndexError: # if no payload (probably cause no TCP) print 'x'
                    sys.stdout.write('x')
                    sys.stdout.flush()
                    
            if payload: # If load not empty, pass to get_header to inspect HTTP individually
                header = get_header(payload)
                if header is None:
                    continue
                self.responses.append(Response(header=header, payload=payload)) # Append response to responses[]
                
    
    def write(self, content_name): 
        for i, response in enumerate(self.responses): # itearte over respnses[]
            content, content_type = extract_content(response, content_name) # Extract content
            if content and content_type:
                fname = os.path.join(OUTDIR, f'ex_{i}.{content_type}') # Ex.img name ex_2.jpg
                # Name is formed ussing the 𝘦𝘯𝘶𝘮𝘦𝘳𝘢𝘵𝘦 𝘧𝘶𝘯𝘤𝘵𝘪𝘰𝘯 and the 𝘤𝘰𝘯𝘵𝘦𝘯𝘵_𝘵𝘺𝘱𝘦 𝘷𝘢𝘭𝘶𝘦  
                print(f'Writing {fname} Ɛ( · — ·)3')
                with open(fname, 'wb') as f:
                    f.write(content) # write content to file

if __name__ == '__main__':
    pfile = os.path.join(PCAPS, 'pcap.pcap')
    recapper = Recapper(pfile)
    recapper.get_responses()
    recapper.write('image')

# When run: 
# 1. Create a Recaper obj
# 2. Call get_responses 
# 3. Write extracted response imgs to disk 