import ply.yacc as yacc
from doingNothing_Lexer import tokens
from sys import exit
import socket

is_client = False
is_server = False
current_identifier = ""
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_conn, serv_caddr = (None, None)

def p_eval(p):
    '''
    eval : empty
         | connect_client
         | create_server
         | send_message
         | wait_response
         | wait_request
         | send_response
         | close
         | kill_connection
    '''

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

def p_connect_client(p):
    '''
    connect_client : CONNECT IDENTIFIER TO PORT COMMA IP_V4
                   | CONNECT IDENTIFIER TO LP PORT COMMA IP_V4 RP
    '''
    global is_client
    if not is_client and not is_server:
        is_client = True
        port = None
        ip = None
        global client

        try:
            port = p[5]
            ip = p[7]
        except:
            port = p[4]
            ip = p[6]

        try:
            print("Attempting to connect to: ", ip, port)
            global current_identifier
            current_identifier = p[2]
            global client
            client.connect((ip, port))
            print("Successfully connected to: ", ip, port)
        except:
            print("Error connecting to: ", ip, port)    
        
    else:
        print("Error connecting to server. "
            + "You can connect to a server only if you are not connected to a server already, "
            + "and you are not a server.")

def p_create_server(p):
    '''
    create_server : CREATE IDENTIFIER AT PORT COMMA IP_V4
                  | CREATE IDENTIFIER AT LP PORT COMMA IP_V4 RP
    '''
    global is_server
    if not is_client and not is_server:
        # Attempt to create server...
        global server
        port = None
        ip = None
        try:
            
            port = p[5]
            ip = p[7]
        except:
            port = p[4]
            ip = p[6]

        try:
            print("Attempting to bind @: ", ip, port)
            global current_identifier
            current_identifier = p[2]
            global server
            server.bind((ip, port))
            server.listen()
            global serv_conn
            global serv_caddr
            serv_conn, serv_caddr = server.accept()
            is_server = True
            print("Successfully binded to: ", ip, port)
        except:
            print("Error connecting to: ", ip, port)

    else:
        print("Error creating server. "
            + "You can create a server only if you do not have a server already, "
            + "and you are running a client.")

def p_send_message(p):
    '''
    send_message : SEND MESSAGE CONTENT
                 | SEND MESSAGE LP CONTENT RP
    '''
    if is_client and not is_server:
        message = None
        try:

            message = p[4]
        except:
            message = p[3]
        print("Sending message...")
        try:
            client.sendall(message)
            print("Message sent.")
        except:
            print("Unable to send message. Verify the connection.")

    else:
        print("Error sending message. You must be a client to send a message.")


def p_wait_response(p):
    '''
    wait_response : WAIT RESPONSE
    '''
    if is_client and not is_server:
        try:
            while True:
                data = client.recv(1024)
                if not data:
                    continue
                else:
                    print("Message from server: ", data)
                    break
        except:
            print("Unable to receive data.")

    else:
        print("Error waiting for response. You must be a client to access this resource.")

def p_wait_request(p):
    '''
    wait_request : WAIT REQUEST
    '''
    if not is_client and is_server:
        print("Waiting for data from client.")
        try:
            while True:
                data = server.recv(1024)
                if not data:
                    continue
                else:
                    print("Message received from client: ", data)
                    break
        except:
            print("Unable to receive message from client. Verify connection.")

    else:
        print("Error waiting for request. You must be a server to access this resource.")

def p_send_response(p):
    '''
    send_response : SEND RESPONSE MESSAGE CONTENT
                  | SEND RESPONSE MESSAGE LP CONTENT RP
    '''
    if not is_client and is_server:
        message = None
        try:
            message = p[5]
        except:
            message = p[4]

        try:
            print("Sending message to client.")
            server.sendall(message)
            print("Message sent.")
        except:
            print("Unable to send message to client.")

    else:
        print("Error sending request. You must be a server to access this resource.")

def p_close(p):
    '''
    close : EXIT
    '''
    print("Sayonara!")
    exit()

def p_kill_connection(p):
    '''
    kill_connection : KILL IDENTIFIER
    '''
    global current_identifier
    global is_client
    global is_server
    print("CHECK IT")
    if ((is_client and not is_server) or (not is_client and is_server)) and p[2] == current_identifier:
        current_identifier = ""
        is_client = False
        is_server = False
        client.close()
        server.close()
        print("Connection closed.")
    else:
        print("Unable to kill id: ", current_identifier)

def p_error(p):
    try:
        print("Error in: " + str(p.value))
    except:
        print("Unexpected Error. Please try again.")
    raise SyntaxError()

parser = yacc.yacc()

while True :
    try :
        line = input('DoingNothing !> ')
    except EOFError : break
    try:
        parser.parse(line.lower())
    except SyntaxError as e: print(e.msg)
