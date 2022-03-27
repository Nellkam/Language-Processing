from itertools import groupby
from operator import itemgetter
from records import Records
from typing import Dict

Cities = Dict[str, Records]

def cities(records: Records) -> Cities:
    city = itemgetter('city')
    return {k: [*g] for k, g in groupby(sorted(records, key=city), key=city)}