import re
from datetime import date
from typing import List, Dict

class MedicalRecord:
    def __init__(self, regexmatch:dict):
        self.data = regexmatch

    def __str__(self) -> str:
        str = "{\n"
        for k, v in self.data.items():
            str += f"\t{k}: {v}\n"
        str += "}\n"
        return str

def markupify(record: Dict[str, str]) -> str:
    markup = f'<h2>{record["id"]} [{record["date"]}]</h2>\n<ul>\n'
    markup += f'\t<li>[{record["index"]}] {record["lastname"]},{record["firstname"]}</li>\n'
    markup += f'\t<li>{"Male" if record["gender"] == "M" else "Female"}, {record["age"]} years old</li>\n'
    markup += f'\t<li>{record["email"]}</li>\n'
    markup += f'\t<li>Lives in {record["city"]}</li>\n'
    markup += f'\t<li>{record["sport"]} for {record["club"]}</li>\n'
    if record["fed"] == "true":
        markup += f'\t<li>Federate</li>\n'
    markup += f'\t<li>{"Positive" if record["result"] == "true" else "Negative"}</li>\n'
    markup += "</ul>\n"
    return markup

Records = dict[str,MedicalRecord]