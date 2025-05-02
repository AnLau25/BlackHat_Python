#technicaly, wireshark for when u don't have accces (tcp proxy)
import sys
import socket
import threading

HEX_FILTER = ''.join(
    [(len(repr(chr(i)))==3) and chr(i) or '.' for i in range(256)] #If length == 3, get char, else, '.'
)#String containing ASCII printable characters.
 #If not printable, print dot

def hexdump(src, length=16, show=True): #Displays coms between local and remote machines
    if isinstance(src,bytes):
        src = src.decode() #Decodes if any byte was passed
    
    results = list()
    
    for i in range(0, len(src), length): #Grabs pieces of the decode and places it in word
        word = str(src[i:i+length])
        
        printable = word.translate(HEX_FILTER) #Substitutes the strings by the raw printable, via .translate()
        hexa = ''.join([f'{ord(c):02X}' for c in word]) #Substitutes the raw printable by hex
        hexwidth =  length*3 
        results.append(f'{i:04x} {hexa:<{hexwidth}>} {printable}')#New array containg the hex value of the first index, the hex value of the word and the word 
    if show:
        for line in results:
            print(line)
    else:
        return results
    #Usefull to find user credentials in plain text protocol and understanding unkown protocols