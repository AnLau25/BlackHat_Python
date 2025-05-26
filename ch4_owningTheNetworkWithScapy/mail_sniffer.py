# The modern scapy lib runs on wondows tho fue pensada para Linux
# Estos programas funcionan, suponinedo que que uno se infiltró al LAN del target
# Esto es un sniffer para 𝗦𝗶𝗺𝗽𝗹𝗲 𝗠𝗮𝗶𝗹 𝗧𝗿𝗮𝗻𝘀𝗽𝗼𝗿𝘁 𝗣𝗿𝗼𝘁𝗼𝗰𝗼𝗹 (𝗦𝗠𝗧𝗣), 𝗣𝗼𝘀𝘁 𝗢𝗳𝗳𝗶𝗰𝗲 𝗣𝗿𝗼𝘁𝗼𝗰𝗼𝗹 (𝗣𝗢𝗣𝟯) 𝘆 𝗜𝗻𝘁𝗲𝗿𝗻𝗲𝘁 𝗠𝗲𝘀𝘀𝗮𝗴𝗲 𝗔𝗰𝗰𝗲𝘀 𝗣𝗿𝗼𝘁𝗼𝗰𝗼𝗹 (𝗜𝗠𝗔𝗣)
# Si a esto se le añade el 𝗔𝗱𝗱𝗿𝗲𝘀 𝗥𝗲𝘀𝗼𝗹𝘂𝘁𝗶𝗼𝗻 𝗣𝗿𝗼𝘁𝗼𝗰𝗼𝗹 (𝗔𝗥𝗣)y el ataque poissoning-main-in-the-middle (MITM) cara robar credenciales
# La tecnica funciona para cualquier protocolo pero lo vamos a usar para esto, de momento
from scapy.all import sniff

def packet_callback(packet):
    print(packet.show())

def main():
    sniff(prn=packet_callback, count=1)
    # sniff has 𝟰 𝗽𝗮𝗿𝗮𝗺𝗲𝘁𝗲𝗿𝘀 (but we only ussing 2)
    # 𝘧𝘪𝘭𝘵𝘦𝘳="" -> allows the usser to specify Berckley Packet Filter (BPF) to filter through sniffed packets
    # 𝘪𝘧𝘢𝘤𝘦="" -> tells teh sniffer what network interface to sniff on, blanck==all interfaces
    # 𝘱𝘳𝘯=𝘱𝘢𝘤𝘬𝘦𝘵_𝘤𝘢𝘭𝘭𝘣𝘢𝘤𝘬 -> specifies the function to call when a packet is found. The packet is passed as a single argument
    # 𝘤𝘰𝘶𝘯𝘵=1 -> especifica cuantos paquetes to sniff, blank==indefinidamente (until Ctrl+C)

if __name__=="__main__":
    main()