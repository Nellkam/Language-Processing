import pprint
import re
import sys
import yeardist
from records import Records, markupify, writeHTML_records
from age_gender import age_gender
# from records import Records,MedicalRecord

def main():
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

    # read csv
    # TODO: move to function
    with open(sys.argv[1], 'r') as f:
        for line in f:
            if match := pattern.match(line):
                records.append(match.groupdict())

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
    queryD = age_gender(records)
    queryF = yeardist.generate(records, "fed")
    queryG = yeardist.generate(records, "result")

    # write queries
    # TODO: move to function
    yeardist.writeHTML(*queryB)
    yeardist.writeHTML(*queryC)
    yeardist.writeHTML(*queryF)
    yeardist.writeHTML(*queryG)

if __name__ == '__main__':
    main()