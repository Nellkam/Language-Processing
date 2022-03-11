import re

class MedicalRecord:
    def __init__(self,regexgroup:list):
        keys = "id index date firstname lastname age gender city sport club email fed result".split()
        self.data = {}
        for i,item in enumerate(list(regexgroup[0])):
            self.data[keys[i]] = item

    def __str__(self) -> str:
        str = "{\n"
        for k,v in self.data.items():
            str += f"\t{k}: {v}\n"
        str +="}\n"
        return str

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

def writeHTML_records(records:dict,filename:str):
    with open(filename,"w") as fp:
        for record in records.values():
            fp.write(record.markupify())
        print(f'$!> Records written to {filename}')

def readCSV(records:dict,filename:str):
    with open(filename,"r") as fp:
        pattern = r"^(\w+),(\d+),(\d{4}-\d{2}-\d{2}),(\w+),(\w+),([1-9]\d?),(F|M),(\w+),(\w+),(\w+),([^,]+),(true|false),(true|false)$"
        for line in fp.readlines():
            match = re.findall(pattern,line)
            if match is None or match==[]:
                continue;
            entry = MedicalRecord(match)
            records[entry.data["id"]]=entry
        print("$!> CSV FILE HAS BEEN READ!")

def printRecords(records:dict):
    for record in records.values():
        print(record)
    print(f'{records.__len__()} total records')


records = {}

readCSV(records,"../emd.csv")
printRecords(records)
writeHTML_records(records,"list.html")


