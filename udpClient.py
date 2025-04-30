#creating a udp client for service texting & others

import socket

target_host = "127.0.0.1"
target_port = 9997

#create socket obj
client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#𝗔𝗙_𝗜𝗡𝗡𝗘𝗧 means we use ⁡⁣⁢⁢𝘴𝘵𝘢𝘯𝘥𝘢𝘳𝘥 𝘐𝘗𝘷4 𝘢𝘥𝘥𝘳 𝘢𝘯𝘥 𝘩𝘰𝘴𝘵𝘯𝘢𝘮𝘦 
#𝗦𝗢𝗖𝗞_𝗗𝗚𝗥𝗔𝗠 indicates UDP client

#send data
client.sendto(b"AAABBBCCC",(target_host,target_port)) 
#UDP is a connectionless protocol, so there is no connect() call

#receive data/response
data, addr = client.recvfrom(4096)

print(data.decode())
client.close()

#Network programmers are the fancy ones