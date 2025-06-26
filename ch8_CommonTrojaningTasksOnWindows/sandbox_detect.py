# Since antiviruses started using Sandboxing to determine sus behaviour, we need to learn to avoid falling in a sandbox
# This, whether the sandbox runs on network perimeter, popular option, or directly on the target machine
# We do this by, basicaly, looking for usser interaction, since sandboxes are usualy automated
# 
# The result of the timestamp should be judged based on the specific trojaning tactic used 

from ctypes import byref, c_uint, c_ulong, sizeof, Structure, windll
import random
import sys
import time
import win32api

class LASTINPUTINFO(Structure): # Time stamp in millisecond of the last input recorded
    fields_ = [('cbSize', 'c_uint'), ('dwTime', 'c_ulong')]
    
def get_last_input(): # Determine the last time of inut
    struct_lastinputinfo = LASTINPUTINFO()
    struct_lastinputinfo.cbSize = sizeof(LASTINPUTINFO) # Init cbSize
    
    windll.user32.GetLastInputInfo(byref(struct_lastinputinfo)) # Populates dwTime with a time stapm
    run_time = windll.kernel32.GetTickCount() # For how long has the system been runring
    
    elapsed = run_time - struct_lastinputinfo.dwTime # calculates acc last input
    print(f"[*] It's been {elapsed} milliseconds since the last event")
    
    return elapsed

while True: # Tester
    get_last_input()
    time.sleep(1)

