from bisect   import bisect_left, bisect_right
from operator import itemgetter
from records  import Records
from typing   import Tuple
import matplotlib.pyplot as plt

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

def plot_age_gender(age_gender: Tuple[Tuple[Records, Records]], total: int):
    f = len(age_gender[0][0]) + len(age_gender[1][0])
    m = len(age_gender[0][1]) + len(age_gender[1][1])
    under35 = len(age_gender[0][0]) + len(age_gender[0][1])
    over35 = len(age_gender[1][0]) + len(age_gender[1][1])
    f_under35 = len(age_gender[0][0])
    m_under35 = len(age_gender[0][1])
    f_over35 = len(age_gender[1][0])
    m_over35 = len(age_gender[1][1])

    labels = ['F', 'M']
    slices = [f, m]
    colors = ['deeppink', 'mediumblue']
    
    plt.pie(slices,
            labels = labels,
            colors = colors,
            startangle = 90,
            radius = 1,
            autopct = '%1.2f%%')

    plt.savefig("output/resources/gender.png", bbox_inches='tight')
    plt.clf()

    labels = ['<35', '>=35']
    slices = [under35, over35]
    colors = ['lightgrey', 'grey']
    
    plt.pie(slices,
            labels = labels,
            colors = colors,
            startangle = 90 + f_over35 * 360 / total,
            radius = 1,
            autopct = '%1.2f%%')

    plt.savefig("output/resources/age.png", bbox_inches='tight')
    plt.clf()

    labels = ['<35', '>=35']

    labels = ['F >= 35', 'M < 35', 'F < 35', 'M >= 35']
    slices = [f_over35, m_under35, f_under35, m_over35]
    colors = ['mediumvioletred', 'deeppink', 'mediumblue', 'darkblue']

    plt.pie(slices,
            labels = labels,
            colors = colors,
            startangle = 90,
            radius = 1,
            autopct = '%1.2f%%')

    plt.savefig("output/resources/age_gender.png", bbox_inches='tight')
    plt.clf()