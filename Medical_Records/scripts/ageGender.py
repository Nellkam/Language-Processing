from bisect   import bisect_left, bisect_right
from operator import itemgetter
from records  import Records
from typing   import Tuple

from pprint import pprint

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