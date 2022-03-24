import re
from records import Records,MedicalRecord
import yeardist
import plotly.graph_objects as go

def readCSV(filename:str) -> Records:
    records = {}
    with open(filename, "r") as fp:
        pattern = re.compile(r"""
            ^                            # start of string
            (?P<id>\w+),                 # _id
            (?P<index>\d+),              # index
            (?P<date>\d{4}-\d{2}-\d{2}), # dataEMD
            (?P<firstname>\w+),          # nome/primeiro
            (?P<lastname>\w+),           # nome/último
            (?P<age>[1-9]\d?),           # idade
            (?P<gender>[FM]),            # género
            (?P<city>\w+),               # morada
            (?P<sport>\w+),              # modalidade
            (?P<club>\w+),               # clube
            (?P<email>[^,]+),            # email
            (?P<fed>true|false),         # federado
            (?P<result>true|false)       # resultado
            $                            # end of string
        """, re.X)
        for line in fp.readlines():
            match = pattern.match(line)
            if match:
                entry = MedicalRecord(match.groupdict())
                records[entry.data["id"]] = entry
        print("$!> CSV FILE HAS BEEN READ!")
    return records

def writeHTML_records(records:Records,filename:str):
    with open(filename,"w") as fp:
        sortDate = list(records.values())
        sortDate.sort(reverse=True)
        for record in sortDate:
            fp.write(record.markupify())
        print(f'$!> Records written to {filename}')

def printRecords(records:Records):
    for record in records.values():
        print(record)
    print(f'{records.__len__()} total records')

# returns a list containing result for each year query
def yearDistributions(records:Records) -> list[tuple[str,dict[str,dict]]]:
    queries = "gender sport fed result".split()
    result = []
    for q in queries:
        result.append(yeardist.generate(records,q))
    return result

def piechart(filename:str,title_:str,labels_:list[str],values_:list[int]):
    colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
    hoverlabel = ("Frequency: "*len(labels_)).split()
    fig = go.Figure(
        data=[go.Pie(
                labels=labels_,
                values=values_,
                showlegend=False,
                text=hoverlabel,
                hovertemplate="%{text} %{value}<extra></extra>"
            )
        ],
        layout=go.Layout(
            height=500,
            width=500,
            hoverlabel=dict(font_size=16)
        )
    )
    fig.update_traces(
        hoverinfo='text+value',
        textinfo='label+percent',
        textfont_size=20,
        marker=dict(colors=colors, line=dict(color='#000000', width=2)),
        title=title_,
        title_font=dict(size=30),
    )
    fig.show()
    fig.write_html(filename)
    fig.write_image(filename.replace("html","jpeg"))
    #help(go.Pie)

def yearGraphs(query:str,years:dict[str,dict[str,list[str]]]):
    keys = list(years.keys())
    keys.append("all")
    for year in keys:
        freqs = yeardist.getFrequency(years,year)
        labels,values=[],[]
        for l,v in freqs.items():
            l=yeardist.convertKey(query,l)
            labels.insert(0,l)
            values.insert(0,v)
        y="Total" if year=="all" else year
        filename="output/resources/"+query+y+"_chart.html" 
        title=yeardist.titles[query]+" "+y
        if(query=="result"):
            piechart(filename,title,labels,values)

def main():
    records = readCSV("../emd.csv")
    queryB,queryC,queryF,queryG = yearDistributions(records)

    writeHTML_records(records, "output/list.html")
    yeardist.writeHTML(*queryB)
    yeardist.writeHTML(*queryC)
    yeardist.writeHTML(*queryF)
    yeardist.writeHTML(*queryG)
    
    yearGraphs(*queryG)

main()
