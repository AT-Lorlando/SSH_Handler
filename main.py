# A server listening on port 4242, where i must send a password to discuss with the server

import socket
from _thread import *
import os
import json
import re

# JSON file hierarchy
# {
#     "id": {
#         "email": "email",
#         "password": "pw",
#         "public_key": "pk"
#     }
# }

HOST = '127.0.0.1'
PORT = 4242
FILENAME = 'data.json' 
connections = []
ThreadCount = 0
ServerSideSocket = socket.socket()

try:
    ServerSideSocket.bind((HOST, PORT))
except socket.error as e:
    print(str(e))
    
print('Socket is listening..')

ServerSideSocket.listen(5)

# OS FUNCTIONS #

def WriteInFile(id, field, value):
    """
        Write in the JSON file a given value in a given field for a given id.
        Args: 
            id: (int) The id of the user you want to modify
            field: (string) The field you want to write
            value: (string) The value you want to write
    """
    with open(FILENAME, 'r') as f:
        json_object = json.load(f)
        
        if id in json_object:
            json_object[id][field] = value
        else:
            json_object[id] = {field: value}
        
    with open(FILENAME, 'w') as f:
        f.write(json.dumps(json_object, indent=4))

# SOCKET FUNCTIONS #    
    
def sendToClient(connection, message):
    """
        Send a message to the client.
        Args:
            connection: (socket) The connection with the client
        Returns:
            The message to send to the client.
    """
    connection.send(str.encode(message))

def receiveFromClient(connection):
    """
        Receive a message from the client.
        Args:
            connection: (socket) The connection with the client
        Returns:
            The message received from the client
    """
    data = connection.recv(2048)
    if not data:
        sendToClient(connection, 'No data, please try again')
        raise Exception('No data received')
        return ""
    else:
        return data.decode('utf-8')

def askForInput(connection, asked_input = ''):
    """
        Ask the client to send a message to the server.
        Args: 
            connection: (socket) The connection with the client
        Returns:
            The message received from the client
    """
    sendToClient(connection, '#02 afi: ' + asked_input)
    return receiveFromClient(connection)

# VALIDATOR FUNCTIONS #

def ValidateEmail(email):
    """
        Validate an email.
        Args: 
            email: (string) The email you want to validate
        Returns:
            True if the email is valid, False otherwise
    """
    if '@' in email and '.' in email:
        print('Email is valid.')
        return True
    else:
        print('Error: Email isn\'t valid.')
        return False

def EmailValidator(connection, email):
    """
        Validate an email and send the response to the client.
        Args: 
            connection: (socket) The connection with the client
            email: (string) The email you want to validate
    """
    sendToClient(connection, 'Validating email...')
    if not ValidateEmail(email):
        sendToClient(connection, '#09 Email is invalid, please check your email or contact the administrator.')
        print('Email validation failed.')
        return False
    else:
        print('Email validation success.')
        return True

def ValidatePassword(password):
    """
        Validate the password. (must contains only a-z, A-Z, 0-9, #,$,!,&)
        Args:
            password: (string) The password you want to validate
        Returns:
            True if the password is valid, False otherwise
    """
    if re.match('^[a-zA-Z0-9#,$,!,&]+$', password):
        print('Password is valid')
        return True
    else:
        print('Error: Password isn\'t valid.')
        return False

def CheckEmailInJSON(email):
    """
        Check if an email is in the JSON file.
        Args: 
            email: (string) The email you want to check
        Returns:
            True if the email is in the JSON file, False otherwise
    """
    with open(FILENAME, 'r') as f:
        json_object = json.load(f)
        
        for id in json_object:
            if email == json_object[id]['email']:
                print('Email is in json')
                return True
    print('Error: Email isn\'t in json')
    return False

def CheckPasswordForID(id, password):
    """
        Check if a password is the good one for a given id.
        Args: 
            id: (int) The id of the user you want to check
            password: (string) The password you want to check
        Returns:
            True if the password is the good one, False otherwise
    """
    with open(FILENAME, 'r') as f:
        json_object = json.load(f)
        
        if id in json_object:
            if password == json_object[id]['password']:
                print('Password is correct')
                return True
    print('Error: Password is incorrect for' + email)
    return False

