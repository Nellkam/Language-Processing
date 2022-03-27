import re
import sys
from os        import makedirs, path
from yeardist  import records_by_year, item_groups, item_frequencies, plot_C, plot_BFG
from unidecode import unidecode
from records   import Records, write_index, write_records, write_query, write_queryE, write_queryD, edge_dates
from jinja2    import Environment, FileSystemLoader, select_autoescape
from city      import cities
from ageGender import age_gender, plot_age_gender

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
    write_queryE(env, cities(records))

    plot_age_gender(age_gender(records), len(records))
    plot_C('total', item_frequencies(records, 'sport'))
    for year, rs in recordsYear.items():
        plot_C(year, item_frequencies(rs, 'sport'))

    for query, item in queries.items():
        if query != 'c':
            plot_BFG(query, records, item)

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