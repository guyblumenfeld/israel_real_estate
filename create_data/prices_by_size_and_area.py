import pandas as pd
from datetime import datetime

"""
instructions:
go to - https://www.cbs.gov.il/he/Statistics/Pages/%D7%9E%D7%97%D7%95%D7%9C%D7%9C%D7%99%D7%9D/%D7%9E%D7%97%D7%95%D7%9C%D7%9C-%D7%9E%D7%97%D7%99%D7%A8%D7%99%D7%9D.aspx
press on - prices -> index and prices from the apartments market -> average prices city, size and area 
"""


def translate_columns(df:pd.DataFrame)->pd.DataFrame:
    dic = {'קוד':'code', 'אזור וחדרים בדירה':'area_and_rooms', 'שנה':'year','ינואר-מרס':'jan-march',
           'אפריל-יוני':'april-jun', 'יולי-ספטמבר':'july-sep', 'אוקטובר-דצמבר':'oct-dec',
           'ממוצע שנתי': 'yearly_average'}
    return df.rename(columns=dic)


def get_clean_data(file_path:str)->pd.DataFrame:
    df = pd.read_excel(file_path, skiprows=20)
    df = df = df.replace('-', 0)
    df = translate_columns(df)
    df[['jan-march', 'april-jun', 'july-sep', 'oct-dec', 'yearly_average']] = df[['jan-march', 'april-jun', 'july-sep', 'oct-dec', 'yearly_average']].astype('float')
    df[['year', 'code']] = df[['year', 'code']].astype('int')
    return df


def flatten_data_by_codes(df, codes):
    df = df[df['code'].isin(codes)]
    months_dic = {'jan-march':1, 'april-jun':4, 'july-sep':7, 'oct-dec':10}
    dfs = []
    for code in codes:
        df_temp = df[df['code']==code]
        label = list(df_temp['area_and_rooms'])[0]
        new_df = pd.DataFrame(columns=[label, 'dt'])
        for i, row in df_temp.iterrows():
            for period in ['jan-march', 'april-jun', 'july-sep', 'oct-dec']:
                print()
                res_row = {label:row[period], 'dt':datetime(year=row['year'], month=months_dic[period], day=1)}
                new_df.loc[len(new_df)] = res_row
        dfs.append(new_df.copy(deep=True))
    result_df = dfs[0]
    for df in dfs[1:]:
        result_df = result_df.merge(df, how='left', left_on='dt', right_on='dt')
    return result_df


def normalize(df):
    cols = list(df.columns)
    cols.remove('dt')
    for col in cols:
        df[col] = round(100* df[col] / list(df[col])[0], 2)
    return df


def get_heb_date_label(dt):
    label = 'רבעון '
    if dt.month == 1:
        label = label + '1'
    elif dt.month == 4:
        label = label + '2'
    elif dt.month == 7:
        label = label + '3'
    if dt.month == 10:
        label = label + '4'
    label = label + '-' + str(dt.year)
    return label


def create_data_by_codes(source_path, codes):
    df = get_clean_data(source_path)
    df = flatten_data_by_codes(df=df, codes=codes)
    df = df.sort_values(by=['dt'], ascending=True)
    df = normalize(df)
    for col in df.columns:
        if col != 'dt':
            df[col] = df[col].apply(lambda x: x-100)
    df['dt_heb_label'] = df['dt'].apply(get_heb_date_label)
    return df


if __name__ == '__main__':
    file_path = "C:\\Users\\guybl\\OneDrive\\מסמכים\\real estate data\\prices_by_size_and_area.xlsx"
    codes_all_areas_by_rooms = [51010, 51030, 51050, 51070, 51090]
    codes_all_sizes_by_district = [51100, 51200, 51300, 51400, 51500, 51600]
    df = create_data_by_codes(source_path=file_path, codes=codes_all_sizes_by_district)
    df.to_excel("C:\\Users\\guybl\\OneDrive\\מסמכים\\real estate data\\prices_by_districts_clean.xlsx")

