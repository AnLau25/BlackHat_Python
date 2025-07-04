# Monitors proc creation and privilege tracking

import os
import sys
import win32api
import win32con
import win32security
import wmi

def log_to_file(message):
    with open('process_monitor_log.scv', 'a') as fd:
        fd.write(f'{message}\r\n')
        
    