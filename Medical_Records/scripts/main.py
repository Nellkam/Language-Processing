import re
from datetime import date

class MedicalRecord:
    def __init__(self, regexmatch:dict):
        self.data = regexmatch

    def __str__(self) -> str:
        str = "{\n"
        for k, v in self.data.items():
            str += f"\t{k}: {v}\n"
        str += "}\n"
        return str
    
    # dunder for sorting
    def __lt__(self, other) -> bool:
        date1 = date(*list(map(int, re.findall(r'\d+', self.data["date"]))))
        date2 = date(*list(map(int, re.findall(r'\d+', other.data["date"]))))
        return date1 < date2

    def markupify(self) -> str:
        str = f'<h2>{self.data["id"]} [{self.data["date"]}]</h2>\n<ul>\n'
        str += f'\t<li>[{self.data["index"]}] {self.data["lastname"]},{self.data["firstname"]}</li>\n'
        str += f'\t<li>{"Male" if self.data["gender"]=="M" else "Female"}, {self.data["age"]} years old</li>\n'
        str += f'\t<li>{self.data["email"]}</li>\n'
        str += f'\t<li>Lives in {self.data["city"]}</li>\n'
        str += f'\t<li>{self.data["sport"]} for {self.data["club"]}</li>\n'
        if self.data["fed"] == "true":
            str += f'\t<li>Federate</li>\n'
        str += f'\t<li>{"Positive" if self.data["result"]=="true" else "Negative"}</li>\n'
        str += "</ul>\n"
        return str

def writeHTML_records(records:dict, filename:str):
    with open(filename, "w") as fp:
        sortDate = list(records.values())
        sortDate.sort(reverse = True)
        for record in sortDate:
            fp.write(record.markupify())
        print(f'$!> Records written to {filename}')

def readCSV(records:dict, filename:str):
    with open(filename, "r") as fp:
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

def printRecords(records:dict):
    for record in records.values():
        print(record)
    print(f'{records.__len__()} total records')


records = {}

readCSV(records, "../emd.csv")
#printRecords(records)
writeHTML_records(records, "list.html")


