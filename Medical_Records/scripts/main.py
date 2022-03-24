import pprint
import re
import sys
import yeardist
from unidecode import unidecode
from records import Records, markupify, writeHTML_records

def main() -> int:
    records: Records = readCSV(sys.argv[1])

    # Test prints - show if 300 records have been correctly parsed and validated
    # !!! Remove before submitting
    print("CSV FILE READ")
    pprint.pprint(records)
    print(f'{len(records)} total records')

    writeHTML_records(records, "list.html")

    # execute queries
    # TODO: move to function
    queryB = yeardist.generate(records, "gender")
    queryC = yeardist.generate(records, "sport")
    queryF = yeardist.generate(records, "fed")
    queryG = yeardist.generate(records, "result")

    # write queries
    # TODO: move to function
    yeardist.writeHTML(*queryB)
    yeardist.writeHTML(*queryC)
    yeardist.writeHTML(*queryF)
    yeardist.writeHTML(*queryG)

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