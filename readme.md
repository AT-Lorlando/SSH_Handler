# SSH Handler

## Description

## Server side

### Installation

### Configuration

## Client side

### Installation

### Configuration

## Discussion between server and client

The server is listening on port X for incoming connections. When a client etablish a connection, the server thread it and start the discussion. When we receive the OK message, we can start to send informations.

Steps :
<!-- - TLS handshake -->
- 1) Server send the OK message, the discussion is started
- 2) Client send his email address
- 3) Server look for the email address in the json file, if it's not found, the server send the error message and close the connection, else the server send the OK message and wait for the password.
- 4) Client send the password given by his password manager.
- 5) Server check the password, if it's not correct, the server send the error message and close the connection, else the server send the OK message and wait for the key.
- 6) Client generate a key pair and send the public key to the server.
- 7) Server write the public key in the json file, for populate it afterwhile, and send the OK message and close the connection.

### Checks to do

#### 2/3 Email address

- [ ] Check if the email address is valid

#### 4/5 Password

- [ ] Check if the password valid (format)
- [ ] Check if the email is in the json file, if not, send the error message and close the connection
- [ ] Check if the password is correct (compare with the json file), if not, send the error message and close the connection

- [ ] Check if the email already have a public key, if yes, ask to the user if he want to replace it.

I moved those two last checks to the fourth step, because the error message can help a potential attacker to know if the email address is valid or not.

#### 6/7 Public key

- [ ] Check if the public key is valid

