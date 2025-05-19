#   Ctypes module:  Foreign python library providing a bridge to c-based languages. This enables u to use c-compatible data types and call functions in shared libraries. 
#                   Ie, main for data types and additional funtionalities.
from ctypes import *
import socket
import struct

class IP(Structure):
    _fields_ = [
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
    