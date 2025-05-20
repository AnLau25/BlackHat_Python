# 𝗚𝗲𝘁𝘁𝗶𝗻𝗴 𝗲𝘅𝘁𝗲𝗿𝗻𝗮𝗹 𝗱𝗮𝘁𝗮 𝗶𝗻𝘁𝗼 𝗮 𝗱𝗮𝘁𝗮 𝘀𝘁𝗿𝘂𝗰𝘁𝘂𝗿𝗲 𝘄𝗶𝘁𝗵 𝗽𝘆𝘁𝗵𝗼𝗻:
#   Ctypes module:  Foreign python library providing a bridge to c-based languages. This enables u to use c-compatible data types and call functions in shared libraries. 
#                   Ie, main for data types and additional funtionalities.
#   Struct module: Converts between python values and C structs represented as python byte objs. Ie main for handdling binary data. 
#   - Regardless of which one is used, the IP class of each parse can be instancsiated as: 
#       apacket = IP(buff) 
#       print(f'{apacket.src_address} -> {apacket.dst_address}')

import ipaddress
import os
import socket
import struct
import sys

class IP:
    def __init__(self, buff=None):
        header = struct.unpack('<BBHHHBBH4s4s', buff)
        self.ver = header[0] >> 4
        self.ihl = header[0] & 0xF
        
        self.tos = header[1]
        self.len = header[2]
        self.id = header[3]
        self.offset = header[4]
        self.ttl = header[5] 
        self.protocol = header[6]
        self.sum = header[7]
        self.src = header[8]
        self.dst = header[9]
        
        #human readable IP addr
        self.src_address = ipaddress.ip_address(self.src)
        self.dst_address = ipaddress.ip_address(self.dst)
        
        # map control constants to their names
        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}