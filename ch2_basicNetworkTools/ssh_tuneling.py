# 𝗦𝗦𝗛 𝗧𝘂𝗻𝗲𝗹𝗶𝗻𝗴
# - Instead of directly sending commands, the tunel sends SSH packaged trafic to the server
# - The server then unpackages it and delivers it
# - 𝗨𝘀𝗲𝗳𝘂𝗹 𝗶𝗳 𝘁𝗵𝗲 𝗦𝗦𝗛 𝘀𝗲𝗿𝘃𝗲𝗿 𝗵𝗮𝘀 𝗮𝗰𝗰𝗲𝘀 𝘁𝗼 𝘁𝗵𝗲 𝘄𝗲𝗯 𝗯𝘂𝘁 𝗻𝗼 𝘁𝗼𝗼𝗹𝘀 𝘁𝗼 𝗵𝗮𝗰𝗸 𝘄𝗶𝘁𝗵 𝗮𝗻𝗱 𝘂 𝗵𝗮𝘃𝗲 𝗻𝗼 𝘄𝗲𝗯 𝗮𝗰𝗰𝗲𝘀
# - Ie you are sending the tools through the tunel to the server, to the web
# - Instead of sending them from the server to the web urself (𝗳𝗼𝗿𝘄𝗮𝗿𝗱 𝗦𝗦𝗛 𝘁𝘂𝗻𝗲𝗹𝗶𝗻𝗴)
# - 𝗜𝗳 𝗻𝗼 𝗦𝗦𝗛 𝘀𝗲𝗿𝘃𝗲𝗿, 𝗿𝗲𝘃𝗲𝗿𝘀𝗲 𝘁𝘂𝗻𝗻𝗲𝗹𝗶𝗻𝗴 is the option
# - In that case, u get tuneled to the local host (port to 3389 for ex to acces internal sytem)

# 𝗣𝗮𝗿𝗮𝗺𝗶𝗸𝗼 𝗿𝗳𝗼𝗿𝘄𝗮𝗿𝗱 (forward tunneling)
def main():
    options, server, remote = parse_options() # Double check to make sure all the necessary arguments are passed before connection

    password = None
    if options.readpass:
        password = getpass.getpass("Enter SSH password: ")

    client = paramiko.SSHClient() # Paramiko client connection
    client.load_system_host_keys()  
    client.set_missing_host_key_policy(paramiko.WarningPolicy())

    verbose("Connecting to ssh host %s:%d ..." % (server[0], server[1]))
    try:
        client.connect(
            server[0],
            server[1],
            username=options.user,
            key_filename=options.keyfile,
            look_for_keys=options.look_for_keys,
            password=password,
        )
    except Exception as e:
        print("*** Failed to connect to %s:%d: %r" % (server[0], server[1], e))
        sys.exit(1)

    verbose(
        "Now forwarding remote port %d to %s:%d ..."
        % (options.port, remote[0], remote[1])
    )

    try: # try calling server tunnel
        reverse_forward_tunnel(
            options.port, remote[0], remote[1], client.get_transport()
        )
    except KeyboardInterrupt:
        print("C-c: Port forwarding stopped.")
        sys.exit(0)
        
# 𝗣𝗮𝗿𝗮𝗺𝗶𝗸𝗼 𝗵𝗮𝘀 𝘁𝘄𝗼 𝗺𝗮𝗶𝗻 𝘁𝗿𝗮𝗻𝘀𝗽𝗼𝗿𝘁 𝗺𝗲𝘁𝗵𝗼𝗱𝘀
# 𝗧𝗿𝗮𝗻𝘀𝗽𝗼𝗿𝘁: Makes and maintanins the incripted connection      
# 𝗖𝗵𝗮𝗻𝗻𝗲𝗹: Acts as a socket to receive and send data over the transport session

def reverse_forward_tunnel(server_port, remote_host, remote_port, transport):
    transport.request_port_forward("", server_port) # Start with a forward TCP connection from 𝘴𝘦𝘳𝘷𝘦𝘳_𝘱𝘰𝘳𝘵 
    while True:
        chan = transport.accept(1000) # Start new transport channel
        if chan is None:
            continue
        thr = threading.Thread(
            target=handler, args=(chan, remote_host, remote_port) # call handler over the channel
        )
        thr.setDaemon(True)
        thr.start()

# In charge of coms, ie, sends and receives data
def handler(chan, host, port):
    sock = socket.socket()
    try:
        sock.connect((host, port))
    except Exception as e:
        verbose("Forwarding request to %s:%d failed: %r" % (host, port, e))
        return

    verbose(
        "Connected!  Tunnel open %r -> %r -> %r"
        % (chan.origin_addr, chan.getpeername(), (host, port))
    )
    while True: # coms loop
        r, w, x = select.select([sock, chan], [], [])
        if sock in r:
            data = sock.recv(1024)
            if len(data) == 0:
                break
            chan.send(data)
        if chan in r:
            data = chan.recv(1024)
            if len(data) == 0:
                break
            sock.send(data)
    chan.close()
    sock.close()
    verbose("Tunnel closed from %r" % (chan.origin_addr,))
    
# 𝗧𝗲𝘀𝘁 𝟭:
# Download rforward.py from Paramiko's git
# 𝗰𝗹𝗶𝗲𝗻𝘁 (𝘸𝘪𝘯𝘥𝘰𝘸𝘴) → python rforward.py 127.0.0.1 -p 8081 -r 192.168.1.207:3000 --user=kali --password
#                   Enter SSH password:
#                   Connecting to ssh host 127.0.0.1:22 ...
#                   Now forwarding remote port 8081 to 192.168.1.207:3000 ... 
# 𝘀𝗲𝗿𝘃𝗲𝗿 (𝘬𝘢𝘭𝘪) → http://localhost:8081 → 192.168.1.207:3000 
# ie, the server goes to the addres we want, through it's own address

# kept getting "*** Failed to connect to 127.0.0.1:22: NoValidConnectionsError(None, 'Unable to connect to port 22 on 127.0.0.1')"