def CheckPasswordForEmail(email, password):
    """
        Check if a password is the good one for a given email.
        Args: 
            email: (string) The email you want to check
            password: (string) The password you want to check
        Returns:
            True if the password is the good one, False otherwise
    """
    with open(FILENAME, 'r') as f:
        json_object = json.load(f)
        
        for id in json_object:
            if email == json_object[id]['email'] and password == json_object[id]['password']:
                print('Password is correct')
                return True
    print('Error: Password is incorrect for' + email)
    return False

def PasswordValidator(connection, email, password):
    """
        Validate the password step and send the response to the client.
            Checks are ValidatePassword, CheckEmailInJSON, CheckPasswordForID
        Args: 
            connection: (socket) The connection with the client
            email: (string) The email you want to validate
            password: (string) The password you want to validate
    """
    sendToClient(connection, 'Validating password...')
    if not ValidatePassword(password):
        sendToClient(connection, '#09 Password is invalid, please check your password or contact the administrator')
        return False
    elif not CheckEmailInJSON(email):
        sendToClient(connection, '#09 An error occured, please check your credentials or contact the administrator')
        return False
    elif not CheckPasswordForEmail(email, password):
        sendToClient(connection, '#09 An error occured, please check your credentials or contact the administrator')
        return False
    else:
        sendToClient(connection, '#01 Credentials are valid, you can now send your public key')
        return True

def CheckEmailPK(email):
    """
        Check if an email already has a public key.
        Args: 
            email: (string) The email you want to check
        Returns:
            True if the email hasn't a public key, False otherwise
    """
    with open(FILENAME, 'r') as f:
        json_object = json.load(f)
        
        for id in json_object:
            if email == json_object[id]['email'] and not json_object[id]['public_key']:
                return True
    return False
    
# THREAD FUNCTIONS #

def multi_threaded_client(connection, thread):
    print('Connected to: ' + address[0] + ':' + str(address[1]) + ' with thread ' + str(thread))
    
    # Start the discussion with the client #
    connection.send(str.encode('#00 Server is working:'))
    
    # Step 1: Receive the email #
    print(str(thread) + ': Waiting for email...')
    try:
        email = askForInput(connection, 'Email')
    except Exception as e:
        print(e)
        connection.close()
        print(str(thread) + ': ' + e)
        return
            
    # Step 2: Validate the email #
    print(str(thread) + ': Validating the email (' + email + ')')
    if not EmailValidator(connection, email):
        print(str(thread) + ": Email is invalid, closing the connection...")
        connection.close()
        return
    print(str(thread) + ': Email is valid.')
        
    
    # Step 3: Receive the password #
    print(str(thread) + ': Waiting for password...')
    try:
        password = askForInput(connection, 'Password')
    except Exception as e:
        print(e)
        connection.close()
        print(str(thread) + ': ' + e)
        return
    
    # Step 4: Validate the password #
    print(str(thread) + ': Validating the password (' + password + ')')
    if not PasswordValidator(connection, email, password):
        print(str(thread) + ": Password is invalid, closing the connection...")
        connection.close()
        return
    print(str(thread) + ': Password is valid.')
        
    
    connection.close()
    return
    
    # if not data:
    #     connection.close()
    
    # print('Receive: ',data)
    
    # # Validate the password 
    # if(not ValidatePassword(data)):
    #     sendToClient(connection, 'Password is invalid')
    #     connection.close()
    # response = 'Password is valid, you can now send your identifier'
    # sendToClient(connection, response)
    
    # data = receiveFromClient(connection)
    # print('Receive: ',data)
    
    
    
    # connection.close()
    

while True:
    Client, address = ServerSideSocket.accept()
    ThreadCount += 1
    connections.append({'connection': Client, 'address': address, 'thread': ThreadCount})
    start_new_thread(multi_threaded_client, (Client, ThreadCount,))
    print('Thread Number: ' + str(ThreadCount))
    
ServerSideSocket.close()

