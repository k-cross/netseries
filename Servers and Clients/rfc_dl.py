import sys
import socket

try:
    rfc_number = int(sys.argv[1])
except (IndexError, ValueError):
    print('Must supply an RFC number as first argument')
    sys.exit(2)

target_host = 'www.ietf.org'
target_port = 80

sock = socket.create_connection((target_host, target_port))

req = (
        'GET /rfc/rfc{rfcnum}.txt HTTP/1.1\r\n'
        'Host: {target_host}:{target_port}\r\n'
        'User-Agent: Python {version}\r\n'
        'Connection: close\r\n'
        '\r\n'
)

req = req.format(
        rfcnum = rfc_number,
        target_host = target_host,
        target_port = target_port,
        version = sys.version_info[0]
)

sock.sendall(req.encode('ascii'))

rfc_raw = bytearray()
while True:
    buf = sock.recv(4096)
    if not len(buf):
        break
    rfc_raw += buf

rfc = rfc_raw.decode('utf-8')

print(rfc)
