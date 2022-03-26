from typing import List, Dict
from operator import itemgetter
import inspect
import re

Record = Dict[str, str]
Records = List[Record]

html5_head_template = """
<!doctype html>
<html lang="en">
<head>
\t<meta charset="utf-8">
\t<title>{TITLE}</title>
</head>
"""

def markupify(record: Record) -> str:
    return inspect.cleandoc(f"""
        <h2>{record['id']} [{record['date']}]</h2>
        <ul id=\"{record['id']}\">
        \t<li>[{record['index']}] {record['lastname']},{record['firstname']}</li>
        \t<li>{'Male' if record['gender'] == 'M' else 'Female'}, {record['age']} years old</li>
        \t<li>{record['email']}</li>
        \t<li>Lives in {record['city']}</li>
        \t<li>{record['sport']} for {record['club']}</li>
        \t<li>Federated: {'Yes' if record['fed'] == 'true' else 'No'}</li>
        \t<li>{'Positive' if record['result'] == 'true' else 'Negative'}</li>
        </ul>
    """)

def writeHTML_records(records: Records, filename: str):
    records_by_date = sorted(records, key=itemgetter('date'), reverse=True)
    with open(filename, "w") as f:
        f.write(re.sub(r'{\w+}',"Medical Records",html5_head_template))
        f.write("\n<body>\n")
        for record in records_by_date:
            f.write(f"{markupify(record)}\n")
        f.write("\n</body>\n")
