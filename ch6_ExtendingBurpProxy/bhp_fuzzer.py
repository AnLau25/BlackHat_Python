from burp import IBrupExtender
from burp import IIntruderPayloadGenerator
from burp import IIntruderPayloadGeneratorFactory

import random
from java.util import List, ArrayList

class BurpExtender(IBrupExtender, IIntruderPayloadGeneratorFactory):
    
    def __init__(self, extender, attack):
        self._extender = extender
        self._helpers = extender._helpers
        self._attack = attack
        self.max_payloads = 10
        self.num_iterations = 0
        
        return 
    
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        
        callbacks.registerIntruderPayloadGeneratorFactory(self)
        # Using 𝘳𝘦𝘨𝘪𝘴𝘵𝘦𝘳𝘐𝘯𝘵𝘳𝘶𝘥𝘦𝘳𝘗𝘢𝘺𝘭𝘰𝘢𝘥𝘎𝘦𝘯𝘦𝘳𝘢𝘵𝘰𝘳𝘍𝘢𝘤𝘵𝘰𝘳𝘺 method to register class 
        # Let's Intruder tool know that 𝘉𝘶𝘳𝘱𝘌𝘹𝘵𝘦𝘯𝘥𝘦𝘳 can generate payloads
        
        return

    def getGeneratorName(self):
        return "BHP Payload Generator"
    
    def createNewInstance(self, attack):
        return BHPFuzzer(self, attack)
        # Receives 𝘢𝘵𝘵𝘢𝘤𝘬 parameter & returns the 𝘐𝘐𝘯𝘵𝘳𝘶𝘥𝘦𝘎𝘦𝘯𝘦𝘳𝘢𝘵𝘰𝘳 class (ie BHPFuzzer)
        
    def hasMorePayloads(self):
        if self.num_iterations == self.max_payloads:
            return False
        else:
            return True
    
    def reset(self):
        self.num_iterations = 0
        return
        