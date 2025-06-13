from burp import IBrupExtender
from burp import IIntruderPayloadGenerator
from burp import IIntruderPayloadGeneratorFactory

import random
from java.util import List, ArrayList

class BurpExtender(IBrupExtender, IIntruderPayloadGeneratorFactory):
      
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
        
    

class BHPFuzzer(IIntruderPayloadGenerator): # Extends 𝘐𝘐𝘯𝘵𝘳𝘶𝘥𝘦𝘳𝘗𝘢𝘺𝘭𝘰𝘢𝘥𝘎𝘦𝘯𝘦𝘳𝘢𝘵𝘰𝘳
    
    def __init__(self, extender, attack):
        self._extender = extender
        self._helpers = extender._helpers
        self._attack = attack
        self.max_payloads = 10 # When to ends the iterations
        self.num_iterations = 0 # How many we got (counter)
        
        return 
    
    def hasMorePayloads(self): # Checks if we've reach max_payloads or no
        if self.num_iterations == self.max_payloads:
            return False
        else:
            return True
    
    def getNextPayload(self, current_payload): # Receives og HTTP payload and fuzzes
        
        payload = "".join(chr(x) for x in current_payload) # Byte arr -> str
        # convert to str
        
        payload = self.mutate_payload(payload)
        # call simple mutator to fuzz the POST
        
        self.num_iterations +=1 # fuzzing attemps ++
        
        return payload # retrun mutated 
     
    def reset(self): # Reset iters
        self.num_iterations = 0
        return