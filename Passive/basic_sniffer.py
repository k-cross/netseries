import sys
import socket
import os
import struct
from ctypes import *

class IP(Structure):
    _fields_ = [
            ('ihl', c_ubyte, 4),
            ('version', c_ubyte, 4),
            ('tos', c_ubyte),
            ('len', c_ushort),
            ('id', c_ushort),
            ('offset', c_ushort),
            ('ttl', c_ubyte),
            ('protocol_num', c_ubyte),
            ('sum', c_ushort),
            ('src', c_uint32), 
            ('dst', c_uint32)
    ]

    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer=None):
        # Map protocol constants to their names
        self.protocol_map = {1:'ICMP', 6:'TCP', 17:'UDP'}

        # Human readable IP addresses
        self.src_address = socket.inet_ntoa(struct.pack('@I', self.src))
        self.dst_address = socket.inet_ntoa(struct.pack('@I', self.dst))

        # Human readable protocol
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)


# Host to listen on
def main():
    if len(sys.argv) > 1:
        host = sys.argv[1]
    else:
        host = '192.168.1.119'

    # create raw socket and bind to public interface
    if os.name == 'nt':
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    print('[*] Starting')

    try:
        sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
        sniffer.bind((host, 0))
        sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1) # Includes IP headers in capture

        # If using Windows, send IOCTL to setup promiscuous mode
        if os.name == 'nt':
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    
        while True:
            # Read in a single packet
            raw_buffer = sniffer.recvfrom(65565)[0]

            # Create IP header from the buffer's first 20 bytes, passing in 32 bytes because of from_buffer_copy error
            ip_header = IP(raw_buffer)

            # Print detected host and protocol
            print('Protocol: %s %s -> %s' % (ip_header.protocol, ip_header.src_address, ip_header.dst_address))

    except KeyboardInterrupt:
        # Turn off promiscuous mode for Windows
        if os.name == 'nt':
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
 
        print('[!] Exiting!')
        sys.exit(1)

if __name__ == '__main__':
    main()
