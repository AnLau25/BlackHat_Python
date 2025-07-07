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

if __name__ == 'main':
    for path in PATHS: 
        # Lauch monitor for all paths in dir list
        monitor_thread = threading.Thread(target=monitor, args=(path,))
        monitor_thread.start()