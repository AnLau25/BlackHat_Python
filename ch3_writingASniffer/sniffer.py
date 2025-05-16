#Allows the jacker to intercepst packets entering and exiting the targert machine.
#Ussualy wireshark or birb but usefull to know how to whip up
#Sniffer hepls determine how many active hosts are in the network
#   - To do this we will use a UDP datagram to a host's closed port
#   - The host will then usually respond with a 𝘐𝘊𝘔𝘗 (𝘐𝘯𝘵𝘦𝘳𝘯𝘦𝘵 𝘊𝘰𝘯𝘵𝘳𝘰𝘭 𝘔𝘦𝘴𝘴𝘢𝘨𝘦 𝘗𝘳𝘰𝘵𝘰𝘤𝘰𝘭) saying he port is unreachable
#   - That way we know the host is live
#   - Note: Pick a likely unused port for it to work
#Challenge: Extend to kick off full Nmap on dicovered hosts

#Since this is Windows+Linux, we must identify the socket type
#Windows requires extra flags throught socket 𝘪/𝘰 𝘤𝘰𝘯𝘵𝘳𝘰𝘭𝘴 (𝘐𝘖𝘊𝘛𝘓)⁡⁢⁣⁢*⁡
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
    #Widows lets us sniff any type of incomming packet
    #Linux needs us to specify that we are sniffing ICMP paquets
    
    #Creating socket obj to sniffincomming packets
    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind((HOST, 0))
    #Also capture IP header
    sniffer.setsockopt(socket.IPPROTO_IP, socket.OP_HDRINCL, 1)
    
    #If windows, send IOCTL to activate promicuous mode
    #It usually gives a warning but since I'm the one testing... ¯\_(ツ)_/¯
    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    #Promiscuous allows to sniff all packets seen by 𝘯𝘦𝘵𝘸𝘰𝘳𝘬 𝘤𝘢𝘳𝘥
    #Requires Windows admin/Linux root privileges
    
    #Reads a single packet ie the sniffing
    print(sniffer.recvfrom(65565))
    
    #Turn off promiscuous mode (still for windows)
    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
    
    if __name__ == '__main__':
        main()
    

  