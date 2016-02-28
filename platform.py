import socket
import platform_utils as pu

platform_IP = pu.get_ip_address('eth0')

print 'platform_IP: ' + platform_IP

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(platform_IP, 8888)

sock.listen(1)

while True:
    print 'wait for client'
    connection, client_address = sock.accept()
    
    try:
        print 'connection from', client_address

        while True:
            data = connection.recv(16)
            print 'received: ' + data
            if data:
                pass
            else:
                print 'no data', client_address
                break
            
    finally:
        connection.close()
