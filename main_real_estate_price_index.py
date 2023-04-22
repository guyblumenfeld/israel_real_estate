import pandas as pd
import datetime


def fix_dates(df):
    df['year'] = df['year'].astype('string') # change the year column type
    df['year'] = df['year'].apply(lambda x: x[:-2]) # remove redundant '.0' from year values
    df['dt'] = df.apply(lambda x: datetime.datetime.strptime(x['year'] + "-" + x['month'], "%Y-%B"), axis=1) # read te date as a datetime object
    df = df[['dt','relative_price']] # keep only relevant columns
    df = df.set_index('dt')
    return df


def rename_columns(df):
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
    df.rename(columns = months_dic, inplace = True)
    df.rename(columns = {'שנה':'year'}, inplace = True)
    return df


def transform_df(df):
    # read the data from the df to a new df acording to the weird way the original df is strctured
    new_df = pd.DataFrame({'year':[],'month':[],'relative_price':[]})
    for index, row in df.iterrows():
        year = row['year']
        for item in row[2:].iteritems():
            dic = {'year':year, 'month':item[0], 'relative_price':item[1]}
            new_df = new_df.append(dic, ignore_index=True)
    return new_df


def get_main_price_index(source_path):
    df = pd.read_excel(source_path, skiprows=22, index_col=None)
    df = rename_columns(df)
    df = df[df['year'].apply(lambda x: not pd.isna(x))]
    df = transform_df(df)
    df = fix_dates(df)
    return df


def get_price_change(look_back_window=12, source_path=''):
    """
    :param look_back_window: how many months to the past to compare to.
    :return:
    """
    df = get_main_price_index(source_path)
    df['old_relative_price'] = df['relative_price'].shift(look_back_window)
    df['price_change'] = df.apply(lambda x: 100*(x['relative_price']-x['old_relative_price'])/x['old_relative_price'], axis=1)
    df = df[['price_change']]
    df = df[df['price_change'].apply(lambda x: not pd.isna(x))]
    df.reset_index(inplace=True)
    df = df.rename(columns={'dt':'date'})
    df['date'] = df['date'].apply(lambda x: x.strftime('%m-%Y'))
    return df


def get_calendar_year_change(look_back_window=12, source_path=''):
    """
    :param look_back_window: how many months to the past to compare to.
    :return:
    """
    df = get_main_price_index(source_path)
    df['old_relative_price'] = df['relative_price'].shift(look_back_window)
    df.reset_index(inplace=True)
    df = df.rename(columns={'dt': 'date'})
    df['date'] = df['date'].apply(lambda x: x.strftime('%m-%Y'))
    df['price_change'] = df.apply(lambda x: 100*(x['relative_price']-x['old_relative_price'])/x['old_relative_price'], axis=1)
    df = df[df['price_change'].apply(lambda x: not pd.isna(x))]
    if datetime.datetime.now().month != 12:
        last_know_price = list(df[df['relative_price'].apply(lambda x: not pd.isna(x))]['relative_price'])[-1]
        last_december_price = list(df[df['date'].apply(lambda x: x[:2]=='12')]['relative_price'])[-1]
        change_since_last_dec = 100 *(last_know_price - last_december_price) / last_december_price
        df = df[df['date'].apply(lambda x: x[:2]=='12')]
        df.loc[len(df)] = {'date':str(datetime.datetime.now().year), 'price_change':change_since_last_dec}
    df['date'] = df['date'].apply(lambda x: x[-4:])
    df['price_change'] = df['price_change'].apply(lambda x: str(round(float(x), 1)))
    df = df[['date', 'price_change']]
    return df.rename(columns={'date':'year'})


if __name__ == '__main__':
    source_path = "C:\\Users\\guybl\\OneDrive\מסמכים\\real estate data\\new houses prices.xlsx"
    df = get_calendar_year_change(look_back_window=12, source_path=source_path)
    df.to_csv("C:\\Users\\guybl\\OneDrive\מסמכים\\real estate data\\new houses yearly change.csv")
    print('done')

