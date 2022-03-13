import re
from records import Records,MedicalRecord
from yeardist import YearDistribution
import yeardist2

def readCSV(filename:str) -> Records:
    with open(filename,"r") as fp:
        records = {}
        pattern = r"^(\w+),(\d+),(\d{4}-\d{2}-\d{2}),(\w+),(\w+),([1-9]\d?),(F|M),(\w+),(\w+),(\w+),([^,]+),(true|false),(true|false)$"
        for line in fp.readlines():
            match = re.findall(pattern,line)
            if match is None or match==[]:
                continue;
            entry = MedicalRecord(match)
            records[entry.data["id"]]=entry
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

writeHTML_records(records,"list.html")

#queryB = YearDistribution(records,"gender")
#queryC = YearDistribution(records,"sport")
#queryF = YearDistribution(records,"fed")
#queryG = YearDistribution(records,"result")
#
#queryB.writeHTML()
#queryC.writeHTML()
#queryF.writeHTML()
#queryG.writeHTML()

queryB = yeardist2.generate(records,"gender") 
queryC = yeardist2.generate(records,"sport") 
queryF = yeardist2.generate(records,"fed") 
queryG = yeardist2.generate(records,"result") 

yeardist2.writeHTML(*queryB)
yeardist2.writeHTML(*queryC)
yeardist2.writeHTML(*queryF)
yeardist2.writeHTML(*queryG)

