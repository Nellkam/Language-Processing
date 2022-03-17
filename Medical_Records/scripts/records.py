from typing import List, Dict
from operator import itemgetter

Record = Dict[str, str]
Records = List[Record]

def markupify(record: Record) -> str:
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

def writeHTML_records(records: Records, filename: str):
    records_by_date = sorted(records, key=itemgetter('date'), reverse=True)
    with open(filename, "w") as f:
        for record in records_by_date:
            f.write(markupify(record))