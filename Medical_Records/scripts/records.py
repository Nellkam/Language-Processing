from typing import List, Dict
from operator import itemgetter
import inspect

Record = Dict[str, str]
Records = List[Record]

def markupify(record: Record) -> str:
    markup = inspect.cleandoc(f"""
        <h2>{record['id']} [{record['date']}]</h2>
        <ul>
        \t<li>[{record['index']}] {record['lastname']},{record['firstname']}</li>
        \t<li>{'Male' if record['gender'] == 'M' else 'Female'}, {record['age']} years old</li>
        \t<li>{record['email']}</li>
        \t<li>Lives in {record['city']}</li>
        \t<li>{record['sport']} for {record['club']}</li>
        \t<li>Federated: {'Yes' if record['fed'] == 'true' else 'No'}</li>
        \t<li>{'Positive' if record['result'] == 'true' else 'Negative'}</li>
        </ul>
    """)
    return markup

def writeHTML_records(records: Records, filename: str):
    records_by_date = sorted(records, key=itemgetter('date'), reverse=True)
    with open(filename, "w") as f:
        for record in records_by_date:
            f.write(f"{markupify(record)}\n")