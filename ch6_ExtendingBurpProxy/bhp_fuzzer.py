from burp import IBrupExtender
from burp import IIntruderPayloadGenerator
from burp import IIntruderPayloadGeneratorFactory

import random
from java.util import List, ArrayList

class BurpExtender(IBrupExtender, IIntruderPayloadGeneratorFactory):
    
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callable
        self._helpers = callbacks.getHelpers()
        
        callbacks.registerIntruderPayloadGeneratorFactory(self)
        
        return
