import ply.lex as lex

reserved = {
    'connect' : 'CONNECT', 
    'send' : 'SEND', 
    'wait' : 'WAIT', 
    'to' : 'TO',
    'response' : 'RESPONSE',
    'request' : 'REQUEST',
    'create' : 'CREATE',
    'message' : 'MESSAGE',
    'exit' : 'EXIT',
    'at' : 'AT',
    'kill' : 'KILL',
}

# List of token names.
tokens = [ 'IP_V4', 'PORT', 'LP', 'RP', 'COMMA', 'IDENTIFIER', 'CONTENT' ] + list(reserved.values())

def t_IP_V4(t):
    r'\b((([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\.)){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))\b'
    return t

def t_PORT(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Rule for left parenthesis.
t_LP = r'\('

# Rule for right parenthesis.
t_RP = r'\)'

# Rule for comma.
t_COMMA = r'\,'

def t_CONTENT(t):
    r'["][^\n]*["]'
    return t

def t_RESERVED_KEYWORDS(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    value = t.value.lower()
    if(reserved.get(value)):
        t.value = str(t.value)
        t.type = reserved.get(value, t.type)
    else:
        t.type = 'IDENTIFIER'
    return t

# Error handling.
def t_error(t):
    print("Oops! Try again!")
    print(t.value)
    t.lexer.skip(1)

# Ignore spaces.
t_ignore = r' '


# Build the lexer.
lexer = lex.lex()
# line = "abc123\"algas!\" AT 1992"
# lexer.input(line)
# while True:
#     token = lexer.token()
#     if not token:
#         break
#     print(token)