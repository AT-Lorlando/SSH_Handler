# A socket to connect to localhost:4242 and send the password

import socket
import rsa
import os

ClientMultiSocket = socket.socket()
HOST = '127.0.0.1'
PORT = 4242

def receiveFromServer():
    """
        Receive a message from the client.
        Args:
            connection: (socket) The connection with the client
        Returns:
            The message received from the client
    """
    data = ClientMultiSocket.recv(2048)
    if not data:
        # raise Exception('No data received')
        ClientMultiSocket.close()
        return ""
    else:
        return data.decode('utf-8')

def sendToServer(message):
    """
        Send a message to the client.
        Args:
            connection: (socket) The connection with the client
        Returns:
            The message to send to the client.
    """
    ClientMultiSocket.send(str.encode(message))

def generateKey():
    """
        Generate a RSA key pair to send to the server.
        Args: 
            None
        Returns:
            The generated key
    """
    (pubkey, privkey) = rsa.newkeys(512)
    # Write those keys to a file
    
    with open('public.pem', 'w+') as f:
        f.write(pubkey.save_pkcs1().decode('utf-8'))
    with open('private.pem', 'w+') as f:
        f.write(privkey.save_pkcs1().decode('utf-8'))
    
    print("Public key: ", pubkey.save_pkcs1().decode('utf-8'))
    
    # Make the pubkey to a ssh key
    pubkey = pubkey.save_pkcs1().decode('utf-8')
    pubkey = pubkey.replace('-----BEGIN RSA PUBLIC KEY-----', '')
    pubkey = pubkey.replace('-----END RSA PUBLIC KEY-----', '')
    pubkey = pubkey.replace('\n', '')

    print("Public key:", pubkey)    
    # Get the user name
    username = os.getlogin()
    # get the hostname of the machine
    hostname = os.uname()[1]
    print("Username:", username)
    print("Hostname:", hostname)
    
    pubkey = 'ssh-rsa ' + pubkey + ' ' + username + '@' + hostname
    print("Public key:", pubkey)    

    return pubkey
    
generateKey()
exit()
print('Waiting for connection response')

try:
    ClientMultiSocket.connect((HOST, PORT))
except socket.error as e:
    print(str(e))

res = receiveFromServer()
if res.startswith('#00'):
    print('Connection successful')
else:
    print('Connection failed')
    exit(1)

while True:
    res = receiveFromServer()
    # if res start with #09, it's an error code, print it and exit
    if res.startswith('#09'):
        print(res)
        exit(1)
    # If res start with #01, it's a message from the server, just print it
    print(res)
    # If res start with #02, it's a message from the server, asking for an input, ask for an input and send it
    if res.startswith('#02'):
        input_asked = res.split(': ')[1]
        i = input('Please enter ' + input_asked + ': ')
        sendToServer(i)
    # If res start with #03, it's a message from the server, asking for generate the key, generate it and send it.
    if res.startswith('#03'):
        key = generateKey()
        sendToServer(key)
    

# # Send the password
# email = input('Email: ')

# ClientMultiSocket.send(str.encode(email))

# res = ClientMultiSocket.recv(1024)

# print(res.decode('utf-8'))
    
# # Send my ID and my email
# ID = input('ID: ')
# email = input('Email: ')

# ClientMultiSocket.send(str.encode('{ID: ' + ID + ', email: ' + email + '}'))
    
# ClientMultiSocket.close()