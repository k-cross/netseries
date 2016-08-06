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
    print('-u --upload=destination')
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
        if o in ('-h')
