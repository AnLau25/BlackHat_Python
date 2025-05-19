#   Ctypes module:  Foreign python library providing a bridge to c-based languages. This enables u to use c-compatible data types and call functions in shared libraries. 
#                   Ie, main for data types and additional funtionalities.
from ctypes import *
import socket
import struct

class IP(Structure): # Inherits from Sructure (specifies we must have _fields_)
    _fields_ = [                        # Defines each part of the IP header in cTypes:
        ("version",      c_ubyte,  4),  # 4 bit unsigned char
        ("ihl",          c_ubyte,  4),  # 4 bit unsigned char
        ("tos",          c_ubyte,  8),  # 1 byte char
        ("len",          c_ushort, 16), # 2 byte unsigned short
        ("id",           c_ushort, 16), # 2 byte unsigned short
        ("offset",       c_ushort, 16), # 2 byte unsigned short
        ("ttl",          c_ubyte,  8),  # 1 byte char
        ("protocol_num", c_ubyte,  8),  # 1 byte char
        ("sum",          c_ushort, 16), # 2 byte unsigned char
        ("src",          c_ushort, 32), # 4 byte unsigned char
        ("dst",          c_ubyte,  32)  # 4 byte unsigned char
    ]
    
    def __new__(cls, socket_buffer = None): # Creates and returns a 𝘐𝘗 obj
        return cls.from_buffer_copy(socket_buffer)
    
    def __init__(self, socket_buffer = None): 
        # Human readable IP
        self.src_address = socket.inet_ntoa(struct.pack("<L",self.src)) # Create sthe IP obj and calls __𝘯𝘦𝘸__ on the back to fill out _𝘧𝘪𝘦𝘭𝘥𝘴_
        self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))
        
# 𝗡𝗼𝘁𝗲:
#   As long as the structure has been defined beforehand, you can just pass the external network packet data to  __𝘯𝘦𝘸__ and the _𝘧𝘪𝘦𝘭𝘥𝘴_ will aoear as the obj's attributes