import ply.lex as lex

reserved = {
    'for': 'FOR',
    'if': 'IF',
    'in': 'IN',
}

literals = ()

tokens = ['TEXT', 'ID', 'OPEN', 'CLOSE'] + list(reserved.values())

states = (
   ('code', 'exclusive'),
)

def t_code_ID(t):
    r'[a-zA-Z_]\w*'
    t.type = reserved.get(t.value, 'ID')    # Check for reserved words
    return t

def t_OPEN(t):
    r'{{'
    t.lexer.begin('code')
    return t

def t_code_CLOSE(t):
    r'}}'
    t.lexer.begin('INITIAL')
    return t

def t_TEXT(t):
    r'''(?s)    # Make the '.' special character match any character at all, including a newline
        .+?     # One or more characters, non-greedy
        (?=     # Positive lookahead assertion
          {%|   # Statements
          {{|   # Expressions
          {#|   # Comments
          \Z|$  # Matches only at the end of the string.
        )
    '''
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_code_ignore  = ' \t'

def t_ANY_error(t):
    print(f'Illegal character {t.value[0]}')
    t.lexer.skip(1)

lexer = lex.lex()

import readline

# while True:
#     try:
#         #s = input('template > ')
#         s = input()
#     except EOFError:
#         break
#     if not s:
#         continue
#     
#     lexer.input(s)   # Give input to lexer
#     while True:         # Tokenize
#         tok = lexer.token()
#         if not tok: 
#             break       # No more input
#         print(tok)
