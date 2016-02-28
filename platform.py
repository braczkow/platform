import socket
import platform_utils as pu
from threading import Thread
from time import sleep

HB_threads = []

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
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((platform_IP, platform_port))
    sock.listen(1)
    
    while True:
        print 'wait for client'
        connection, client_address = sock.accept()
        
        global HB_threads
        HB_threads.append( start_platform_HB(connection) )
        

def start_server(platform_IP, platform_port):
    print 'starting server'
    server_thread = Thread(target = server_worker, args=[platform_IP, platform_port])
    server_thread.start()
    return server_thread


platform_IP = pu.get_ip_address('eth0')
platform_port = 8888

print 'IP: ' + platform_IP

server_thread = start_server(platform_IP, platform_port)

server_thread.join()

print 'Bye bye.'

    

