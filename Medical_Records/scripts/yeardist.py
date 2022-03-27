import re
from records import Records
from typing import Any, Dict, Set
import numpy as np
import matplotlib.pyplot as plt
import os

html5_head_template = """
<!doctype html>
<html lang="en">
<head>
\t<meta charset="utf-8">
\t<title>{TITLE}</title>
</head>
"""

def convertKey(query: str, key: str) -> str:
    if key == "M":
        return "Masculino"
    elif key == "F":
        return "Feminino"
    elif key == "true":
        return "Aprovado" if query == "result" else "Sim"
    elif key == "false":
        return "Reprovado" if query == "result" else "Não"
    else:
        return key

def generate(records: Records, query: str) -> tuple[str, dict]:
    years: Dict[Any, Any] = {}
    if query != "gender" and query != "sport" and query != "fed" and query != "result":
        return ("", {})
    for record in records:
        year = re.findall(r'^\d+', record["date"])[0]
        if year not in years:
            years[year] = {}
        if record[query] not in years[year]:
            years[year][record[query]] = set()
        years[year][record[query]].add(record["id"])
    return (query, years)

def getFrequency(years: dict, year: str = None) -> dict[str, int]:
    result: Dict[str, int] = {}
    for y, dist in years.items():
        if year is None or year == y or year == "total":
            for k, ids in dist.items():
                if k not in result:
                    result[k] = 0
                result[k] += len(ids)
        if year is not None and year == y:
            break
    return result

def getIds(years: dict, year: str = None) -> dict[str, set[str]]:
    result: Dict[str, Set[str]] = {}
    for y, dist in years.items():
        if year is None or year == y or year == "total":
            for k, ids in dist.items():
                if k not in result:
                    result[k] = set()
                result[k] = result[k].union(ids)
        if year is not None and year == y:
            break
    return result

def writeHTML(query: str, years: dict, listPath: str):
    titles = {
        "sport": "Distribuição Modalidades",
        "gender": "Distribuição Género",
        "fed": "Estatuto Federado",
        "result": "Resultados Exames Fitness"
    }

    keys = list(years.keys())
    keys.append("total")
    for year in keys:
        freq = getFrequency(years, year)
        ids = getIds(years, year)
        filename = f"output/{query}{year}.html"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            f.write(re.sub(r'{\w+}',filename.split("/")[-1],html5_head_template))
            f.write("\n<body>\n")
            f.write(f"<h1>{titles[query]} {year} </h1>\n")
            for key in freq.keys():
                f.write(f"<h2>{'='*10} {convertKey(query,key)} [{freq[key]}] {'='*10}</h2>\n<ul>\n")
                for id in ids[key]:
                    f.write(f'\t<li><a href="{listPath}#{id}" target="_blank">{id}</a></li>\n')
                f.write("</ul>")
            f.write("\n</body>\n")

def run(records:Records):
    queries = "gender sport fed result".split()
    data = {}
    
    #Text
    for q in queries:
        data[q] = generate(records,q)[1]
        writeHTML(q,data[q],"./output/list.html")
    
    #Plots
    plot_BFG("result",data["result"])
    plot_BFG("gender",data["gender"])
    plot_BFG("fed",data["fed"])
    
    years = list(data["sport"].keys()) ; years.append("total")
    for year in years:
        freqs = getFrequency(data["sport"],year)
        plot_C(year,freqs)

def plot_C(year:str,sports:dict[str,int]):
    _, ax = plt.subplots()

    # Example data
    labels = list(sports.keys())
    y_pos = np.arange(len(labels))
    values = [ sports[label] for label in labels ]

    ax.barh(y_pos, values, align='center')
    ax.set_yticks(y_pos, labels=labels)
    ax.invert_yaxis()

    plt.savefig(f"./output/resources/plotsport{year}.png")


def plot_BFG(query:str,years:dict):
    #Data format
    results:dict[str,list[int]] = {}
    category_names:list[str] = [] 

    ykeys = list(years.keys()) ; ykeys.sort()
    ykeys.append("total")
    for year in ykeys:
        freqs = getFrequency(years,year)
        category_names = list(freqs.keys()) ; category_names.sort()
        values = []

        for label in category_names:
            values.append(freqs[label])

        total = sum(values)

        if query=="result":
            values = list(map(lambda abs:round(abs/total*100),values))

        results[year] =  values
    
    category_names = list(map(lambda key:convertKey(query,key),category_names))
     
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

    plt.savefig(f"./output/resources/plot{query}.png")
