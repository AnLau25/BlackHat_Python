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

class NetCat:
    def __init__(self, args, buffer=None): #innit with command line args and buffer
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket (client)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        
    def listen(self):
        self.socket.bind((self.args.target, self.args.port)) #binds target and port
        self.socket.listen(5)
        
        while True: #listen in a loop
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread(
                target=self.handle, args=(client_socket,) #passing connected socket to handle()
            )
            client_thread.start
            
    def send(self):
        self.socket.connect((self.args.target, self.args.port))
        if self.buffer:
            self.socket.send(self.buffer)
        try:
            while True:
                recev_len = 1
                response = ''
                while recev_len:
                    data = self.socket.recv(4096)
                    recev_len = len(data)
                    response += data.decode()
                    if recev_len<4096:
                        break
                if response:
                    print(response)
                    buffer = input('>')
                    buffer += '\n'
                    self.socket.send(buffer.encode())
        except KeyboardInterrupt:
            print('User terminated.')
            self.socket.close()
            sys.exit()
        
    def run(self):
        if self.args.listen: #If listener, call listener method
            self.listen()
        else: #Else, send
            self.send()        

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

