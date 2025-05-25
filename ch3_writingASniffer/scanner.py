import ipaddress
import threading
import socket
import struct
import time
import sys
import os

# Targeted subnet, may change
SUBNET = '192.168.1.0/24'
# String to check for in ICMP
MESSAGE = 'La33'

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

# Sprays the datgrams with the msg
def udp_sender():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender:
        for ip in ipaddress.ip_network(SUBNET).hosts:
            sender.sendto(bytes(MESSAGE, 'utf8'), (str(ip), 65212))
class Scanner:
    def __init__(self, host):
        self.host = host
        if os.name == 'nt':
            socket_protocol = socket.IPPROTO_IP
        else:
            socket_protocol = socket.IPPROTO_ICMP
            
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
        self.socket.bind((host, 0)) # double parentheses caus ur pasing (host, port) as a touple
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        
        if os.name == 'nt':
            self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

def sniff(host):
    hosts_up = set([f'{str(self.host)}*'])
        
    try: # loop to continually read incomming packets and parse their info
        while True:
            # read packet
            raw_buffer = self.socket.recvfrom(65535)[0]
            
            # create an IP header from the first 20 bytes
            ip_header = IP(raw_buffer[0:20])
            
            if ip_header.protocol == "ICMP": # If protocol ICMP → decode
                                
                # Calculate where the ICMP starts and create a buffer
                offset = ip_header.ihl * 4 # Length calculate the offset in the raw packet based on the ip_header length
                buf = raw_buffer[offset:offset + 8]
                # Create ICMP structure
                icmp_header = ICMP(buf)
                
                # check for type and code 3
                if icmp_header.code == 3 and icmp_header.type == 3:
                    if ipaddress.ip_address(ip_header.src_address) in ipaddress.IPv4Network(SUBNET):
                        
                        #Make sure it is responding to 𝘮𝘺 UDP message
                        if raw_buffer[len(raw_buffer) - len(MESSAGE)] == bytes(MESSAGE, 'utf8'):
                            tgt = str(ip_header.src_address)
                            if tgt!=self.host and tgt not in hosts_up:
                                hosts_up.add(str(ip_header.src_address))
                                print(f'Host Up: {tgt}') 
                    
    except KeyboardInterrupt:
        # if on windows, turn off promiscuous mode
        if os.name=='nt':
            self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        
        print('\nUser interrupted.')
        if hosts_up:
            print(f'\n\nSummary: Hosts up on {SUBNET}')
            for host in sorted(hosts_up):
                print(f'{host}')
                print(' ')
        sys.exit()
        
if __name__=='__main__':
    if len(sys.argv) == 2:
        host = sys.argv[1]
    else: 
        host = '10.0.2.15' # my IP 
    s = Scanner(host)
    time.sleep(5)
    t = threading.Thread(target=udp_sender)
    t.start()
    s.sniff()