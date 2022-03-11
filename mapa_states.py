import pandas as pd
import numpy as np

incidents = pd.read_csv('./data/incidents_dataset.csv')
import datetime
incidents["month"] = incidents["date"].apply(lambda date: datetime.datetime.strptime(date, "%Y-%m-%d").month)
incidents["year"] = incidents["date"].apply(lambda date: datetime.datetime.strptime(date, "%Y-%m-%d").year)
incidents["month-year"] = incidents["month"].astype(str) + "-" + incidents["year"].astype(str)

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
incidents_per_state = incidents.groupby(["code","state","month-year"], as_index=False)["n_injured"].sum().rename(columns={'sum':'n_injured'})
def plot_map(df, col, pal):
    df = df[df[col]>0]
    fig = px.choropleth(df, locations="code", locationmode='USA-states', 
                  color=col, hover_name="state", 
                  title=col, hover_data=[col], 
                  color_continuous_scale=pal,
                  animation_frame="month-year",
                  projection="natural earth",
                  scope="north america")
#     fig.update_layout(coloraxis_showscale=False)
    fig.show()


plot_map(incidents_per_state, 'n_injured', 'Reds')

