import re
from records import Records

titles = {
    "sport": "Sports Distribution",
    "gender": "Gender Distribution",
    "fed": "Federate Status",
    "result": "Medical Fitness Results"
}

def generate(records: Records, query: str) -> tuple[str, dict]:
    years = {}
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
    result = {}
    for y, dist in years.items():
        if year is None or year == y or year == "all":
            for k, ids in dist.items():
                if k not in result:
                    result[k] = 0
                result[k] += len(ids)
        if year is not None and year == y:
            break
    return result

def getIds(years: dict, year: str = None) -> dict[str, set[str]]:
    result = {}
    for y, dist in years.items():
        if year is None or year == y or year == "all":
            for k, ids in dist.items():
                if k not in result:
                    result[k] = set()
                result[k] = result[k].union(ids)
        if year is not None and year == y:
            break
    return result

def convertKey(query: str, key: str) -> str:
    if key == "M":
        return "Male"
    elif key == "F":
        return "Female"
    elif key == "true":
        return "Pass" if query == "result" else "True"
    elif key == "false":
        return "Not Pass" if query == "result" else "False"
    else:
        return key

def writeHTML(query: str, years: dict):
    keys = list(years.keys())
    keys.append("all")
    for year in keys:
        filename = "output/"+query+f"{year if year!='all' else 'total'}.html"
        freq = getFrequency(years, year)
        ids = getIds(years, year)
        with open(filename, "w") as f:
            f.writelines("<h1>"+titles[query]+f" {year if year!='all' else 'Total'} "+"</h1>")
            for key in freq.keys():
                f.writelines(f"<h2>{'='*10} {convertKey(query,key)} [{freq[key]}] {'='*10}</h2>\n<ul>\n")
                for id in ids[key]:
                    f.writelines("\t<li>"+id+"</li>\n")
                f.writelines("</ul>")
