import socket
import sys
import json
from threading import Thread
from time import sleep

import platform_HB


def do_ping(mach_address):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print 'ping socket create failed. Bye Bye.'
        return

    print 'ping socket created'
    
    s.connect((mach_address , int(platform_HB_port))) 
    print 'ping socket connected'
    
    message = '["ping"]'
    print 'ping message: ' + message

    s.sendall(message)

def ping_machine():
    print 'available machines:'
    machid = 0
    for m in machines:
        print str(machid) + ' : ' + str(m)
        machid += 1
        
    machid_raw = raw_input('select: ')   
    mach = int(machid_raw)
    mach_address = machines[mach][0]
    
    print 'selected machine IP: ' + mach_address
    
    do_ping(mach_address)
    
    
# platform_IP = pu.get_ip_address('eth0')

config = None

try:
    config_file_name = "platform.config"
    config_file = open(config_file_name)
    config = json.load(config_file)
except:
    print 'Cannot read config.json. Bye bye.'
    sys.exit()

if not 'platform_IP' in config:
    print 'platform_IP not configured. Bye bye.'
    sys.exit()

if not 'platform_port' in config:
    print 'platform_port not configured. Bye bye.'
    sys.exit()


platform_HB_IP = config['platform_IP']
platform_HB_port = int(config['platform_port'])

print 'IP: ' + platform_HB_IP
print 'port: ' + str(platform_HB_port)

HB_server_thread = platform_HB.start_HB_server(platform_HB_IP, platform_HB_port)

do_continue = True

while do_continue:
    option = raw_input( 'Options:\n-q: quit\n-p: ping machine' )
    if option == 'q':
        platform_HB.stop_HB_server()
        do_continue = False
        
    elif option == 'p':
        ping_machine()
    else:
        print 'unknown option'
    



HB_server_thread.join()

print 'Bye bye.'

    

