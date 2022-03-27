from bisect    import bisect_left, bisect_right
from itertools import groupby
from operator  import itemgetter
from typing    import Dict, List, Tuple

Record = Dict[str, str]
Records = List[Record]

def edge_dates(records: Records) -> Tuple[str, str]:
    date = itemgetter('date')
    return (min(records, key=date)['date'], max(records, key=date)['date'])

def records_by_year(records: Records) -> Dict[str, Records]:
    year = lambda x: x['date'][:4]
    return {k: [*g] for k, g in groupby(sorted(records, key=year), key=year)}

def item_frequencies(records: Records, item: str) -> Dict[str, int]:
    f = itemgetter(item)
    return {k: len([*g]) for k, g in groupby(sorted(records, key=f), key=f)}

def item_groups(records: Records, item: str) -> Dict[str, Records]:
    f = itemgetter(item)
    return {k: [*g] for k, g in groupby(sorted(records, key=f), key=f)}

def age_gender(records: Records) -> Tuple[Tuple[Records, Records]]:
    sorted_by_age = sorted(records, key=itemgetter('age'))
    split_idx = bisect_left(sorted_by_age, '35', key=itemgetter('age'))
    under35 = sorted_by_age[:split_idx]
    over35 = sorted_by_age[split_idx:]

    sorted_under35 = sorted(under35, key=itemgetter('gender'))
    split_idx = bisect_right(sorted_under35, 'F', key=itemgetter('gender'))
    f_under35 = under35[:split_idx]
    m_under35 = under35[split_idx:]

    sorted_over35 = sorted(over35, key=itemgetter('gender'))
    split_idx = bisect_right(sorted_over35, 'F', key=itemgetter('gender'))
    f_over35 = over35[:split_idx]
    m_over35 = over35[split_idx:]

    return ((f_under35, m_under35), (f_over35, m_over35))