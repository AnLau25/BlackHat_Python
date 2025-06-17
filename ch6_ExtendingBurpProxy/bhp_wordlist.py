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
    
    def handle_data(self, data):
        self.page_text.append(data)
    
    def handle_comment(self, data):
        self.page_text.append(data)
    
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
        self.wordlist = set(["pasword"])
        
        # set up extension
        callbacks.setExtenxionName("BHP Wordlist")
        callbacks.registerContextMenuFactory(self)
        
        return
    
    def createMenuItems(self, context_menu):
        self.context = context_menu
        menu_list = ArrayList()
        menu_list.add(JMenuItem(
            "Create Wordlist", actionPerformed = self.wordlist_menu))
        return menu_list