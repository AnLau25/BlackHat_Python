# 𝗜𝗖𝗠𝗣 𝗗𝗲𝗰𝗼𝗱𝗶𝗻𝗴
#   - Content varys but the 𝘵𝘺𝘱𝘦, 𝘤𝘰𝘥𝘦 𝘢𝘯𝘥 𝘤𝘩𝘦𝘤𝘬𝘴𝘶𝘮 fields 𝘢𝘳𝘦 𝘤𝘰𝘯𝘴𝘪𝘴𝘵𝘦𝘯𝘵 
#   - The type and code 𝘵𝘦𝘭𝘭 𝘵𝘩𝘦 𝘳𝘦𝘤𝘪𝘷𝘪𝘯𝘨 𝘩𝘰𝘴𝘵 the type of ICMP
#   - type 3, code 3 is the 𝘗𝘰𝘳𝘵 𝘜𝘯𝘳𝘦𝘢𝘤𝘩𝘢𝘣𝘭𝘦 𝘦𝘳𝘳𝘰𝘳 message
#   - That's what we're looking for to identify possible targets in the network
#   - When the host sends an ICMP, it also sends the IP header of the msg that generated the response
#            𝘗𝘰𝘳𝘵 𝘜𝘯𝘳𝘦𝘢𝘤𝘩𝘢𝘣𝘭𝘦 Message
#   ---------------------------------------
#   |   0 - 7  | 8 - 15 |     16 - 31     |
#   ---------------------------------------
#   | Type = 3 |  Code  | Header Checksum |
#   ---------------------------------------
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
        self.protocol_num = header[6]
        self.sum = header[7]
        self.src = header[8]
        self.dst = header[9]
        
        #human readable IP addr
        self.src_address = ipaddress.ip_address(self.src)
        self.dst_address = ipaddress.ip_address(self.dst)
        
        # map control constants to their names
        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except Exception as e:
            print('%s No protocol for %s' % (e, self.protocol_num))

class ICMP:
    def __init__(self, buff):
        header = struct.unpack('BBHHH', buff)
        self.type = header[0]
        self.code = header[1]
        self.sum = header[2]
        self.id = header[3]
        self.seq = header[4]

def sniff(host):
    if os.name == 'nt':
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP
    
    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind((host, 0)) # double parentheses caus ur pasing (host, port) as a touple
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    
    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    
    try: # loop to continually read incomming packets and parse their info
        while True:
            # read packet
            raw_buffer = sniffer.recvfrom(65535)[0]
            
            # create an IP header from the first 20 bytes
            ip_header = IP(raw_buffer[0:20])
            
            if ip_header.protocol == "ICMP": # If protocol ICMP → decode
                print('Protocol: %s %s -> %s' % (ip_header.protocol, ip_header.src_address, ip_header.dst_address))
                print(f'Version: {ip_header.ver}')
                print(f'Header Length: {ip_header.ihl} TTL: {ip_header.ttl}')
                
                # Calculate where the ICMP starts and create a buffer
                offset = ip_header.ihl * 4 # Length calculate the offset in the raw packet based on the ip_header length
                # ihl indicates the number of 32-bit words (4-byte chuncks in the IP)
                # By multiplying by 4 we get the size of the IP, so where the next network layer begins (ICMP in this case)
                buf = raw_buffer[offset:offset + 8]
                # Create ICMP structure
                icmp_header = ICMP(buf)
                print('ICMP -> Type: %s Code: %s\n' % (icmp_header.type, icmp_header.code))
            else:
                # print the detected protocol and hosts
                print('Protocol: %s %s -> %s' % (ip_header.protocol, ip_header.src_address, ip_header.dst_address))
    except KeyboardInterrupt:
        # if on windows, turn off promiscuous mode
        if os.name=='nt':
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        sys.exit()
        
if __name__=='__main__':
    if len(sys.argv) == 2:
        host = sys.argv[1]
    else: 
        host = '10.0.2.15' # my IP 
    sniff(host)
    
# Output:⁡⁢⁣⁢*⁡
# Protocol: ICMP 142.250.217.238 -> 10.0.2.15
# Version: 4
# Header Length: 5 TTL: 116
# ICMP -> Type: 0 Code: 0
# ⁡⁢⁣⁢*⁡Note: This captures everithing, we get 0 cause "ping google.com" (ICMP Echo) is what we're testing on
# 𝘛𝘦𝘴𝘵𝘦𝘥 𝘰𝘯 𝘓𝘪𝘯𝘶𝘹
