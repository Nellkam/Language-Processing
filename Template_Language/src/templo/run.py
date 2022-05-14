import builtins
import operator
import sys
import typing as t
from .yacc import parser
from .tests import TESTS


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
            case "fordict":
                print(dic[x[3]])
                for a, b in dic[x[3]].items(): # ! Easy clashes
                    dic[x[1]] = a
                    dic[x[2]] = b
                    out += run(x[4], dic)
            case "repeat":
                for _ in range(run([x[1]], dic)):
                    out += run(x[2], dic)
            case "variable":
                try:
                    out = dic.get(x[1], None)
                except AttributeError:
                    out = None
            case "int":
                out = int(x[1])
            case "float":
                out = float(x[1])
            case "bool":
                out = x[1] == "True"
            case "list":
                out = list(map(lambda y: run([y], dic), x[1]))
            case "tuple":
                out = tuple(map(lambda y: run([y], dic), x[1]))
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
            case "item":
                # ! Jinja deals with this differently, might need to use try, except statements
                out = run([x[1]], dic).__getitem__(run([x[2]], dic))
            case "attr":
                # ! i don't think this makes comment makes sense anymore -> should var be assigned to this? (if the method returns a value instead of applying to var then it makes a difference) test in jinja
                out = getattr(run([x[1]], dic), x[2])
            case "method":
                # ! should var be assigned to this? (if the method returns a value instead of applying to var then it makes a difference) test in jinja
                args = tuple(map(lambda y: run([y], dic), x[3]))
                out = getattr(run([x[1]], dic), x[2])(*args)
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
    "**": lambda x, y: x**y,
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


def template(template):
    ast = parser.parse(template)

    def _f(dic=None):
        return run(ast, dic)

    return _f


def main(argv):
    import readline

    while True:
        try:
            s = input("template > ")
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)

        class MyClass:
            x = 5

            def f(self, i, j, k):
                return i * j - k + self.x

            def g(self):
                return 9

        p1 = MyClass()

        d = {
            "a": [2, 1, 3],
            "b": "Diana",
            "c": {"foo": 42, "bar": 73},
            "d": 42,
            "e": p1,
        }

        print("dict:", d)
        print("ast:", result)
        print(run(result, d))


if __name__ == "__main__":
    sys.exit(main(sys.argv))
