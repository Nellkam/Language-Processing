import pprint
import re
import sys
from typing import List, Dict
# from records import Records,MedicalRecord
# import yeardist

Records = List[Dict[str, str]]
records: Records = []

pattern = re.compile(r"""
    ^                            # start of string
    (?P<id>\w+),                 # _id
    (?P<index>\d+),              # index
    (?P<date>\d{4}-\d{2}-\d{2}), # dataEMD
    (?P<firstname>\w+),          # nome/primeiro
    (?P<lastname>\w+),           # nome/último
    (?P<age>[1-9]\d?),           # idade
    (?P<gender>[FM]),            # género
    (?P<city>\w+),               # morada
    (?P<sport>\w+),              # modalidade
    (?P<club>\w+),               # clube
    (?P<email>[^,]+),            # email
    (?P<fed>true|false),         # federado
    (?P<result>true|false)       # resultado
    $                            # end of string
""", re.X)

with open(sys.argv[1], 'r') as f:
    for line in f:
        if match := pattern.match(line):
            records.append(match.groupdict())

pprint.pprint(records)
print(f'{len(records)} total records')

# def writeHTML_records(records: List[Dict[str, str]], filename: str):
#     with open(filename, "w") as fp:
#         sortDate = list(records.values())
#         sortDate.sort(reverse=True)
#         for record in sortDate:
#             fp.write(record.markupify())
#         print(f'$!> Records written to {filename}')
#
# #printRecords(records)
# writeHTML_records(records, "list.html")
#
# queryB = yeardist.generate(records, "gender")
# queryC = yeardist.generate(records, "sport")
# queryF = yeardist.generate(records, "fed")
# queryG = yeardist.generate(records, "result")
#
# yeardist.writeHTML(*queryB)
# yeardist.writeHTML(*queryC)
# yeardist.writeHTML(*queryF)
# yeardist.writeHTML(*queryG)
