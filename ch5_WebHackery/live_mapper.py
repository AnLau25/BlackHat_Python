#Testing mapper on a live target

import os
import sys
import time
import queue
import requests
import threading
import contextlib

FILTERED = [".jpg", ".gif", ".png", ".css"] # List of extensions to ignore
TARGET = "http://boodelyboo.com/wordpress" # Id target website
THREADS = 10

answers = queue.Queue() # Localy located file paths
web_paths = queue.Queue() # Paths atempted to locate in the remote server

def gather_paths():
    for root, _, files in os.walk('.'): # 𝘰𝘴.𝘸𝘢𝘭𝘬() to "walk" through the file directories in the local web app 
        for fname in files:
            if os.path.splitext(fname)[1] in FILTERED: # Test discovered files on current 𝘱𝘢𝘵𝘩 against 𝘍𝘐𝘓𝘛𝘌𝘙𝘌𝘋
                continue
            path = os.path.join(root, fname)
            if path.startswith('./'): # modified for path reding (mod 1)
                path = path[2:] # mod 2
                print(path)
                web_paths.put(path) # Append valid discovered path

@contextlib.contextmanager
# Usuall you'd be needin a __enter__ and __exit__ methods for context manager
# But we don't need a full context manager, nor that much control
# So in-comes @𝘤𝘰𝘯𝘵𝘦𝘹𝘵𝘭𝘪𝘣.𝘤𝘰𝘯𝘵𝘦𝘹𝘵𝘮𝘢𝘯𝘢𝘨𝘦𝘳: Allows to turn a generator function into a context manager 
def chdir(path):
    """
        On enter, change directory to specified path.
        On exit, change directory back to original.
    """
    this_dir = os.getcwd() # Innits by saving current path
    os.chdir(path)
    try:
        yield # control back to 𝘨𝘢𝘵𝘩𝘦𝘳_𝘱𝘢𝘵𝘩𝘴()
    finally: # always executes
        os.chdir(this_dir) # rever to origine dir

def test_remote():
    while not web_paths.empty(): # loop until web_paths is empty 
        path = web_paths.get() # for each iter, grab a path from the Queue
        url = f'{TARGET}{path}' # and add it to the target web path 
        time.sleep(2) # the target may have throttling/lockout (ie, locks you out if you send too many requests)
        r = requests.get(url) # attempt to retreive the formed url
        if r.status_code == 200: # success == 200
            answers.put(url) # add to answers on succes
            sys.stdout.write('+')
        else:
            sys.stdout.write('x') # x to let us know it failed
        sys.stdout.flush()
            
        
        

if __name__=="__main__":
    with chdir("/home/kali/wordpress"): # with statement to set path to execute code into and dir to go-back-to
        gather_paths()
    input('Press return to continue.')