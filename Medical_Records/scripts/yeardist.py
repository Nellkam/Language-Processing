from itertools import groupby
from operator  import itemgetter
from typing    import List, Dict
import matplotlib.pyplot as plt
import numpy             as np

Record = Dict[str, str]
Records = List[Record]

def records_by_year(records: Records) -> Dict[str, Records]:
    year = lambda x: x['date'][:4]
    return {k: [*g] for k, g in groupby(sorted(records, key=year), key=year)}

def item_frequencies(records: Records, item: str) -> Dict[str, int]:
    f = itemgetter(item)
    return {k: len([*g]) for k, g in groupby(sorted(records, key=f), key=f)}

def item_groups(records: Records, item: str) -> Dict[str, Records]:
    f = itemgetter(item)
    return {k: [*g] for k, g in groupby(sorted(records, key=f), key=f)}

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

    results = {}
    for year, recs in records_years.items():
        d = item_frequencies(recs, item)
        for c in category_names:
            if c not in d:
                d[c] = 0
        results[year] = [*d.values()]

    results['total'] = [*item_frequencies(records, item).values()]

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