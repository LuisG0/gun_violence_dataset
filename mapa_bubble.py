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

df = incidents

fig = px.scatter_geo(df, lat="latitude",lon="longitude",
                     hover_name="city_or_county",
                     size="n_injured",
                     animation_frame="month-year",
                     projection="natural earth",
                     scope="north america"
                     )
fig.show()