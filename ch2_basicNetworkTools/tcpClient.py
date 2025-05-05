#creating a tcp client for service texting & others

import socket

target_host = "127.0.0.1"
target_port = 9998

#create socket obj
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#𝗔𝗙_𝗜𝗡𝗡𝗘𝗧 means we use ⁡⁣⁢⁢𝘴𝘵𝘢𝘯𝘥𝘢𝘳𝘥 𝘐𝘗𝘷4 𝘢𝘥𝘥𝘳 𝘢𝘯𝘥 𝘩𝘰𝘴𝘵𝘯𝘢𝘮𝘦 
#𝗦𝗢𝗖𝗞_𝗦𝗧𝗥𝗘𝗔𝗠 indicates TCP client

#connect to client
client.connect((target_host,target_port))

#send data
client.send(b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n") 

#receive data/response
response = client.recv(4096)

print(response.decode())
client.close()

#Assumptions about the sockets
#   - The connection will always succede
#   - The server expects us to send data first (not always tho)
#   - The server will always return data quickly

#Pentesters usually dont care abt exception and error handdling