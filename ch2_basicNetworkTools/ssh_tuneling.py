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
        
def reverse_forward_tunnel(server_port, remote_host, remote_port, transport):
    transport.request_port_forward("", server_port)
    while True:
        chan = transport.accept(1000)
        if chan is None:
            continue
        thr = threading.Thread(
            target=handler, args=(chan, remote_host, remote_port)
        )
        thr.setDaemon(True)
        thr.start()