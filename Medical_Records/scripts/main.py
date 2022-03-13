import re
from records import Records,MedicalRecord
import yeardist

def readCSV(filename:str):
    with open(filename, "r") as fp:
        records = {}
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
        for line in fp.readlines():
            match = pattern.match(line)
            if match:
                entry = MedicalRecord(match.groupdict())
                records[entry.data["id"]] = entry
        print("$!> CSV FILE HAS BEEN READ!")
        return records

def writeHTML_records(records:Records,filename:str):
    with open(filename,"w") as fp:
        sortDate = list(records.values())
        sortDate.sort(reverse=True)
        for record in sortDate:
            fp.write(record.markupify())
        print(f'$!> Records written to {filename}')

def printRecords(records:Records):
    for record in records.values():
        print(record)
    print(f'{records.__len__()} total records')


records = readCSV("../emd.csv")

#printRecords(records)
writeHTML_records(records, "list.html")

queryB = yeardist.generate(records,"gender") 
queryC = yeardist.generate(records,"sport") 
queryF = yeardist.generate(records,"fed") 
queryG = yeardist.generate(records,"result") 

yeardist.writeHTML(*queryB)
yeardist.writeHTML(*queryC)
yeardist.writeHTML(*queryF)
yeardist.writeHTML(*queryG)
