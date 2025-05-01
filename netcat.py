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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(#creates the command line interface
        description='BHP Net Tool',
        formatter_class= argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Example:
            netcat.py -t 192.168.1.108 -p 5555 -l -c # command shell
            netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt #upload to file
            netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat /etc/passwd\" #execute command
            echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135 #echo text to port 135
            netcat.py -t 192.168.1.108 -p 5555 #connect to server'''
        )
    )#examples of program usage from --help
    
    parser.add_argument('c' '--command', action='store_true', help='command shell')
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
    parser.add_argument('-t', '--target', default='192.168.1.203', help='specified IP')
    parser.add_argument('-u', '--upload', help='upload file')
    #c, -𝗲 and -𝘂 imply -𝗹 since they are on the listener side
    #the sender side makes the conection to the listener so it 𝗼𝗻𝗹𝘆 𝗻𝗲𝗲𝗱𝘀 -𝘁 𝗮𝗻𝗱 -𝗽 𝘁𝗼 𝗱𝗲𝗳𝗶𝗻𝗲 𝘁𝗵𝗲 𝘁𝗮𝗿𝗴𝗲𝘁 
    args = parser.parse_args()
    if args.listen:#setup as a listener → invoke NetCat with empty buffer
        buffer=''
    else:#else send buffer content from stdin
        buffer=sys.stdin.read()
    
    nc = NetCat(args, buffer.encode())
    nc.run         

