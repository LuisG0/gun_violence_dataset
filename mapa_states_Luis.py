import pandas as pd

incidents = pd.read_csv('gun_violence_dataset/incidents_dataset.csv')
incidents = incidents.drop(labels=['Unnamed: 0'], axis=1,errors='ignore')
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
#incidents = incidents.query("year == 2014 & month == 1")

incidents_per_state = incidents.groupby(["code","state","month/year"], as_index=False)
incidents_map = incidents_per_state["n_injured"].agg(['sum','count']).rename(columns={'count':'n_incidents','sum':'n_injured'})
incidents_map["n_killed"] = incidents_per_state["n_killed"].agg(['sum']).rename(columns={'sum':'n_killed'})["n_killed"]
incidents_map = incidents_map.reset_index()

def plot_map(df, col, pal):
    df = df[df["n_incidents"]>0]
    fig = px.choropleth(df, locations="code", locationmode='USA-states', 
                  color=col, hover_name="state", 
                  title=col, hover_data=["n_injured","n_killed","n_incidents"], 
                  color_continuous_scale=pal,
                  animation_frame="month/year",
                  projection="natural earth",
                  scope="north america")
    fig.update_coloraxes(cmax =df[col].max(),cmin =df[col].min())
    fig.show()


plot_map(incidents_map, 'n_injured', 'Reds') #n_injured, n_killed or n_incidents

