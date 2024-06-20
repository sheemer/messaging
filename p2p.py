import sys
import socket
import threading
import rsa
import re

#Need security
publicKey, privateKey = rsa.newkeys(512)

with open("pubkey_master.pem", "wb") as f:
    f.write(publicKey.save_pkcs1("PEM"))
    

#TODO: exit program when client ends the connection
def connect(conn):
    while True:
        received = conn.recv(1024)
        
        if received ==' ':
            pass
       # elif 'BEGIN RSA PUBLIC KEY' in str(received):
        #    with open("public_client.pem", "wb") as f:
                 #clientpublicKey = rsa.PublicKey.save_pkcs1('PEM')(received, f.write)
         #       f.write(str(received).replace('b', "" ))
                 
          #  with open("public_client.pem", "rb") as file:
            #    content = file.read().decode()
           #     tim = print(content.encode())
                
    
            #with open("public_client.pem", "wb") as f:
            #  f.write(tim.save_pkcs1("PEM"))
    
        #Not working
            #-----------------------------------------------
        else:
            decmess = rsa.decrypt(received.decode(), clientkey)
            print(decmess)

def sendMsg(conn):
    while True:
        send_msg = input().replace('b', '').encode()
        encMessage = rsa.encrypt(send_msg,clientkey)
        if send_msg == ' ':
            pass
        else:
            conn.send(encMessage)

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('192.168.1.248', 12345))
    s.listen(5)
    (conn, addr) = s.accept() 
    
    
    print ('Got connection from', addr)
    f = open("public_client.pem",'wb')

    l = conn.recv(1024)
    
    f.write(l)
    f.close() 
    clientkey = rsa.PublicKey.load_pkcs1(l)
       
    thread1 = threading.Thread(target = connect, args = ([conn]))
    thread2 = threading.Thread(target = sendMsg, args = ([conn]))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()