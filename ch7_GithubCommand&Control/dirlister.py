import os

def run(**args):
    print("[*] In dirlister module")
    files = os.listdir(".")
    return str(files)    

# Defines 𝘳𝘶𝘯(), function to list all of the files in the current dir and returns them as a string
# Nota: Each module should have a run function taking x args, allowing to load each module in the same way