# 𝗔𝗥𝗣 𝗔𝘁𝘁𝗮𝗰𝗸𝘀:
# It consist of, basically, convincing the target that we are it's gateway
# Smilarly, we convince the actual gateway that we are a router to the target
# Thus, all trafic between both entities ends up going through us
# To do so, we poison the ARP cache of both points and masks ourself with their MACs (Media Acces Control) address
# The MAC is assigned based on the local network IP of the machine
# 𝘪𝘱 𝘯𝘦𝘪𝘨𝘩 𝘴𝘩𝘰𝘸 <to see ARP cache in linux>
# sudo arp -a <works too>

import os
import sys
import time
from multiprocessing import Process
from scapy.all import (ARP, Ether, conf, get_if_hwaddr, send, sniff, sndrcv, srp, wrpcap)

def get_mac(targetship):
    packet = Ether(dst = 'ff:ff:ff:ff:ff:ff')/ARP(op="who-has", pdst=targetship)
    # Pass target ip to create a packet, 𝘌𝘵𝘩𝘦𝘳 𝘧𝘰𝘳 𝘣𝘳𝘰𝘢𝘥𝘤𝘢𝘴𝘵 and 𝘈𝘙𝘗 𝘵𝘰 𝘳𝘦𝘲𝘶𝘦𝘴𝘵 𝘔𝘈𝘊 
    resp, _ = srp(packet, timeout=2, retry=0, verbose=False)
    # pass packet onto srp to send on Nerwork level 2 (it also receives)
    for _, r in resp:
        return r[Ether].src
    return None 

class Arper:
    def __init__(self, victim, gateway, interface = 'eth0'):
        self.victim = victim
        self.victimMac = get_mac(victim)
        self.gateway = gateway
        self.gatewayMac = get_mac(gateway)
        self.interface = interface
        conf.iface = interface
        conf.verb = 0 
        # initialize the class with the victim and gateway to get their MAC. Specify interface (eth0 as default)
        print(f'Initialized {interface}:')
        print(f'Gateway ({gateway}) is at {self.gatewayMac}')
        print(f'Victim ({victim}) is at {self.victimMac}')
        print('-'*30)
    
    def run(self):
        self.poison_thread = Process(target=self.poison)
        self.poison_thread.start()
        # Poison start to unleach attack
        self.sniff_thread = Process(target=self.sniff)
        self.sniff_thread.start()
        # Sniff start to track attack by network sniffing
    
    def poison(self):
        pass
    
    def sniff():
        pass
    
    def restore(self):
        pass
    
if __name__ == '__main__':
    (victim, gateway, interface) = (sys.argv[1], sys.argv[2], sys.argv[3])
    arpoon = Arper(victim, gateway, interface)
    arpoon.run()