# Using burp caught trafic to generate a word lists

from burp import IBurpExtender
from burp import IContextMenuFactory

from java.util import ArrayList
from javax.swing import JMenuItem

from datetime import datetime
from HTMLParser import HTMLParser

import re

class TagStripper(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.page_text = []
    
    # Store page text as a member variable
    def handle_data(self, data):
        self.page_text.append(data)
    
    # Adds the words stored in developer comments to the psswd lst
    def handle_comment(self, data):
        # Tho, technically, just calls 𝘩𝘢𝘯𝘥𝘭𝘦_𝘥𝘢𝘵𝘢(), but it could be it's own thing
        self.page_text.append(data)
    
    # Takes html content and strips it to txt
    def strip(self, html):
        self.feed(html)
        return " ".join(self.page_text)

class BurpExtender(IBurpExtender,IContextMenuFactory):
    
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self.context = None
        self.hosts = set()
    
        # Start with something common/espected
        self.wordlist = set(["password"]) # like "password"
        
        # set up extension
        callbacks.setExtensionName("BHP Wordlist")
        callbacks.registerContextMenuFactory(self)
        
        return
    
    def createMenuItems(self, context_menu):
        self.context = context_menu
        menu_list = ArrayList()
        menu_list.add(JMenuItem(
            "Create Wordlist", actionPerformed = self.wordlist_menu))
        return menu_list
    
    def wordlist_menu(self, event):
        http_traffic = self.context.getSelectedMessage()
        # grab details of what the user clicked
        # Triggered when the user clicks on defined menu item
        
        for traffic in http_traffic:
            http_service = traffic.getHttpService()
            host = http_service.getHost()
            # Retreive IP and host name 
            self.hosts.add(host)
            http_response = traffic.getResponse()
            
            # Send name of respnding host to 𝘨𝘦𝘵_𝘸𝘰𝘳𝘥𝘴()
            if http_response:
                self.get_words(http_response)
        
        self.display_wordlist()
        return
    
    def get_words(self, http_response):
        headers, body = http_response.tostring().split('\r\n\r\n',1)
        
        # skip non-text responses
        if headers.lower().find('content-type: text') == -1:
            return
        
        # strips HTML code from the rest of the page txt
        tag_stripper = TagStripper()
        page_text = tag_stripper.strip(body)
        
        # Find all the wordsstarting with an alphabetic char by ussing reg expressions
        words = re.findall("[a-zA-Z]\w{2}", page_text)
        
        for word in words:
            # filter out long strings
            if len(word)<=14: # Store in lowecase
                self.wordlist.add(word.lower())
        
        return
    
    def mangle(self, word):
        year = datetime.now().year 
        suffixes = ["", "1", "!", "year"] # Suffixes to try with
        mangled = []
        
        for password in (word, word.capitalize()): 
        # Loop through words and suffises to create multiple combinations, both lower and upper case
            for suffix in suffixes:
                mangled.append("%s%s" % (password, suffix))
        
        return mangled
    
    def display_wordlist(self):
        print("#!comment: BHP Wordlist for site(s) %s" % ", ".join(self.hosts))
        # John the Ripper style comment to know what site the pswds are from
        
        for word in sorted(self.wordlist):
            for password in self.mangle(word):
                print(password)
        
        return