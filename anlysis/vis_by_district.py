from old_code.get_data import get_district_data, transform_df
import plotly.express as px


series_id = {'jerusalem': '60000', 'north': '60100', 'haifa': '60200', 'center': '60300', 'tel_aviv': '60400', 'south': '60500'}
df = get_district_data(series_id)
df = transform_df(df)
fig = px.line(df, y="relative_price", color='district')
fig.show()


