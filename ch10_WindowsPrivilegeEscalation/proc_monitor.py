# Monitors proc creation and privilege tracking

import os
import sys
import win32api
import win32con
import win32security
import wmi

def get_proc_pivileges(pid):
    try:
        hproc = win32api.OpenProcess(
            win32api.PROCESS_QUERY_INFORMATION, False, pid
        )
        htok = win32security.OpenProcessToken(hproc, win32con.TOKEN_QUERY)
        privs = win32security.GetTokenInformation(htok, win32security.TokenPrivileges)
        privileges = ''
        for priv_id, flags in privs:
            if flags == (win32security.SE_PRIVILEGE_ENABLED | win32security.SE_PRIVILEGE_ENABLED_BY_DEFAULT):
                privileges += f'{win32security.LookupPrivilegeName(None, priv_id)}|'
    except Exception:
        privileges = 'N/A'
    
    return privileges


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
        
# 𝗧𝗲𝘀𝘁 𝟭:
# 
# 𝘱𝘳𝘰𝘤𝘦𝘴𝘴_𝘮𝘰𝘯𝘪𝘵𝘰𝘳_𝘭𝘰𝘨.𝘴𝘤𝘷 will apear in same folder, indicates the info we wants to catch
# 
# 𝗜𝗻 𝗖𝗠𝗗:
# python proc_monitor.py
# ('"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe" --type=renderer --extension-process --enable-dinosaur-easter-egg-alt-images --no-pre-read-main-dll --video-capture-use-gpu-memory-buffer --lang=en-US --device-scale-factor=1.25 --num-raster-threads=2 --enable-main-frame-before-activation --renderer-client-id=2532 --time-ticks-at-unix-epoch=-1751562848156566 --launch-time-ticks=83545087428 --metrics-shmem-handle=4320,i,12564247726896596968,16379157665239309029,2097152 --field-trial-handle=2116,i,3987644641829430670,16292763222225121616,262144 --variations-seed-version=20250702-180038.517000 --mojo-platform-channel-handle=11592 /prefetch:2, 20250704122622.065611-240, C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe', "13544, 8580, ('DESKTOP-D9T7SMS', 0, 'User'), N/A")
# <Test by opening various programs to check the procs they generate, try sing-out/in>