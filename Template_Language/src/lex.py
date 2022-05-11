import ply.lex as lex

reserved = {
    'endfor': 'ENDFOR',
    'endif': 'ENDIF',
    'for': 'FOR',
    'if': 'IF',
    'in': 'IN',
    'is': 'IS',
}

literals = ('|', '.', '[', ']')

tokens = [
    'id',
    'int',
    'float',
    'str',
    'text',
    'ADD', 'SUB', 'MUL', 'DIV',
    'NE', 'EQ', 'GT', 'GE', 'LT', 'LE',
    'AND', 'OR', 'NOT',
    'OE', # Open  Expression {{
    'CE', # Close Expression }}
    'OS', # Open  Statement  {%
    'CS', # Close Statement  %}
    'OC', # Open  Comment    {#
    'CC', # Close Comment    #}
    ] + list(reserved.values())

states = (
   ('code', 'exclusive'),
   ('comment', 'exclusive'),
   ('raw', 'exclusive'),
)

t_code_ADD = '\+'
t_code_SUB = '-'
t_code_MUL = '\*'
t_code_DIV = '/'
t_code_EQ = '=='
t_code_NE = '!='
t_code_GT = '>'
t_code_GE = '>='
t_code_LT = '<'
t_code_LE = '<='
t_code_OR = 'or'
t_code_AND = 'and'
t_code_NOT = 'not'
t_code_int = r'\d(?:_?\d+)*'
t_code_float = r'\d(?:_?\d+)*\.\d+(?:e[+-]?\d+)?'

def t_raw(t): # ! maybe integrate into the code and make raw a reserved word
    r'{%\s*raw\s*%}'
    t.lexer.begin('raw')

def t_end_raw(t):
    r'{%\s*endraw\s*%}'
    t.lexer.begin('INITIAL')

def t_code_str(t): # ! lookahead/behind might not be the best way to go as it requeries ignoring quotes
    r'''(
          (?<=")                # Positive lookbehind for double quote
            (?:\\.|[^"\\])*     # Double quoted strings
          (?=")                 # Positive lookahead for double quote
        |
          (?<=')                # Positive lookbehind for double quote
            (?:\\.|[^"\\])*     # Single quoted strings
          (?=')                 # Positive lookbehind for double quote
        )
    '''
    return t

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

def t_INITIAL_raw_text(t):
    r'''(?s)        # Make the '.' special character match any character at all, including a newline
        .+?         # One or more characters, non-greedy
        (?=         # Positive lookahead assertion
          {{|       # Expressions
          {%|       # Statements
          {[#]|     # Comments
          \Z        # Matches only at the end of the string.
        )
    '''
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_code_ignore  = ' \t"\'' # ! Deal with " to fix lookahead/behind differently

def t_ANY_error(t):
    print(f'Illegal character {t.value[0]}')
    t.lexer.skip(1)

lexer = lex.lex()

# import readline
# 
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
