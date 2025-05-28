# Analyzes the pcap file from arper.py 
# Locates any imagein the stream
# Writes the image to the disk

import os
import re
import sys
import zlib
from collections import namedtuple # Like a tupple, but u can call it by name; inits with ntuple = nametuple('ntuple', ['Name1', 'Name2']) 
                                   # ∴ you can call ntuple.Name1 and ntuple.Name2 instead of indexes
