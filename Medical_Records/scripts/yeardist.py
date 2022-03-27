import os
import re
from itertools import groupby
from typing import Any, List, Dict, Set
from operator import itemgetter

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

# def getFrequency(years: dict, year: str = None) -> dict[str, int]:
#     result: Dict[str, int] = {}
#     for y, dist in years.items():
#         if year is None or year == y or year == "all":
#             for k, ids in dist.items():
#                 if k not in result:
#                     result[k] = 0
#                 result[k] += len(ids)
#         if year is not None and year == y:
#             break
#     return result
# 
# def getIds(years: dict, year: str = None) -> dict[str, set[str]]:
#     result: Dict[str, Set[str]] = {}
#     for y, dist in years.items():
#         if year is None or year == y or year == "all":
#             for k, ids in dist.items():
#                 if k not in result:
#                     result[k] = set()
#                 result[k] = result[k].union(ids)
#         if year is not None and year == y:
#             break
#     return result
# 
# def convertKey(query: str, key: str) -> str:
#     if key == "M":
#         return "Male"
#     elif key == "F":
#         return "Female"
#     elif key == "true":
#         return "Pass" if query == "result" else "True"
#     elif key == "false":
#         return "Not Pass" if query == "result" else "False"
#     else:
#         return key
# 
# def writeHTML(query: str, years: dict):
#     titles = {
#         "sport": "Sports Distribution",
#         "gender": "Gender Distribution",
#         "fed": "Federate Status",
#         "result": "Medical Fitness Results"
#     }
# 
#     keys = list(years.keys())
#     keys.append("all")
#     for year in keys:
#         freq = getFrequency(years, year)
#         ids = getIds(years, year)
#         filename = f"output/{query}{year if year != 'all' else 'total'}.html"
#         os.makedirs(os.path.dirname(filename), exist_ok=True)
#         with open(filename, "w") as f:
#             f.write(f"<h1>{titles[query]} {year if year!='all' else 'Total'} </h1>")
#             for key in freq.keys():
#                 f.write(f"<h2>{'='*10} {convertKey(query,key)} [{freq[key]}] {'='*10}</h2>\n<ul>\n")
#                 for id in ids[key]:
#                     f.write(f"\t<li>{id}</li>\n")
#                 f.write("</ul>")
# 