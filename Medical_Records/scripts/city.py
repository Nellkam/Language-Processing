from inspect import cleandoc
from itertools import groupby
from operator import itemgetter
from os import makedirs, path
from records import Records
from typing import Dict, List

Cities = Dict[str, Records]

def cities(records: Records) -> Cities:
    city = itemgetter('city')
    return {k: [*g] for k, g in groupby(sorted(records, key=city), key=city)}
    # return {k: [*g] for k, g in groupby(sorted(records, key=itemgetter('city')), key=itemgetter('city'))}
    # return dict(map(lambda kg: (kg[0], list(kg[1])), groupby(sorted(records, key=itemgetter('city')), key=itemgetter('city'))))
    # grouped_by_city: City = {}
    # city = itemgetter('city')
    # for k, g in groupby(sorted(records, key=city), key=city):
    #     grouped_by_city[k] = list(g)
    # return grouped_by_city

def markupify_city(city: str, records: Records) -> str:
    records.sort(key=itemgetter('firstname', 'lastname'))
    return cleandoc(f"""
        {city}: {len(records)}
        <ul>
        {"".join(f"<li><b>{r['firstname']}:</b> {r['sport']}</li>" for r in records)}
        </ul>
    """) + '\n'
    # result = ""
    # result += f"{city}: {len(records)}"
    # result += '<ul>'
    # for record in records:
    #     result += f"\t<li><b>{record['firstname']} {record['lastname']}:</b> {record['sport']}</li>"
    # result += '</ul>'
    # return result

def write_cities(cities: Cities):
    file = 'output/cities.html'
    makedirs(path.dirname(file), exist_ok=True)
    with open(file, 'w') as f:
        for city in cities.items():
            f.write(markupify_city(*city))

def write_cities2(cities: Cities):
    file = 'output/cities.html'
    makedirs(path.dirname(file), exist_ok=True)
    with open(file, 'w') as f:
        for city, records in cities.items():
            records.sort(key=itemgetter('firstname', 'lastname'))
            f.write(cleandoc(f"""
                {city}: {len(records)}
                <ul>
                {"".join(f"<li><b>{r['firstname']}:</b> {r['sport']}</li>" for r in records)}
                </ul>
            """))
            # f.write(f"{city}: {len(records)}\n")
            # f.write('<ul>\n')
            # for record in records:
            #     f.write(f"\t<li><b>{record['firstname']} {record['lastname']}:</b> {record['sport']}</li>\n")
            # f.write('</ul>\n')