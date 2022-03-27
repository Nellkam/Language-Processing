import pprint
import re
import sys
from os import makedirs, path
from yeardist import records_by_year, item_groups
from unidecode import unidecode
from records import Records, write_index, write_records, write_queryB, write_subqueryB, edge_dates
from jinja2 import Environment, FileSystemLoader, select_autoescape

def main() -> int:
    records: Records = readCSV(sys.argv[1])
    
    makedirs(path.dirname("output/"), exist_ok=True)

    recordsYear: Dict[str, Records] = records_by_year(records)
    
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader, autoescape=select_autoescape())

    write_index(env, edge_dates(records))
    write_records(env, records)
    write_queryB(env, records_by_year(records).keys(), item_groups(records, 'gender'))
    write_subqueryB(env, recordsYear)
    # write_queryC()
    # write_queryD()
    # write_queryE()
    # write_queryF()
    # write_queryG()

    # execute queries
    # queryB = generate(records, "gender")
    # queryC = generate(records, "sport")
    # queryF = generate(records, "fed")
    # queryG = generate(records, "result")

    # write queries
    # yeardist.writeHTML(*queryB)
    # yeardist.writeHTML(*queryC)
    # yeardist.writeHTML(*queryF)
    # yeardist.writeHTML(*queryG)

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
                records.append(match.groupdict())

    return records

if __name__ == '__main__':
    sys.exit(main())