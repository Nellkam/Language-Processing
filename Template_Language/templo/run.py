import builtins
import operator
import typing as t
from tests import TESTS


def run(ast, dic):
    out = ""
    for x in ast:
        match x[0]:
            case "text":
                out += x[1]
            case "print":
                # ! Should x[1] be a singleton or should something be restructured?
                out += str(run([x[1]], dic))  
            case "if":
                for cond, elems in x[1]:
                    if run([cond], dic):
                        out += run(elems, dic)
                        break
            case "for":
                for a in dic[x[2]]:
                    dic[x[1]] = a
                    out += run(x[3], dic)
            case "repeat":
                for _ in range(run([x[1]], dic)):
                    out += run(x[2], dic)
            case "int":
                out = int(x[1])
            case "float":
                out = float(x[1])
            case "bool":
                out = x[1] == "True"
            case "variable":
                out = dic[x[1]]
            case "+" | "-" | "*" | "/" | "//" | "%" | "**" | "==" | "!=" | ">" | ">=" | "<" | "<=" | "in" | "notin" | "and" | "or":
                out = OPERATORS[x[0]](run([x[1]], dic), run([x[2]], dic))
            case "uplus":
                out = +run([x[1]], dic)
            case "uminus":
                out = -run([x[1]], dic)
            case "is":
                out = TESTS[x[2]](run([x[1]], dic))
            case "isnot":
                out = not TESTS[x[2]](run([x[1]], dic))
            case "not":
                out = not run([x[1]], dic)
            case "filter":
                out = getattr(builtins, x[2])(run([x[1]], dic))
            case "method":
                # ! should var be assigned to this? (if the method returns a value instead of applying to var then it makes a difference) test in jinja
                out = getattr(run([x[1]], dic), x[2])()  
            case "item":  
                # ! Jinja deals with this differently, might need to use try, except statements
                out = run([x[1]], dic).__getitem__(run([x[2]], dic))
            case "attr":
                # ! i don't think this makes comment makes sense anymore -> should var be assigned to this? (if the method returns a value instead of applying to var then it makes a difference) test in jinja
                out = getattr(run([x[1]], dic), x[2])  
            case _:
                pass
    return out


OPERATORS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "//": operator.floordiv,
    "%": lambda x, y: x % y,
    "**": lambda x, y: x ** y,
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
    "in": lambda x, y: operator.contains(y, x),
    "notin": lambda x, y: not operator.contains(y, x),
    "and": lambda x, y: x and y,
    "or": lambda x, y: x or y,
}
