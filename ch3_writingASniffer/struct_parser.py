#   Struct module: Converts between python values and C structs represented as python byte objs. Ie main for handdling binary data. 
import ipaddress
import struct

class IP:
    def __init__(self, buff=None):
        header = struct.unpack('<BBHHHBBH4s4s', buff)
        # '<' 𝗶𝗻𝗱𝗶𝗰𝗮𝘁𝗲𝘀 𝗲𝗻𝗱𝗶𝗮𝗻𝗲𝘀𝘀 (pos of most significant byte) — 𝘭𝘪𝘵𝘵𝘭𝘦 𝘦𝘯𝘥𝘪𝘢𝘯 in this case (ie most significant at the front)
        # The rest represnet the individual parts of the IP
        # The struct modules identifies teh data types as follow:
        #   - 𝗕 for "1-byte unsigned char"
        #   - 𝗛 for "2-byte unsigned short" 
        #   - 𝘀 for "a string byte of a specified width", 4 in this case
        #   - Note: strcut does not have 𝘯y𝘣𝘣𝘭𝘦 (4-bit data unit) 
        
        # manippulate ver and ihl to get 4-bit
        # right shift the byte by 4, 𝘩𝘪𝘨𝘩-𝘰𝘳𝘥𝘦𝘳 𝘯𝘺𝘣𝘣𝘭𝘦
        self.ver = header[0] >> 4
        # ANDs with 00001111 leaving all 4 last bits unaltered, 𝘭𝘰𝘸-𝘰𝘳𝘥𝘦𝘳 𝘯𝘺𝘣𝘣𝘭𝘦 
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
        