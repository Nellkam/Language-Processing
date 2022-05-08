import ply.yacc as yacc
from run import run

from lex import tokens, literals

"""
Template : Elems

Elems : Elems Elem
      |

Elem : text
     | Code

Code : Expression
     | Statement
     | Comment

Expression : OE id Filters CE
           | OE id Attributes CE

Expression : OE id Ops CE

Ops : Ops Op
    |

Op : '|' Filter
   | '[' Item ']'
   | '.' Attribute

Statement : For
          | If

Filters : Filters '|' id
        |

Attributes : Attributes '.' id
           |

For : OS FOR id IN id CS Elems OS ENDFOR CS

If : OS IF id CS Elems OS ENDIF CS

Comment : OC text CC

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
    "Elem : text"
    p[0] = ('text', p[1])

def p_Elem_Code(p):
    "Elem : Code"
    p[0] = p[1]

def p_Code_Expression(p):
    "Code : Expression"
    p[0] = p[1]

def p_Code_Statement(p):
    "Code : Statement"
    p[0] = p[1]

# ! Should comments be ignored here or in the lexer?
def p_Code_Comment(p):
    "Code : Comment"
    p[0] = p[1]

def p_Expression(p):
    "Expression : OE id Ops CE"
    p[0] = ('variable', p[2], p[3])

def p_Ops_multiple(p):
    "Ops : Ops Op"
    p[0] = p[1] + [p[2]]

def p_Ops_empty(p):
    "Ops : "
    p[0] = []

def p_Op_Filter(p):
    "Op : '|' id"
    p[0] = ('filter', p[2])

def p_Op_Item_str(p):
    "Op : '[' str ']'"
    p[0] = ('item', p[2][1:][:-1])

def p_Op_Item_int(p):
    "Op : '[' int ']'"
    p[0] = ('item', int(p[2]))

def p_Op_Attr(p):
    "Op : '.' id"
    p[0] = ('attr', p[2])

def p_Statement_if(p):
    "Statement : If"
    p[0] = p[1]

def p_Statement_for(p):
    "Statement : For"
    p[0] = p[1]

def p_If(p):
    "If : OS IF id CS Elems OS ENDIF CS"
    p[0] = ('if', p[3], p[5])

def p_For(p):
    "For : OS FOR id IN id CS Elems OS ENDFOR CS"
    p[0] = ('for', p[3], p[5], p[7])

# ! Should comments be ignored here or in the lexer?
def p_Comment(p):
    "Comment : OC text CC"
    p[0] = '',

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

import readline

while True:
    try:
        s = input('template > ')
    except EOFError:
        break
    if not s:
        continue
    result = parser.parse(s)
    print('ast:', result)

    # d = {
    #     'a': [2,1,3],
    #     'b': "abc",
    #     'c': {'foo': 42, 'bar': 73},
    #     'd': 42,
    # }
    # print(d)
    # run(result, d)
