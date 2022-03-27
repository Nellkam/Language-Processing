from typing import List, Dict, Tuple
from operator import itemgetter
from yeardist import item_groups

Record = Dict[str, str]
Records = List[Record]

def write_index(env, dates: Tuple[str, str]):
    template = env.get_template('index.html')
    with open('output/index.html', 'w') as f:
        f.write(template.render(dates=dates))

def write_records(env, records: Records):
    records_by_name = sorted(records, key=itemgetter('firstname', 'lastname'))
    template = env.get_template('records.html')
    with open('output/records.html', 'w') as f:
        f.write(template.render(records=records_by_name))

def write_query(env, years: List[str], total: Dict[str, Records], query: str):
    template = env.get_template(f'query.html')
    with open(f'output/query{query}.html', 'w') as f:
        f.write(template.render(query=query, years=years, total=total))

def write_subquery(env, years: Dict[str, Records], item: str, query: str):
    template = env.get_template(f'subquery.html')
    for year, records in years.items():
        with open(f'output/query{query}{year}.html', 'w') as f:
            f.write(template.render(year=year, item=item_groups(records, item)))

def edge_dates(records: Records) -> Tuple[str, str]:
    date = itemgetter('date')
    return (min(records, key=date)['date'], max(records, key=date)['date'])