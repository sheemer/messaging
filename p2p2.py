import sys
import socket
import threading
from getpass import getpass
import rsa  
import os
import base64 

os.system("clear || cls")

with open("picsnail", 'r') as login:
    sl = login.read()
print(sl)
print("snailchat")



publickey, privateKey = rsa.newkeys(512)


with open("public_client.pem", "wb") as f:
    f.write(publickey.save_pkcs1("PEM"))
    
with open("public_client.pem", "rb") as file:
    content = file.read()
    

  
def connect(s):
    while True:
        r_msg = s.recv(1024)
        decmess = rsa.decrypt(r_msg,privateKey)

        if not r_msg:
            break
        if r_msg == '':
            pass
        else:
            msgde = str(decmess).replace("b'" , "")
            print(name1[:-1], msgde[:-1])


def receive(s):
    while True:
        s_msg = input().replace('b','').encode()
        encMessage = rsa.encrypt(s_msg, masterkeypub)
        if s_msg == '':
            pass
        else:
            s.send(encMessage)

if __name__ == '__main__':
   
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((sys.argv[1], int(sys.argv[2])))
    
    #Password to send to the server.
    
    password = getpass("Please enter chat password:  ").encode()
    codedpass = base64.b64encode(password)
    s.send(codedpass)
    
   
   
   #Client sending PUBKEY
    f = open('public_client.pem','rb')
    l = f.read(1024)
    s.send(l)
    

    
    #Client recieving the MASTERPUBKEY
    t = open("pubkey_master.pem",'wb')
    p = s.recv(1024)
    t.write(p)
    t.close() 
    masterkeypub = rsa.PublicKey.load_pkcs1(p)

    
    username =input("Please input your username:").replace("b'", '').encode()
    s.send(username)
    name = s.recv(1024)
    name1 = str(name).replace("b'", '')
       
    
    print("Connection to office successful. Safe sending!")
    #--------------------------------------------------------------------------
    thread1 = threading.Thread(target = connect, args = ([s]))
    thread2 = threading.Thread(target = receive, args = ([s]))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()