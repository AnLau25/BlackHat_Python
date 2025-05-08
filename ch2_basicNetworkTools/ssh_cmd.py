#SSH (Secure Shell) protocol on Python with Paramiko (PyCripto for SSH2)
import paramiko

#connects to a SSH server and runs a single command
def ssh_command(ip, port, user, passwd, cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    #Set the policy to accept the SSH key for the server (cause we are both)
    client.connect(ip, port=port, username=user, password=passwd)
    
    _, stdout, stderr = client.exec_command(cmd) #If the connection is succesfull we run the command 
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
        
    ip = input('Enter server IP: ') or '192.168.1.203' #testing, should be 127.0.0.1??
    port = int(input('Enter port or <CR>: ') or 2222)
    cmd = input('Enter command or <CR>: ') or 'id'
    ssh_command(ip, port, user, password, cmd)
        
# 𝗣𝗮𝗿𝗮𝗺𝗶𝗸𝗼
# - Supports both password and SSH key authentication
# - In irl circumstances, you'd use keys        

# 𝗡𝗼𝘁𝗮𝘀:
# Wtf is shoulder-surfing???
    
# 𝗦𝗦𝗛 𝗙𝗶𝘅𝗲𝘀:
# 1. Verif SSH → 𝘴𝘶𝘥𝘰 𝘴𝘺𝘴𝘵𝘦𝘮𝘤𝘵𝘭 𝘴𝘵𝘢𝘵𝘶𝘴 𝘴𝘴𝘩
# 2. If "Active: inactive" → 𝘴𝘶𝘥𝘰 𝘴𝘺𝘴𝘵𝘦𝘮𝘤𝘵𝘭 𝘦𝘯𝘢𝘣𝘭𝘦 --𝘯𝘰𝘸 𝘴𝘴𝘩
# 3. Quick fixes:
#   sudo apt install openssh-server
#   sudo systemctl start ssh
#   sudo systemctl enable ssh

# 𝗧𝗲𝘀𝘁 𝟭:
#   python ssh_cmd.py
#   Username: kali
#   Password: 
#   Enter server IP: 127.0.0.1
#   Enter port or <CR>: 22
#   Enter command or <CR>: ip

