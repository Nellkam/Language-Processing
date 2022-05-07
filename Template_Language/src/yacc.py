import ply.yacc as yacc

from lex import tokens, literals

"""
Template : Elems

Elems : Elems Elem
      |

Elem : TEXT
     | Code

Code : Expression
     | Statement
     | Comment

Expression : OPEN ID CLOSE

Statement : For
          | If

For : OPEN FOR ID IN ID CLOSE Elems OPEN ENDFOR CLOSE

If : OPEN IF ID CLOSE

Comment : OPEN TEXT CLOSE
"""

def p_Template(p):
    "Template : Elems"
    p[0] = p[1]
    
def p_Elems_multiple(p):
    "Elems : Elems Elem"
    p[0] = p[1] + [p[2]]

def p_Elems_single(p):
    "Elems : "
    p[0] = []

def p_Elem_TEXT(p):
    "Elem : TEXT"
    p[0] = ('text', p[1])

def p_Elem_Code(p):
    "Elem : Code"
    p[0] = p[1]

def p_Code_Expression(p):
    "Code : Expression"
    p[0] = p[1]

def p_Expression_ID(p):
    "Expression : OPEN ID CLOSE"
    p[0] = ('variable', p[2])

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

while True:
    try:
        s = input('template > ')
    except EOFError:
        break
    if not s:
        continue
    result = parser.parse(s)
    print('ast:', result)
