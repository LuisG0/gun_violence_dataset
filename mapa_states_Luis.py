from matplotlib.pyplot import text
import pandas as pd

incidents = pd.read_csv('gun_violence_dataset/incidents_dataset.csv')
incidents = incidents.drop(labels=['Unnamed: 0'], axis=1,errors='ignore')

population = pd.read_csv('data/nst-est2019-alldata.csv')
population = population[["NAME","POPESTIMATE2017"]].rename(columns={"NAME":"state","POPESTIMATE2017":"pop"})


import datetime
incidents["month"] = incidents["date"].apply(lambda date: datetime.datetime.strptime(date, "%Y-%m-%d").month)
incidents["year"] = incidents["date"].apply(lambda date: datetime.datetime.strptime(date, "%Y-%m-%d").year)
incidents["month/year"] = incidents["month"].astype(str) + "/" + incidents["year"].astype(str)

import plotly.express as px
incidents = incidents.query("year != 2013")
incidents = incidents.query("year != 2018")

def state2code(df):
    '''
    Transform USA states to 2 letters code.
    '''
    import json
    with open('state2Code.json') as json_file:
        codeDicts = json.load(json_file)
    df["code"] = df["state"].apply(lambda x: codeDicts[x])
    return df

incidents = state2code(incidents)

incidents_per_state = incidents.groupby(["code","state","month/year"], as_index=False)
incidents_map = incidents_per_state["n_injured"].agg(['sum','count']).rename(columns={'count':'n_incidents','sum':'n_injured'})
incidents_map["n_killed"] = incidents_per_state["n_killed"].agg(['sum']).rename(columns={'sum':'n_killed'})["n_killed"]
incidents_map = incidents_map.reset_index()

# Get incidents per million people
incidents_map = incidents_map.join(population.set_index('state'),on='state')
incidents_map["incidents_per_1M"] = incidents_map["n_incidents"] / incidents_map["pop"] * 1000000
incidents_map["injuried_per_1M"] = incidents_map["n_injured"] / incidents_map["pop"] * 1000000
incidents_map["killed_per_1M"] = incidents_map["n_killed"] / incidents_map["pop"] * 1000000

def plot_map(df, col, pal):
    df = df[df["n_incidents"]>0]
    fig = px.choropleth(df, locations="code", locationmode='USA-states', 
                  color=col,
                  hover_name="state", 
                  hover_data=["n_injured","n_killed","n_incidents"], 
                  color_continuous_scale=pal,
                  animation_frame="month/year",
                  projection="natural earth",
                  scope="north america",
                  title="Número de incidentes con armas por cada millón de habitantes"
                  )
    fig.update_coloraxes(cmax =df[col].max(),cmin =df[col].min())
    fig.show()


plot_map(incidents_map, 'incidents_per_1M', 'Reds') #n_injured, n_killed or n_incidents

