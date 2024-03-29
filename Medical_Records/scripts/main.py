import re
import sys
from jinja2    import Environment, FileSystemLoader, select_autoescape
from operator  import itemgetter
from os        import makedirs, path
from plots     import plot_C, plot_D, plot_BFG
from queries   import Record, Records, edge_dates, records_by_year, item_groups, item_frequencies, age_gender
from typing    import Dict
from unidecode import unidecode
from writes    import write_index, write_records, write_query, write_queryD, write_queryE

def main() -> int:
    records: Records = readCSV(sys.argv[1])
    recordsYear: Dict[str, Records] = records_by_year(records)
    
    queries: Dict[str, str] = {
        'b': 'gender',
        'c': 'sport',
        'f': 'fed',
        'g': 'result',
    }

    makedirs(path.dirname("output/"), exist_ok=True)
    makedirs(path.dirname("output/resources/"), exist_ok=True)
    
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader, autoescape=select_autoescape())

    write_index(env, edge_dates(records))
    write_records(env, records)
    for query in queries.items():
        write_query(env, recordsYear, records, *query)
    write_queryD(env, age_gender(records))
    write_queryE(env, item_groups(records, 'city'))

    plot_C('total', item_frequencies(records, 'sport'))
    plot_D(age_gender(records), len(records))
    for year, rs in recordsYear.items():
        plot_C(year, item_frequencies(rs, 'sport'))
    for query, item in queries.items(): # type: ignore
        if query != 'c':
            plot_BFG(query, records, item) # type: ignore

    return 0

def readCSV(csv_file: str) -> Records:
    records: Records = []

    pattern = re.compile(r"""
        ^                                   # start of string
        (?P<id>       [\da-z]{24}),         # _id
        (?P<index>    0|[1-9]\d*),          # index
        (?P<date>     \d{4}-\d{2}-\d{2}),   # dataEMD
        (?P<firstname>[A-Z][a-z]*),         # nome/primeiro
        (?P<lastname> [A-Z][a-z]*),         # nome/último
        (?P<age>      0|[1-9]\d{,2}),       # idade
        (?P<gender>   [FM]),                # género
        (?P<city>     [A-Z][a-z]*),         # morada
        (?P<sport>    [A-Z][A-Za-z]*),      # modalidade
        (?P<club>     [A-Z][A-Za-z]*),      # clube
        (?P<email>                          # email
            [a-z0-9!#$%&'*+/=?^_`{|}~-]+            # local-part before fst dot
            (?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*     # local-part from fst dot
            @                                       # @ (at sign)
            (?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+  # domain name
            [a-z0-9](?:[a-z0-9-]*[a-z0-9])?),       # top-level domain name
        (?P<fed>      true|false),          # federado
        (?P<result>   true|false)           # resultado
        $                                   # end of string
    """, re.X)

    with open(csv_file, 'r') as f:
        next(f)
        for line in f:
            if match := pattern.match(unidecode(line)):
                records.append(verbose(match.groupdict()))

    return sorted(records, key=itemgetter('firstname', 'lastname'))

def verbose(record: Record) -> Record:
    if record['gender'] == 'F':
        record['gender'] = 'Feminino'
    else:
        record['gender'] = 'Masculino'

    if record['fed'] == 'true':
        record['fed'] = 'Sim'
    else:
        record['fed'] = 'Não'

    if record['result'] == 'true':
        record['result'] = 'Aprovado'
    else:
        record['result'] = 'Reprovado'

    return record

if __name__ == '__main__':
    sys.exit(main())