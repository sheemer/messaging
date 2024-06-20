import sys
import socket
import threading

import rsa  

# Need security

publickey, privateKey = rsa.newkeys(512)
print(publickey)

with open("public_client.pem", "wb") as f:
    f.write(publickey.save_pkcs1("PEM"))
    
with open("public_client.pem", "rb") as file:
    content = file.read()
    print(content)
    

#with open("public_server.pem", "rb") as f:
#    public_key_server = rsa.PublicKey.load_pkcs1(f.read())

#TODO:end connection with 'exit'
def connect(s):
    while True:
        r_msg = s.recv(1024)
        decmess = rsa.decrypt(r_msg,privateKey)

        if not r_msg:
            break
        if r_msg == '':
            pass
        else:
            print(decmess)


def receive(s):
    while True:
        s_msg = input().replace('b','').encode()
        #encMessage = rsa.encrypt(s_msg.encode(),publickey)
        if s_msg == '':
            pass
        #if s_msg.decode() == 'exit':
         #   print("wan exit")
         #   break
        else:
            s.send(s_msg)

if __name__ == '__main__':

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((sys.argv[1], int(sys.argv[2])))
    # not working
    #file = open("public_client.pem" , "rb")
    f = open('public_client.pem','rb')
    print('Sending...')
    l = f.read(1024)
    print(l)
    s.send(l)
    
    
    #--------------------------------------------------------------------------
    thread1 = threading.Thread(target = connect, args = ([s]))
    thread2 = threading.Thread(target = receive, args = ([s]))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()