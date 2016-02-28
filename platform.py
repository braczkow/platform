import socket
import platform_utils as pu
from threading import Thread
from time import sleep

HB_threads = []
machines = []

def platform_HB_worker(connection):
    while True:
        data = connection.recv(256)
        print 'data: ' + data
              
        
def start_platform_HB(connection):
    print "Starting platform_HB thread"
    HB_thread = Thread(target = platform_HB_worker, args=[connection])
    HB_thread.start()
    return HB_thread

def server_worker(platform_IP, platform_port):
    print 'server_worker'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((platform_IP, platform_port))
    sock.listen(1)
    
    while True:
        print 'wait for client'
        connection, client_address = sock.accept()
        print 'accepted from: ' + str(client_address)
        global machines
        machines.append(client_address)
        
        global HB_threads
        HB_threads.append( start_platform_HB(connection) )
        

def start_server(platform_IP, platform_port):
    print 'starting server'
    server_thread = Thread(target = server_worker, args=[platform_IP, platform_port])
    server_thread.start()
    return server_thread

def do_ping(mach_address):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print 'ping socket create failed. Bye Bye.'
        return

    print 'ping socket created'
    
    s.connect((mach_address , int(platform_port))) 
    print 'ping socket connected'
    
    message = '["ping"]'
    print 'ping message: ' + message

    s.sendall(message)

def ping_machine():
    print 'available machines:'
    machid = 0
    for m in machines:
        print str(machid) + ' : ' + m
        machid += 1
        
    machid_raw = raw_input('select: ')   
    mach = int(machid_raw)
    mach_address = machines[mach]
    
    print 'selected machine IP: ' + mach_address
    
    do_ping(mach_address)
    
    


platform_IP = pu.get_ip_address('eth0')
platform_port = 8888

print 'IP: ' + platform_IP

server_thread = start_server(platform_IP, platform_port)

do_continue = True

while do_continue:
    option = raw_input( 'Options:\n-q: quit\n-p: ping machine' )
    if option == 'q':
        do_continue = False
    elif option == 'p':
        ping_machine()
    else:
        print 'unknown option'
    
    


server_thread.join()

print 'Bye bye.'

    

