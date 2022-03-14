import pandas as pd
import numpy as np
incidents = pd.read_csv('gun_violence_dataset/incidents_dataset.csv')
incidents = incidents.drop(labels=['Unnamed: 0'], axis=1,errors='ignore')
import datetime
incidents["month"] = incidents["date"].apply(lambda date: datetime.datetime.strptime(date, "%Y-%m-%d").month)
incidents["year"] = incidents["date"].apply(lambda date: datetime.datetime.strptime(date, "%Y-%m-%d").year)
incidents["month/year"] = incidents["month"].astype(str) + "/" + incidents["year"].astype(str)
incidents["city, state"] = incidents["city_or_county"] + ", " + incidents["state"]
incidents["n_killed_group"] = pd.cut(incidents.n_killed,bins=[-1,0,3,7,np.inf],labels=["0","1-3","4-7","8+"])
print(incidents.query("month/year == 6/2016").sort_values("n_killed_group"))
incidents = incidents.query("year != 2013")
incidents = incidents.query("year != 2018")

#incidents = incidents.query("month/year == 6/2016")
scale = 1
incidents["size"] = (incidents["n_injured"]+1) * scale 

import plotly.express as px
import plotly.graph_objects as go
fig = px.scatter_geo(incidents, lat="latitude",lon="longitude",
                     hover_name="city, state",
                     size="size",
                     size_max=50,
                     hover_data=["n_killed","n_injured"],
                     animation_frame="month/year",
                     projection="natural earth",
                     scope="north america",
                     opacity = 0.4,
                     color="n_killed",
                     color_continuous_scale = "Turbo",#["#34eb89","#dcff33","#ff2655","#9e0022"],
                     title = "Incidentes con armas de fuego"
                    #  color="n_killed_group",
                    #  color_discrete_sequence  =["#919090","#ff8aa3","#ff2655","#9e0022"]
                     )
fig.update_coloraxes(cmax =incidents["n_injured"].max(),cmin =0)
                     
fig.show()