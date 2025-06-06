# acc thought it said butter, anyway Ɛ( · — ·)3
# Normalmente lanzarias una araña como la de Burp Suit, para "crawl" a travez delos files
# Pero, a veces, lo que quires agarrar son ficheros de configuracion, debugging o restos del dev que no c usaron
# En ese caso puedes usar fuerza brta ara encontrarlos por medio de nombres, como el projecto Gobuster o SVNDigger
# Descargarel .zip de SVNDigger de github y encontrar all.txt 

import sys
import queue
import requests
import threading

AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0"
TARGET = "http://testphp.vulnweb.com"
EXTENSIONS = ['.php', '.bak', '.orig', '.inc']
THREADS = 50
WORDLIST = "/home/kali/all.txt"

def get_words(resume=None):
    
    def extended_words(word): # inner function to try extensions on every word
        if "." in word:
            words.put(f'/{word}')
        else:
            words.put(f'/{word}/')
        
        for extension in EXTENSIONS:
            words.put(f'/{word}{extension}')
            
    with open(WORDLIST) as f:
        raw_words = f.read() # Read word list
    
    found_resume = False
    words = queue.Queue()
    
    for word in raw_words.split():
        if resume is not None: # Set the path to the last brute forcer tried, in case of disconection
            if found_resume:
                extended_words(word)
            elif word==resume:
                found_resume = True
                print(f'Resuming wordlist from: {resume}')
        else:
            # print(word) ok so it's printing, all right. Wayyy too much noice tho 
            extended_words(word)
    
    return words #queue of words to use in the acc brute forcer function

def dir_bruter(words):
    headers = {'User-Agent': AGENT} # Agent created to pass the request as "decent ppl"
    
    while not words.empty(): # Loop through the words queue
        url = f'{TARGET}{words.get()}' # Create a new url
        try: # send request to remote server
            r = requests.get(url, headers=headers)
        except requests.exceptions.ConnectionError:
            sys.stderr.write('x');sys.stderr.flush() # Print "x" in case of error
            continue
        
        if r.status_code in [200, 301, 302]: # Includes redirect cause it might be interesting
            print(f'\nSucces ({r.status_code}: {url})')
        elif r.status_code == 404:
            sys.stderr.write('.');sys.stderr.flush() # Print "." in case of error 404/not found
        else:
            print(f'{r.status_code} => {url}') 
            # Anything else, we print the url, cause it means there might be smt there
    
if __name__=="__main__":
    words = get_words() # Create the words queue
    sys.stdin.readline() 
    # Creates a small pause, just so that the suden trafic goes unoticed, press any key to coninue
    for _ in range(THREADS):
        t = threading.Thread(target=dir_bruter, args=(words,))
        t.start() # start threads
        
# 𝗧𝗲𝘀𝘁:
#
# .......................
# Succes (200: http://testphp.vulnweb.com/admin/)
# ...
# Succes (200: http://testphp.vulnweb.com/CVS/)
# .....................................................
#
# ------------ but load of "." responses ------------
#
# .............................................xxxxxx..
# .....................................................
# Succes (200: http://testphp.vulnweb.com/index.bak)
# Succes (200: http://testphp.vulnweb.com/index.php)...
#
# Cut of the sake of my sanity, but it returns a lot of links   
# Again, keep in mind, this is OWASP's vulnerable web