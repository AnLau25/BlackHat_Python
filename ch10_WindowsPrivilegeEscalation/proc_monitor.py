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

def monitor():
    head = 'CommandLine, Time, Executable, Parent PID, PID, User, Privileges'
    log_to_file(head)
    c = wmi.WMI() # wmi instance
    process_watcher = c.Win32_Process.watch_for('creation')
    # Tell 𝘤 to watch for the "process 𝘤𝘳𝘦𝘢𝘵𝘪𝘰𝘯 event"
    
    while True: # Blocks until new process is found
        try: # Use Win32_Process class to catch proc info
            new_process = process_watcher()
            cmndline = new_process.CommandLine
            create_date = new_process.CreationDate
            executable = new_process.ExecutablePath
            parent_pid = new_process.ParentProcessId
            pid = new_process.ProcessId
            proc_owner = new_process.GetOwner() # To determine who spawned the proc
            
            privileges = 'N/A'
            process_log_message = ( # Print findings
                f'{cmndline}, {create_date}, {executable}',
                f'{parent_pid}, {pid}, {proc_owner}, {privileges}'
            )
            
            print(process_log_message)
        except Exception:
            pass

if __name__ == '__main__':
    monitor()
        
    
        
    