from itertools import groupby
from operator import itemgetter
from records import Records
from typing import Any, Dict, List

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

# TODO functions to convert strings to html syntax
def markupify_city(cities: Cities):
    for city, records in cities.items():
        records.sort(key=itemgetter('firstname'))
        records.sort(key=itemgetter('lastname'))
        print(f'{city}: {len(records)}')
        print('<ul>')
        for record in records:
            print(f'\t<li><b>{record["firstname"]} {record["lastname"]}:</b> {record["sport"]}</li>')
        print('</ul>')