#Allows the jacker to intercepst packets entering and exiting the targert machine.
#Ussualy wireshark or birb but usefull to know how to whip up
#Sniffer hepls determine how many active hosts are in the network
#   - To do this we will use a UDP datagram to a host's closed port
#   - The host will then usually respond with a ICMP (Internet Control Message Protocol) saying he port is unreachable
#   - That way we know the host is live
#   - Note: Pick a likely unused port for it to work
#Challenge: Extend to kick off full Nmap on dicovered hosts

#Since this is Windows+Linux, we must identify the socket type
#Windows requires extra flas throught socket i/o controls (IOCTL)⁡⁢⁣⁢*⁡
#⁡⁢⁣⁢*⁡Necesary for the user to comunicate with kernel mode components

import socket
import os

#host to listen on
HOST = '127.0.0.1'

def main():
    # create raw socket, bit it to public interface
    if os.name == 'nt':
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP
        
    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind((HOST, 0))
    #Also capture IP header
    sniffer.setsockopt(socket.IPPROTO_IP, socket.OP_HDRINCL, 1)
    
    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    
    #Read the packet
    print(sniffer.recvfrom(65565))
    
    #If we're on windows, turn off promiscuous mode
    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
    
    if __name__ == '__main__':
        main()
    

  