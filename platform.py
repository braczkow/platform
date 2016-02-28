import socket

platform_IP = '192.168.1.68'

print 'platform_IP: ' + platform_IP

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'socket created.'

sock.bind((platform_IP, 8888))
print 'socket bound'

sock.listen(1)
print 'socket listen.'

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
