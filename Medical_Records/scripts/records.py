from typing import List, Dict
from operator import itemgetter
from inspect import cleandoc

Record = Dict[str, str]
Records = List[Record]

def writeHTML_records(env, records: Records):
    records_by_name = sorted(records, key=itemgetter('firstname', 'lastname'), reverse=True)
    template = env.get_template('records.html')
    with open('records.html', 'w') as f:
        f.write(template.render(records=records))