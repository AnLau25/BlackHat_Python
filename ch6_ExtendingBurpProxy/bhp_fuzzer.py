from burp import IBurpExtender
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
    
    def mutate_payload(self, original_payload):
        picker = random.randint(1,3)
        # Sim or external script
        
        offset = random.randint(0, len(original_payload) - 1)
        # select a random offset in payload to mutate
        
        front, back = original_payload[:offset], original_payload[offset:]
        # break the payload into chunks
        
        # sql injection attmept
        if picker == 1:
            front += "'"
        
        elif picker == 2: # attempt to jam an xss (cross site scripting)
            front += "<script>alert('BHP!');</script>"
        
        elif picker == 3: # repeat a random chunk of the original payload
            chunk_length = random.randint(0, len(back)-1)
            repeater = random.randint(1,10)
            for _ in range(repeater):
                front += original_payload[:offset + chunk_length]
        
        return front + back