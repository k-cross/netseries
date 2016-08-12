import sys
import socket
import threading

def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_host, local_port))
    except:
        print('[!] Failed to listen on %s:%d' %(local_host, local_port))
        print('[!] Check for other listening sockets or permissions')
        sys.exit(0)

    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        # print local connection info
        print('[==>] Received incoming connection from %s:%d' % 
             (addr[0], addr[1]))

        proxy_thread = threading.Thread(target=proxy_handler,
            args=(client_socket, remote_host, remote_port, receive_first))

        proxy_thread.start()

def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    # Recieve data from the remote end if needed
    if receive_first:
        remote_buffer = receive_first(remote_socket)
        hexdump(remote_buffer)

        remote_buffer = response_handler(remote_buffer)

        if len(remote_buffer):
            print('[<==] Sending %d bytes to localhost.' % len(remote_buffer))
            client_socket.send(remote_buffer)

    # Loop: read from local, send to remote, send to local
    while True:
        # Read from local
        local_buffer = receive_first(client_socket)

        if len(local_buffer):
            print('[==>] Received %d bytes from localhost.' % len(local_buffer))
            hexdump(local_buffer)

            local_buffer = request_handler(local_buffer)

            # Send to remote
            remote_socket.send(local_buffer)
            print('[==>] Sent to remote.')

        # Receive response
        remote_buffer = receive_first(remote_socket)

        if len(remote_buffer):
            print('[<==] Received %d bytes from remote.' % len(remote_buffer))
            hexdump(remote_buffer)

            # Send to response handler
            remote_buffer = response_handler(remote_buffer)

            # Send response to local socket
            client_socket.send(remote_buffer)
            print('[<==] Sent to localhost.')

        # If no data, close connections
        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print('[*] Connections closed.')

            break

# hex dumping function taken from:
# http://code.activestate.com/recipes/142812-hex-dumper/
def hexdump(src, length=16):
    result = []
    digits = 4 if isinstance(src, unicode) else 2
    for i in range(0, len(src), length):
        s = src[i:i + length]
        hexa = b' '.join(['%0*X' % (digits, ord(x)) for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append(b'%04X %-*s %s' % (i, length*(digits + 1), hexa, text))

    print(b'\n'.join(result))

def receive_from(connection):
    buffer = ''
    connection.settimeout(2)

    try:
        # keep reading from buffer until timeout/no data
        while True:
            data = connection.recv(4096)

            if not data:
                break

            buffer += data
    except:
        pass

    return buffer

def request_handler(buffer):
    # perform packet modifications
    return buffer

def response_handler(buffer):
    # perform packet modifications
    return buffer

def main():
    if len(sys.argv[1:]) != 5:
        print('Usage: proxy.py [localhost] [localport] ...')
        sys.exit(0)

    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    receive_first = sys.argv[5]
    if 'True' in receive_first:
        receive_first = True
    else:
        receive_first = False

    server_loop(local_host, local_port, remote_host, remote_port, receive_first)

if __name__ == '__main__':
    main()
