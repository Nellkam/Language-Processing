from typing import List, Dict, Tuple
from operator import itemgetter

Record = Dict[str, str]
Records = List[Record]

def write_index(env, dates: Tuple[str, str]):
    template = env.get_template('index.html')
    with open('index.html', 'w') as f:
        f.write(template.render(dates=dates))

def write_records(env, records: Records):
    records_by_name = sorted(records, key=itemgetter('firstname', 'lastname'))
    template = env.get_template('records.html')
    with open('records.html', 'w') as f:
        f.write(template.render(records=records_by_name))

def edge_dates(records: Records) -> Tuple[str, str]:
    date = itemgetter('date')
    return (min(records, key=date)['date'], max(records, key=date)['date'])