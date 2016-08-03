"""
Assumptions:
    1. Our connection will always succeed
    2. Server always expects us to send data first
    3. Server will always send us data back in a timely fashion
"""
import socket

target_host = "www.google.com"
target_port = 80

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_host, target_port))
client.send("GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")

response = client.recv(4096)

print(response)
