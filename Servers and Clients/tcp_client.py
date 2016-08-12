"""
Assumptions:
    1. Our connection will always succeed
    2. Server always expects us to send data first
    3. Server will always send us data back in a timely fashion
"""
import socket

target_host = 'www.google.com'
target_port = 80

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_host, target_port))
client.send('GET / HTTP/1.1\r\nHost: google.com\r\n\r\n'.encode('ascii'))

"""
The create_connection is a convienece function for TCP connections
The sendall below can be used for larger texts/requests and lists:

client = socket.create_connection((target_host, target_port))
client.sendall('GET / HTTP/1.1\r\nHost: google.com\r\n\r\n'.encode('ascii'))

"""

response = client.recv(4096)

print(response)
