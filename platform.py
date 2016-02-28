import socket
import platform_utils as pu

myIp = pu.get_ip_address('eth0')


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = (myIp, 8888)
print 'starting up on %s port %s' % server_address
sock.bind(server_address)

sock.listen(1)

while True:
    print 'waiting for a connection'
    connection, client_address = sock.accept()
    
    try:
        print 'connection from', client_address

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            print 'received "%s"' % data
            if data:
                print 'sending data back to the client'
                connection.sendall(data)
            else:
                print 'no more data from', client_address
                break
            
    finally:
        connection.close()