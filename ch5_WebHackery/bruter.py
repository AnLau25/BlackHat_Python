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
    
    def extended_words(word):
        if "." in word:
            words.put(f'/{word}')
        else:
            words.put(f'/{word}')
        
        for extension in EXTENSIONS:
            words.put(f'/{word}{extension}')
            
    with open(WORDLIST) as f:
        raw_words = f.read
    
    
