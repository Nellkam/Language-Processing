import builtins
from tests import TESTS

def run(ast, dic):
    out = ''
    for x in ast:
        match x[0]:
            case 'text':
                out += x[1]
            case 'print':
                out += str(run([x[1]], dic)) # ! Should x[1] be a singleton or should something be restructured?
            case 'if':
                if run([x[1]], dic):
                    out += run(x[2], dic)
            # case 'ifis':
            #     if TESTS[x[2]](dic[x[1]]):
            #         out += run(x[3], dic)
            case 'for':
                for a in dic[x[2]]:
                    dic[x[1]] = a
                    out +=  run(x[3], dic)
            case 'int':
                out = int(x[1])
            case 'variable':
                out = dic[x[1]]
                #var = dic[x[1]]
                #for y in x[2]:
                #    match y[0]:
                #        case 'filter':
                #            var = getattr(builtins, y[1])(var)
                #        case 'item':             # ! Jinja deals with this differently, might need to use try, except statements
                #            var = var.__getitem__(y[1])
                #        case 'attr':
                #            getattr(var, y[1])() # ! should var be assigned to this? (if the method returns a value instead of applying to var then it makes a difference) test in jinja
                #out = var
            case '+':
                out = run([x[1]], dic) + run([x[2]], dic)
            case '-':
                out = run([x[1]], dic) - run([x[2]], dic)
            case '*':
                out = run([x[1]], dic) * run([x[2]], dic)
            case '/':
                out = run([x[1]], dic) / run([x[2]], dic)
            case '==':
                out = run([x[1]], dic) == run([x[2]], dic)
            case '!=':
                out = run([x[1]], dic) != run([x[2]], dic)
            case '<':
                out = run([x[1]], dic) < run([x[2]], dic)
            case '>':
                out = run([x[1]], dic) > run([x[2]], dic)
            case '<=':
                out = run([x[1]], dic) <= run([x[2]], dic)
            case '>=':
                out = run([x[1]], dic) >= run([x[2]], dic)
            case 'is':
                out = TESTS[x[2]](run([x[1]], dic))
            case 'isnot':
                out = not TESTS[x[2]](run([x[1]], dic))
            case 'in':
                out = run([x[1]], dic) in run([x[2]], dic)
            case 'notin':
                out = run([x[1]], dic) not in run([x[2]], dic)
            case 'not':
                out = not run([x[1]], dic)
            case 'and':
                out = run([x[1]], dic) and run([x[2]], dic)
            case 'or':
                out = run([x[1]], dic) or run([x[2]], dic)
            case 'filter':
                out = getattr(builtins, x[2])(run([x[1]], dic))
            case 'method':
                out = getattr(run([x[1]], dic), x[2])() # ! should var be assigned to this? (if the method returns a value instead of applying to var then it makes a difference) test in jinja
            case _:
                pass
    return out
