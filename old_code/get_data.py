import pandas as pd
import datetime
import requests
import plotly.express as px


def get_code_list_all_areas_and_room_numbers():
    # create a list with all ids
    df = pd.read_excel("data\\by_city_and_rooms.xlsx", skiprows=20, index_col=None)
    code_list = list(df['קוד'])
    return code_list


def read_data(code_list):
    problematic_codes = []
    new_df = pd.DataFrame({'year':[],'q':[],'relative_price':[], 'area_and_rooms':[]})
    url = 'https://boardsgenerator.cbs.gov.il/Handlers/Prices/GridHandler.ashx?mode=Init'
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',}
    for code in code_list:
        data = {'query': '{"model":null,"dataTypeId":"2","subjectId":"165","SeriesCodes":[' + str(code) +'],"Fyear":2010,"Tyear":2021,"IndicesTypeOption":"Prices","Language":"Hebrew","Fquarter":3,"Tquarter":4}'}
        try:
            response = requests.post(url, headers=headers, data=data).json()
            df = pd.DataFrame(response['data'])
            for index, row in df.iterrows():
                year = row['Year']
                area_and_rooms = row['ItemApartment']
                for item in row[5:-1].iteritems():
                    dic = {'area_and_rooms':area_and_rooms, 'year':year, 'q':item[0], 'relative_price':item[1]}
                    new_df = new_df.append(dic, ignore_index=True)
        except:
            problematic_codes.append(code)
    if problematic_codes:
        print(f"an issue occurred trying to pull these codes: {problematic_codes}")
    else:
        print("pulled data for all codes.")
    return new_df


def fix_dates(df):
    df['year'] = df['year'].astype('string') # change the year column type
    df['year'] = df['year'].apply(lambda x: x[:-2]) # remove redundant '.0' from year values
    quarters_dic = {"1":"01","2":"04", "3":"07", "4":"10"}
    df['q'] = df['q'].astype("string")
    df['month'] = df['q'].apply(lambda x: quarters_dic[x[1]])
    df['dt'] = df.apply(lambda x: datetime.datetime.strptime(x['year'] + "-" + x['month'], "%Y-%m"), axis=1) # read te date as a datetime object
    df = df.set_index('dt')
    return df


def select_cols_and_fix_types(df):
    df = df[['relative_price', 'area_and_rooms']]
    df['relative_price'] = df['relative_price'].apply(lambda x: x.replace(",", "").replace("-",""))
    df['relative_price'] = df['relative_price'].apply(lambda x: 0 if x == "" else x)
    df['relative_price'] = df['relative_price'].astype("double")
    return df


def get_data_official_api(series_id):
    try:
        df = pd.DataFrame()
        for id in series_id.keys():
            url = f'https://api.cbs.gov.il/index/data/price?id={series_id[id]}&format=json&download=false'
            resp = requests.get(url).json()
            data = resp['month'][0]['date']
            col = pd.DataFrame.from_records(data)              # a column in the result df
            col['E'] = col['currBase'].apply(pd.Series).value
            col['date'] = col['month'].map(str) + '/' + col['year'].map(str)
            col = col[['date','E']]
            col = col.set_index('date')
            col.columns = [id]
            col.index = pd.to_datetime(col.index)
            col = col.sort_index()
            col.index = col.index.strftime('%m/%Y')
            df = pd.concat([df, col], axis=1)
        df = df.reset_index()
        df['date'] = df['date'].apply(lambda x: datetime.datetime.strptime(str(x), "%m/%Y"))
        df = df.set_index('date')
        return df
    except Exception as e:
        print('problem getting data from lamas')


def transform_df(df):
    new_df = pd.DataFrame({'date':[], 'district':[], 'relative_price':[]})
    df = df.reset_index()
    for index, row in df.iterrows():
        date = row['date']
        for item in row[1:].iteritems():
            dic = {'date':date, 'district':item[0], 'relative_price':item[1]}
            new_df = new_df.append(dic, ignore_index=True)
    new_df = new_df.set_index("date")
    return new_df



#  ----- unofficial api
"""
df = read_data(get_code_list())
df.to_csv("prices_by_city_and_rooms.csv")
df = fix_dates(df)
df = select_cols_and_fix_types(df)
"""

# ---- using official api
"""
series_id = {'jerusalem': '60000', 'north': '60100', 'haifa': '60200', 'center': '60300', 'tel_aviv': '60400', 'south': '60500'}
df = get_data_official_api(series_id)
df = transform_df(df)
fig = px.line(df, y="relative_price", color='district')
fig.show()
"""

