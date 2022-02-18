from pytrends.request import TrendReq
import plotly.express as px
import pandas as pd

pytrends = TrendReq(hl='en-US', tz=360)

account = ["machine learning"]

pytrends.build_payload(
    account,
    cat=0,
    timeframe="today 12-m",
)

data = pytrends.interest_over_time()
data = data.reset_index()

fig = px.line(
    data,
    x="date",
    y=account,
    title='Web Search Interest Over Time'
)
fig.show()