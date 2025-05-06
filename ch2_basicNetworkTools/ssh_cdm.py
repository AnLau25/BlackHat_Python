#SSH (Secure Shell) protocol on Python with Paramiko (PyCripto for SSH2)
import paramiko

def ssh_command(ip, port, user, passwd, cdm):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)
    
    _, stdout, stderr = client.exec_command(cdm)
    output = stdout.readlines() + stderr.readlines()
    if output:
        print('--- Output ---')
        for line in output:
            print(line.strip())
    
    if __name__ == '__main__':
        import getpass
        # user = getpass.getuser()
        user = input('Username: ')
        password = getpass.getpass()
        
        ip = input('Enter server IP: ') or '192.168.1.203' #testing, could be 127.0.0.1??
        port = input('Enter port or <CR>: ') or '2222'
        cdm = input('Enter command or <CR>: ') or 'id'
        ssh_command(ip, port, user, password, cdm)
        
        
        
        
    