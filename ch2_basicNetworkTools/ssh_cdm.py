#SSH (Secure Shell) protocol on Python with Paramiko (PyCripto for SSH2)
import paramiko

#connects to a SSH server and runs a single command
def ssh_command(ip, port, user, passwd, cdm):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    #Set the policy to accept the SSH key for the server (cause we are both)
    client.connect(ip, port=port, username=user, password=passwd)
    
    _, stdout, stderr = client.exec_command(cdm) #If the connection is succesfull we run the command 
    output = stdout.readlines() + stderr.readlines() 
    if output: #If output, print each line of the output
        print('--- Output ---')
        for line in output:
            print(line.strip())
    
if __name__ == '__main__':
    import getpass #gets current environement username
    # user = getpass.getuser()
    user = input('Username: ') #asks on commandline since it is diferent on both machines
    password = getpass.getpass() #gets the password, does no display it
        
    ip = input('Enter server IP: ') or '192.168.1.203' #testing, could be 127.0.0.1??
    port = input('Enter port or <CR>: ') or '2222'
    cdm = input('Enter command or <CR>: ') or 'id'
    ssh_command(ip, port, user, password, cdm)
        
        
# 𝗣𝗮𝗿𝗮𝗺𝗶𝗸𝗼
# - Supports both password and SSH key authentication
# - In irl circumstances, you'd use keys        

# 𝗡𝗼𝘁𝗮𝘀:
# Wtf is shoulder-surfing???
    