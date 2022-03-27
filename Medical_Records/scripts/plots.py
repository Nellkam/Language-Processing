from queries import Records, item_frequencies, item_groups, records_by_year
from typing  import Dict, List, Tuple
import matplotlib.pyplot as plt # type: ignore
import numpy             as np

def plot_D(age_gender: Tuple[Tuple[Records, Records], Tuple[Records,Records]], total: int):
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

    labels = ['F >= 35', 'F < 35', 'M < 35', 'M >= 35']
    slices = [f_over35, f_under35, m_under35, m_over35]
    colors = ['mediumvioletred', 'deeppink', 'mediumblue', 'darkblue']

    plt.pie(slices,
            labels = labels,
            colors = colors,
            startangle = 90,
            radius = 1,
            autopct = '%1.2f%%')

    plt.savefig("output/resources/age_gender.png", bbox_inches='tight')
    plt.clf()

def plot_C(year: str, sports: Dict[str, int]):
    _, ax = plt.subplots()
    labels = list(sports.keys())
    y_pos = np.arange(len(labels))
    values = [ sports[label] for label in labels ]

    ax.barh(y_pos, values, align='center')
    ax.set_yticks(y_pos, labels=labels)
    ax.invert_yaxis()

    plt.savefig(f"./output/resources/plotc{year}.png", bbox_inches="tight")
    plt.clf()

def plot_BFG(query: str, records: Records, item: str):
    category_names = item_groups(records, item).keys()
    records_years = records_by_year(records)

    results: Dict[str, List[float]] = {}
    for year, recs in records_years.items():
        d = item_frequencies(recs, item)
        for c in category_names:
            if c not in d:
                d[c] = 0
        results[year] = [*d.values()]

    results['total'] = [*item_frequencies(records, item).values()]

    if query == 'g':
        for year, cat in results.items():
            if year == 'total':
                results['total'] = list(map(lambda x: x * 100 / len(records), results['total']))
            else:
                total = len(records_years[year])
                results[year] = list(map(lambda x: x * 100 / total, cat))

    #Template
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.colormaps['RdYlGn'](
        np.linspace(0.15, 0.85, data.shape[1]))

    _, ax = plt.subplots()
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        rects = ax.barh(labels, widths, left=starts, height=0.2,
                        label=colname, color=color, align="center")

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        ax.bar_label(rects, label_type='center', color=text_color)
    ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='small')

    plt.savefig(f"./output/resources/plot{query}total.png",bbox_inches="tight")
    plt.clf()