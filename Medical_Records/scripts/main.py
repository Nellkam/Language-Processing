import re

class MedicalRecord:
    def __init__(self,regexgroup):
        keys = "id index date firstname lastname age gender city sport club email fed result".split()
        self.data = {}
        for i,item in enumerate(list(regexgroup[0])):
            self.data[keys[i]] = item

    def __str__(self):
        str = "{\n"
        for k,v in self.data.items():
            str = str+f"\t{k}: {v}\n"
        str = str+"}\n"
        return str

records = {}

with open("../emd.csv") as fp:
    pattern = r"^(\w+),(\d+),((?:\d+-?)+),(\w+),(\w+),(1?[1-9]?(?:(?<=,)[1-9]|(?<=\d)\d)),(F|M),(\w+),(\w+),(\w+),(.+?),(true|false),(true|false)$"
    for line in fp.readlines():
        match = re.findall(pattern,line)
        if match is None or match==[]:
            continue;
        entry = MedicalRecord(match)
        records[entry.data["id"]]=entry

for record in records.values():
    print(record)
print(records.__len__())

