def run(ast, dic):
    tmp = {}
    for x in ast:
        match x[0]:
            case 'text':
                print(x[1], end="")
            case 'variable':
                print(dic[x[1]], end="")
            case 'if':
                if dic[x[1]]:
                    run(x[2], dic)
            case 'for':
                for a in dic[x[2]]:
                    dic[x[1]] = a
                    run(x[3], dic)
            case _:
                pass
