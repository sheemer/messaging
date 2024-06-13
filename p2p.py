import sys
import socket
import threading
import rsa


#Need security
publicKey, privateKey = rsa.newkeys(512)

#TODO: exit program when client ends the connection
def connect(conn):
    while True:
        received = conn.recv(1024)
        decmess = rsa.decrypt(received.decode(),privateKey)
        if received ==' ':
            pass
        if received == '-----BEGIN RSA PUBLIC KEY-----':
            
        #Not working
            #-----------------------------------------------
        else:
            print("Sender:",decmess)

def sendMsg(conn):
    while True:
        send_msg = input().replace('b', '')
        encMessage = rsa.encrypt(send_msg.encode(),publicKey)
        if send_msg == ' ':
            pass
        else:
            conn.sendall(encMessage)

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('192.168.1.248', 12345))
    s.listen(5)
    (conn, addr) = s.accept() 
    print ('Got connection from', addr)
    thread1 = threading.Thread(target = connect, args = ([conn]))
    thread2 = threading.Thread(target = sendMsg, args = ([conn]))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()