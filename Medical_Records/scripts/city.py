from itertools import groupby
from operator import itemgetter
from records import Records
from typing import Any, Dict, List

City = Dict[str, List[Dict[str, Any]]]

def city(records: Records) -> City:
    f = itemgetter('city')
    return {k: [*g] for k, g in groupby(sorted(records, key=f), key=f)}
    # return {k: [*g] for k, g in groupby(sorted(records, key=itemgetter('city')), key=itemgetter('city'))}
    # return dict(map(lambda kg: (kg[0], list(kg[1])), groupby(sorted(records, key=itemgetter('city')), key=itemgetter('city'))))
    # grouped_by_city: City = {}
    # city = itemgetter('city')
    # for k, g in groupby(sorted(records, key=city), key=city):
    #     grouped_by_city[k] = list(g)
    # return grouped_by_city

def dist_city(city: City) -> Dict[str, int]:
    return {k: len(v) for k, v in city.items()}