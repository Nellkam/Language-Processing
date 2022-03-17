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

Records = dict[str,MedicalRecord]
