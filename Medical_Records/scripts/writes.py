from operator import itemgetter
from typing   import List, Dict, Tuple
from queries  import Record, Records, item_groups

def write_index(env, dates: Tuple[str, str]):
    template = env.get_template('index.html')
    with open('output/index.html', 'w') as f:
        f.write(template.render(dates=dates))

def write_records(env, records: Records):
    template = env.get_template('records.html')
    with open('output/records.html', 'w') as f:
        f.write(template.render(records=records))

def write_query(env, years: Dict[str, Records], records: Records, query: str, item: str):
    template = env.get_template(f'query.html')
    with open(f"output/query{query}.html", 'w') as f:
        f.write(template.render(
            query=query,
            years=years.keys(),
            total=item_groups(records, item),
            size=len(records)
        ))

    template = env.get_template(f'subquery.html')
    for year, records in years.items():
        with open(f"output/query{query}{year}.html", 'w') as f:
            f.write(template.render(
                query=query,
                year=year,
                item=item_groups(records, item),
                size=len(records)
            ))

def write_queryD(env, dist: Tuple[Tuple[Records, Records], Tuple[Records, Records]]):
    template = env.get_template(f'queryd.html')
    with open(f"output/queryd.html", 'w') as f:
        f.write(template.render(dist = dist))

def write_queryE(env, cities: Dict[str, Records]):
    template = env.get_template(f'querye.html')
    with open(f"output/querye.html", 'w') as f:
        f.write(template.render(cities = cities))