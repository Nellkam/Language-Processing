import ply.yacc as yacc
from run import run
import sys

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

RExp : Exp LT Exp
     | Exp LE Exp
     | Exp GT Exp
     | Exp GE Exp
     | Exp EQ Exp
     | Exp NE Exp

AExp : Exp ADD Exp
     | Exp SUB Exp
     | Exp MUL Exp
     | Exp DIV Exp

OExp : Exp IN Exp
     | Exp IS Exp
     | Exp NOTIN Exp
     | Exp ISNOT Exp
     | Exp '[' Exp ']'
     | Exp '.' id
     | Exp '|' id

"""

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'NOT'),
    ('nonassoc', 'EQ', 'NE', 'GT', 'GE', 'LT', 'LE', 'IS', 'IN', 'ISNOT', 'NOTIN'),  # Nonassociative operators
    ('left', 'ADD', 'SUB'),
    ('left', 'MUL', 'DIV'),
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

def p_Code_Comment(p): # ! Should comments be ignored here or in the lexer?
    "Code : Comment"
    p[0] = p[1]

def p_Expression(p):
    "Expression : OE Exp CE"
    p[0] = ('print', (p[2]))

def p_Statement_if(p):
    "Statement : If"
    p[0] = p[1]

def p_Statement_for(p):
    "Statement : For"
    p[0] = p[1]

def p_If(p):
    "If : OS IF Exp CS Elems OS ENDIF CS"
    p[0] = ('if', p[3], p[5])

def p_For(p):
    "For : OS FOR id IN id CS Elems OS ENDFOR CS"
    p[0] = ('for', p[3], p[5], p[7])

def p_Exp_id(p):
    "Exp : id"
    p[0] = ('variable', p[1])

def p_Exp_Literal(p):
    "Exp : Literal"
    p[0] = p[1]

def p_Exp_AExp(p):
    "Exp : AExp"
    p[0] = p[1]

def p_Exp_RExp(p):
    "Exp : RExp"
    p[0] = p[1]

def p_Exp_LExp(p):
    "Exp : LExp"
    p[0] = p[1]

def p_Exp_OExp(p):
    "Exp : OExp"
    p[0] = p[1]

def p_Exp_braces(p):
    "Exp : '(' Exp ')'"
    p[0] = p[2]

def p_Literal_str(p):
    "Literal : str"
    p[0] = ('text', p[1])

def p_Literal_Num(p):
    "Literal : Num"
    p[0] = p[1]

def p_Literal_Bool(p):
    "Literal : Bool"
    p[0] = p[1]

def p_Num_int(p):
    "Num : int"
    p[0] = ('int', p[1])

def p_Num_float(p):
    "Num : float"
    p[0] = ('float', p[1])

def p_Bool_TRUE(p):
    "Bool : TRUE"
    p[0] = ('bool', p[1])

def p_Bool_FALSE(p):
    "Bool : FALSE"
    p[0] = ('bool', p[1])

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

def p_RExp_IS(p):
    "RExp : Exp IS id"
    p[0] = ('is', p[1], p[3])

def p_RExp_IS_NOT(p):
    "RExp : Exp ISNOT id"
    p[0] = ('isnot', p[1], p[3])

def p_RExp_IN(p):
    "RExp : Exp IN Exp"
    p[0] = ('in', p[1], p[3])

def p_RExp_NOT_IN(p):
    "RExp : Exp NOTIN Exp"
    p[0] = ('notin', p[1], p[3])

def p_LExp_NOT(p):
    "LExp : NOT Exp"
    p[0] = ('not', p[2])

def p_LExp_AND(p):
    "LExp : Exp AND Exp"
    p[0] = ('and', p[1], p[3])

def p_LExp_OR(p):
    "LExp : Exp OR Exp"
    p[0] = ('or', p[1], p[3])

def p_OExp_filter(p):
    "OExp : Exp PIPE id"
    p[0] = ('filter', p[1], p[3])

def p_OExp_method(p):
    "OExp : Exp DOT id '(' ')'"
    p[0] = ('method', p[1], p[3])

def p_OExp_attr(p):
    "OExp : Exp DOT id"
    p[0] = ('attr', p[1], p[3])

def p_OExp_item(p):
    "OExp : Exp '[' Exp ']'"
    p[0] = ('item', p[1], p[3])

def p_Comment(p): # ! Should comments be ignored here or in the lexer?
    "Comment : OC text CC"
    p[0] = '',

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!", p)

# Build the parser
parser = yacc.yacc()

def main(argv):
    import readline

    while True:
        try:
            s = input('template > ')
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)

        class MyClass:
            x = 5

        p1 = MyClass()

        d = {
            'a': [2,1,3],
            'b': "abc",
            'c': {'foo': 42, 'bar': 73},
            'd': 42,
            'e': p1,
        }

        print('dict:', d)
        print('ast:', result)
        print(run(result, d))


if __name__ == "__main__":
    sys.exit(main(sys.argv))