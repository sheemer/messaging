import sys
import socket
import threading
import rsa
from getpass4 import getpass
import os
import base64


os.system("clear || cls")
with open("picsnail", 'r') as login:
    sl = login.read()
print(sl)
print("snailchat")


publicKey, privateKey = rsa.newkeys(4096)

with open("pubkey_master.pem", "wb") as f:
    f.write(publicKey.save_pkcs1("PEM"))
    
    

    
def connect(conn):
    while True:
        received = conn.recv(1024)
        
        if received ==' ':
            pass
        else:
            decmess = rsa.decrypt(received, privateKey)
            msgde = str(decmess).replace("b'" , "")
            print(name1[:-1], msgde[:-1])

def sendMsg(conn):
    while True:
        send_msg = input().replace('b', '').encode()
        encMessage = rsa.encrypt(send_msg,clientkey)
        if send_msg == ' ':
            pass
        else:
            conn.send(encMessage)
                      
if __name__ == '__main__':
    password = getpass('Please enter chat password: ')
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", 12345))
    s.listen(5)
    print("Your Computer Name is:" + hostname)
    print("Your Computer IP Address is:" + IPAddr)
    print("Wait for a connection.")
    (conn, addr) = s.accept() 
    print ('Got connection from: ', addr)
    
    
    #Checking If passwords match.
    clientpws = conn.recv(1024)
    decodepws = base64.b64decode(clientpws).decode()
    if password == decodepws:
        print("Client password success. Happy chatting!")
        pass
    else: 
        print("Client password fail.")
        sys.exit() 
   
    
    
    #MASTER recieving the Client PUBKEY
    f = open("public_client.pem",'wb')
    l = conn.recv(1024)
    f.write(l)
    f.close()
     
    clientkey = rsa.PublicKey.load_pkcs1(l)
    
 #MASTER Sending the MASTER PUBKEY
    t = open("pubkey_master.pem",'rb')
    p = t.read(1024)
    conn.send(p)
    
    username =input("Please input your username:").replace("b'", '').encode()
    conn.send(username)
    
    name = conn.recv(1024)
    name1 = str(name).replace("b'" ,"" )
    
    
    
       
    thread1 = threading.Thread(target = connect, args = ([conn]))
    thread2 = threading.Thread(target = sendMsg, args = ([conn]))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
