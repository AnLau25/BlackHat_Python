#Netcat script in case (more often than not) netcat was removed
import argparse
import socket 
import shlex
import subprocess #interface for process creation and client program interaction
import sys
import textwrap
import threading

def execute(cdm):
    cdm = cdm.strip
    if not cdm:
        return
    output = subprocess.check_output(shlex.split(cdm), stderr=subprocess.STDOUT)
    #𝗰𝗵𝗲𝗰𝗸_𝗼𝘂𝘁𝗽𝘂𝘁 runs the comand and captures the output
    return output.decode()


