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

class Arper:
    def __init__(self, victim, gateway, interface = 'eth0'):
        pass
    
    def run(self):
        pass
    
    def poison(self):
        pass
    
    def sniff():
        pass
    
    def restore(self):
        pass