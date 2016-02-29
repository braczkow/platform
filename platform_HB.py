from threading import Thread
from time import sleep
import socket
import json

import platform_status

__HB_threads = []
__do_continue = True

def __is_json(data):
    try:
        json.loads(data)
        return True
    except:
        return False

def __HB_recv_worker(connection, client_address):
    global __do_continue
    while __do_continue:
        data = ''
        
        while not __is_json(data) and __do_continue:
            try:
                data += connection.recv(1)
            except socket.error, e:
                print 'HB no data available. sleep.'
                sleep(1)
        
        if __do_continue:
            print 'HB json data: ' + data
        
            message = json.loads(data)

            platform_status.on_machine_HB(message, client_address) 

        sleep(1)
    
    print 'HB finish recv_worker'
    connection.close()
                      
def __start_HB_recv_worker(connection, client_address):
    print "Starting platform_HB thread"
    HB_thread = Thread(target = __HB_recv_worker, args=[connection, client_address])
    HB_thread.start()
    return HB_thread


def __HB_server_worker(platform_IP, platform_port):
    print 'server_worker'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((platform_IP, platform_port))
    sock.listen(1)
    
    global __HB_threads
    global __do_continue

    while __do_continue:
        print 'wait for client'
        connection, client_address = sock.accept()
        print 'accepted from: ' + str(client_address)
        
        connection.setblocking(0)

        __HB_threads.append( __start_HB_recv_worker(connection, client_address) )

    for t in __HB_threads:
        t.join()
        

def start_HB_server(platform_IP, platform_port):
    print 'starting HB_server'
    server_thread = Thread(target = __HB_server_worker, args=[platform_IP, platform_port])
    server_thread.start()
    return server_thread

def stop_HB_server():
    print 'stop HB_server'
    global __do_continue
    __do_continue = False
    pass