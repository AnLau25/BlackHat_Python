#technicaly, wireshark for when u don't have accces (tcp proxy)
import sys
import socket
import threading

HEX_FILTER = ''.join(
    [(len(repr(chr(i)))==3) and chr(i) or '.' for i in range(256)] #If length == 3, get char, else, '.'
)#String containing ASCII printable characters.
 #If not printable, print dot

def hexdump(src, length=16,show=True): #Displays coms between local and remote machines
    if isinstance(src,bytes):
        src = src.decode() #Decodes if any byte was passed
    
    results = list()
    
    for i in range(0, len(src),length): #Grabs pieces of the decode and places it in word
        word = str(src[i:i+length])
        
        printable = word.translate(HEX_FILTER) #Substitutes the strings by the raw printable, via .translate()
        hexa = ''.join([f'{ord(c):02X}' for c in word]) #Substitutes the raw printable by hex
        hexwidth =  length*3 
        results.append(f'{i:04x} {hexa:<{hexwidth}} {printable}')#New array containg the hex value of the first index, the hex value of the word and the word 
    if show:
        for line in results:
            print(line)
    else:
        return results
    #Usefull to find user credentials in plain text protocol and understanding unkown protocols
    
#receives local and remote data
def receive_from (connection):
    buffer = b"" #empty byte string, responces from socket
    connection.settimeout(5) #default, but can be modified based on need
    try:
        while True: #Loop to read data
            data = connection.recv(4096)
            if not data: #Until no more data or time out
                break
            buffer += data
    except Exception as e:
        pass
    return buffer #returns to remote or local caller
 
#To modify response/requests before proxy sends them   
def request_handler(buffer):
    #client modifs here
    return buffer
        
def response_handler(buffer):
    #client modifs here
    return buffer

        
if __name__ == "__main__":
    hexdump("python is a language\n and Aston is a car\n")
    