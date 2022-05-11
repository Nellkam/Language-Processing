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

Expression : OE str CE
           | OE id Ops CE

Ops : Ops Op
    |

Op : '|' id      # Filter
   | '[' str ']'  # Item
   | '.' id      # Attribute

Statement : For
          | If

Filters : Filters '|' id
        |

Attributes : Attributes '.' id
           |

For : OS FOR id IN id CS Elems OS ENDFOR CS

If : OS IF id CS Elems OS ENDIF CS
   | OS IF id IS id CD Elems OS ENDIF CS

Comment : OC text CC

Exp : id
    | Literal
    | AExp
    | RExp
    | LExp
    | '(' Exp ')'

Literal : str
        | Num
        | Bool
        | List   # '[' List ']'
        | Tuple  # '(' List ')'
        | Dict

Num : int
    | float

Bool : TRUE
     | FALSE

List : '[' List1 ']'

List1 : List1 ',' Exp
      | Exp
      | # fix this

Tuple : '[' Tuple1 ']'

Tuple1 : Tuple1 ',' Exp
       | Exp
       | # fix this

Dict : '{' Dict1 '}'

Dict1 : Dict1 ',' Key ':' Value
      | Key ':' Value

Key : str
    | Num
    | Tuple

LExp : Exp OR  Exp
     | Exp AND Exp
     | NOT Exp

RExp : Exp LOWER         Exp
     | Exp LOWERQUALS    Exp
     | Exp GREATER       Exp
     | Exp GREATEREQUALS Exp
     | Exp EQUALS        Exp
     | Exp NOTEQUALS     Exp

AExp : Exp ADD Exp
     | Exp SUB Exp
     | Exp MUL Exp
     | Exp DIV Exp

OExp : Exp IN Exp
     | Exp IS Exp
     | Exp '[' Exp ']'
     | Exp '.' Exp

"""

precedence = (
    ('left', 'ADD', 'SUB'),
    ('left', 'MUL', 'DIV'),
    ('nonassoc', 'EQ', 'NE', 'GT', 'GE', 'LT', 'LE'),  # Nonassociative operators
    ('left', 'NOT'),
    ('left', 'OR'),
    ('left', 'AND'),
)

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
    "Expression : OE Exp CE"
    p[0] = ('print', (p[2]))

# def p_Expression_id(p):
#     "Expression : OE id Ops CE"
#     p[0] = ('variable', p[2], p[3])

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
    p[0] = ('item', p[2])

def p_Op_Item_int(p):
    "Op : '[' int ']'"
    p[0] = ('item', int(p[2])) # ! Probably remove cast

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
    "If : OS IF Exp CS Elems OS ENDIF CS"
    p[0] = ('if', p[3], p[5])

def p_If_is(p):
   "If : OS IF id IS id CS Elems OS ENDIF CS"
   p[0] = ('ifis', p[3], p[5], p[7])

def p_For(p):
    "For : OS FOR id IN id CS Elems OS ENDFOR CS"
    p[0] = ('for', p[3], p[5], p[7])

def p_Exp_id(p):
    "Exp : id"
    p[0] = ('variable', p[1], [])

def p_Exp_Literal(p):
    "Exp : Literal"
    p[0] = p[1]

def p_Literal_str(p):
    "Literal : str"
    p[0] = ('text', p[1])

def p_Literal_Num(p):
    "Literal : Num"
    p[0] = p[1]

def p_Exp_AExp(p):
    "Exp : AExp"
    p[0] = p[1]

def p_Exp_RExp(p):
    "Exp : RExp"
    p[0] = p[1]

def p_Exp_braces(p):
    "Exp : '(' Exp ')'"
    p[0] = p[2]

def p_Num_int(p):
    "Num : int"
    p[0] = ('int', p[1])

def p_Num_float(p):
    "Num : float"
    p[0] = ('float', p[1])

def p_AExp_ADD(p):
    "AExp : Exp ADD Exp"
    p[0] = ('+', p[1], p[3])

def p_AExp_SUB(p):
    "AExp : Exp SUB Exp"
    p[0] = ('-', p[1], p[3])

def p_AExp_MUL(p):
    "AExp : Exp MUL Exp"
    p[0] = ('*', p[1], p[3])

def p_AExp_DIV(p):
    "AExp : Exp DIV Exp"
    p[0] = ('/', p[1], p[3])

def p_RExp_EQ(p):
    "RExp : Exp EQ Exp"
    p[0] = ('==', p[1], p[3])

def p_RExp_NEQ(p):
    "RExp : Exp NE Exp"
    p[0] = ('!=', p[1], p[3])

def p_RExp_GT(p):
    "RExp : Exp GT Exp"
    p[0] = ('>', p[1], p[3])

def p_RExp_GE(p):
    "RExp : Exp GE Exp"
    p[0] = ('>=', p[1], p[3])

def p_RExp_LT(p):
    "RExp : Exp LT Exp" 
    p[0] = ('<', p[1], p[3])

def p_RExp_LE(p):
    "RExp : Exp LE Exp"
    p[0] = ('<=', p[1], p[3])

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

    d = {
        'a': [2,1,3],
        'b': "abc",
        'c': {'foo': 42, 'bar': 73},
        'd': 42,
    }

    print('ast:', result)
    print('dict:', d)
    print(run(result, d))

# def p_Exp_LExp(p):
#     "Exp : LExp"
#     p[0] = ''
# 
# def p_LExp_OR(p):
#     "LExp : Exp OR Exp"
#     p[0] = ''
# 
# def p_LExp_AND(p):
#     "LExp : Exp AND Exp"
#     p[0] = ''
# 
# def p_LExp_NOT(p):
#     "LExp : NOT Exp"
#     p[0] = ''