def run(ast, dic):
    for x in ast:
        match x[0]:
            case 'text':
                print(x[1], end="")
            case 'variable':
                print(dic[x[1]], end="")
