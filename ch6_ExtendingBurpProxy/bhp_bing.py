# Bing allows you to query for for all the websites it finds at an IP using, the "IP" search modifier

from burp import IBurpExtender
from burp import IContextMenuFactory

from java.net import URL
from java.util import ArrayList
from javax.swing import JMenuItem
from thread import start_new_thread

import json
import socket
import urllib
API_KEY = "YOURKEY"
API_HOST = 'api.cognitive.microsoft.com'


class BurpExtender(IBurpExtender, IContextMenuFactory):
    
    def registerExtender(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self.context = None
        
        # Set up extentsion
        callbacks.setExtensionName("BHP Bing")
        callbacks.registerContexMenuFactory(self)
        
        return
        