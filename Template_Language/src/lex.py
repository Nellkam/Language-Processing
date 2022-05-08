import ply.lex as lex

reserved = {
    'endfor': 'ENDFOR',
    'endif': 'ENDIF',
    'for': 'FOR',
    'if': 'IF',
    'in': 'IN',
}

literals = ('|',)

tokens = [
    'id',
    'text',
    'OE', # Open Expression tag
    'CE', # Close Expression tag
    'OS', # Open Statement tag
    'CS', # Close Statement tag
    'OC', # Open Comment tag
    'CC', # Close Comment tag
    ] + list(reserved.values())

states = (
   ('code', 'exclusive'),
   ('comment', 'exclusive'),
)

def t_code_id(t):
    r'[a-zA-Z_]\w*'
    t.type = reserved.get(t.value, 'id')    # Check for reserved words
    return t

def t_OE(t):
    r'{{'
    t.lexer.begin('code')
    return t

def t_OS(t):
    r'{%'
    t.lexer.begin('code')
    return t

def t_OC(t):
    r'{[#]'
    t.lexer.begin('comment')
    return t

def t_code_CE(t):
    r'}}'
    t.lexer.begin('INITIAL')
    return t

def t_code_CS(t):
    r'%}'
    t.lexer.begin('INITIAL')
    return t

def t_comment_CC(t): # ! Just ignore comments?
    r'[#]}'
    t.lexer.begin('INITIAL')
    return t

def t_comment_text(t):
    r'''(?s)        # Make the '.' special character match any character at all, including a newline
        .+?         # One or more characters, non-greedy
        (?=[#]})    # Positive lookahead assertion
    '''
    return t

def t_text(t):
    r'''(?s)    # Make the '.' special character match any character at all, including a newline
        .+?     # One or more characters, non-greedy
        (?=     # Positive lookahead assertion
          {{|   # Expressions
          {%|   # Statements
          {[#]| # Comments
          \Z    # Matches only at the end of the string.
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

while True:
    try:
        #s = input('template > ')
        s = input()
    except EOFError:
        break
    if not s:
        continue
    
    lexer.input(s)   # Give input to lexer
    while True:         # Tokenize
        tok = lexer.token()
        if not tok: 
            break       # No more input
        print(tok)
