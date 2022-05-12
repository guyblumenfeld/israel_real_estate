import pandas as pd
import datetime
from get_data import get_data_official_api


def rename_columns_cpi_df(df):
    months_dic = {
    'ינואר': 'January',
    'פברואר': 'February',
    'מרס': 'March',
    'אפריל': 'April',
    'מאי': 'May',
    'יוני': 'June',
    'יולי': 'July',
    'אוגוסט': 'August',
    'ספטמבר': 'September',
    'אוקטובר': 'October',
    'נובמבר': 'November',
    'דצמבר': 'December'}
    df.rename(columns=months_dic, inplace=True)
    df.rename(columns={'שנה':'year', 'פריט':'index_value'}, inplace=True)
    return df


def transform_cpi_df(df):
    # read the data from the df to a new df according to the weird way the original df is strctured
    new_df = pd.DataFrame({'year':[], 'month':[], 'index_value':[]})
    for index, row in df.iterrows():
        year = row['year']
        for item in row[2:].iteritems():
            dic = {'year':year, 'index_value':item[1], 'month':item[0]}
            new_df = new_df.append(dic, ignore_index=True)
    return new_df


def fix_dates(df):
    df['year'] = df['year'].astype('string') # change the year column type
    df['year'] = df['year'].apply(lambda x: x[:-2]) # remove redundant '.0' from year values
    df['dt'] = df.apply(lambda x: datetime.datetime.strptime(x['year'] + "-" + x['month'], "%Y-%B"), axis=1) # read te date as a datetime object
    df = df[['dt','index_value']] # keep only relevant columns
    df = df.set_index('dt')
    return df


def get_cpi(look_back_window=12):
    """
    :param look_back_window: how many months to the past to compare to.
    :return:
    """
    df = pd.read_excel("data\\cpi_from_the_website.xlsx", skiprows=22, index_col=None)
    df = rename_columns_cpi_df(df)
    df = transform_cpi_df(df)
    df = fix_dates(df)
    df['year_ago_monthly_index'] = df['index_value'].shift(look_back_window)
    df['inflation'] = df.apply(
        lambda x: 100 * (x['index_value'] - x['year_ago_monthly_index']) / x['year_ago_monthly_index'], axis=1)
    df = df[['inflation']]
    df = df.dropna(how='any', axis=0)
    return df



"""
import plotly.express as px
fig = px.line(df, y="y_over_y_inflation")
fig.show()
"""