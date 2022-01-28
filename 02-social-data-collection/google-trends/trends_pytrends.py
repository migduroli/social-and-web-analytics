from pytrends.request import TrendReq
import plotly.express as px
import pandas as pd

pytrends = TrendReq(hl='en-US', tz=360)

kw_list = ["machine learning"]

pytrends.build_payload(kw_list, cat=0, timeframe='today 12-m')


data = pytrends.interest_over_time()
data = data.reset_index()


fig = px.line(
    data,
    x="date",
    y=['machine learning'],
    title='Keyword Web Search Interest Over Time'
)
fig.show()

pytrends.get_historical_interest(
    kw_list,
    year_start=2022,
    month_start=1,
    day_start=1,
    hour_start=0,
    year_end=2022,
    month_end=1,
    day_end=10,
    hour_end=0,
    cat=0,
    sleep=0
)

by_region = pytrends.interest_by_region(
    resolution='COUNTRY',
    inc_low_vol=True,
    inc_geo_code=False
)

by_region.head(10)


keywords = pytrends.suggestions(keyword='Business Intelligence')
df = pd.DataFrame(keywords)
print(df)
