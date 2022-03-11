import re
from records import Records

class YearDistribution:
    def __init__(self,records:Records,query:str):
        self.__years = {}
        if query!="gender" and query!="sport" and query!="fed" and query!="result":
            return
        self.__query = query
        for record in records.values():
            year = re.findall(r'^\d+',record.data["date"])[0]
            if year not in self.__years:
                self.__years[year] = {}
            if record.data[query] not in self.__years[year]:
                self.__years[year][record.data[query]] = set()
            self.__years[year][record.data[query]].add(record.data["id"])

    def frequency(self,year:str=None) -> dict[str,int]:
        result = {}
        for y,dist in self.__years.items():
            if year is None or year==y: 
                for k,ids in dist.items():
                    if k not in result:
                        result[k] = 0
                    result[k] += len(ids)
            if year is not None and year==y:
                break
        return result

    def ids(self,year:str=None) -> dict[str,set[str]]:
        result = {}
        for y,dist in self.__years.items():
            if year is None or year==y: 
                for k,ids in dist.items():
                    if k not in result:
                        result[k] = set()
                    result[k] = result[k].union(ids)
            if year is not None and year==y:
                break
        return result

    def writeHTML(self):
        for year in self.__years.keys():
            filename = "output/"+self.__query+f"{year}.html"
            freq = self.frequency(year)
            ids = self.ids(year)
            with open(filename,"w") as fp:
                fp.writelines("<h1>"+year+"</h1>")
                for key in freq.keys():
                    fp.writelines(f"<h2>{'='*10} {key} [{freq[key]}] {'='*10}</h2>\n<ul>\n")    
                    for id in ids[key]:
                        fp.writelines("\t<li>"+id+"</li>\n")
                    fp.writelines("</ul>")
