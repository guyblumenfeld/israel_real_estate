import pandas as pd
import datetime
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt


def normalize_values(df_3):
    for srs in df_3['area_and_rooms'].drop_duplicates():
        start_value = df_3.loc[df_3['area_and_rooms'] == srs]['relative_price'][0]
        df_3.loc[df_3['area_and_rooms'] == srs, ['relative_price']] = 100*(df_3.loc[df_3['area_and_rooms'] == srs, ['relative_price']] / start_value)
    return df_3


def fix_dates(df):
    df['year'] = df['year'].astype('string') # change the year column type
    df['year'] = df['year'].apply(lambda x: x[:-2]) # remove redundant '.0' from year values
    quarters_dic = {"1":"01","2":"04", "3":"07", "4":"10"}
    df['q'] = df['q'].astype("string")
    df['month'] = df['q'].apply(lambda x: quarters_dic[x[1]])
    df['dt'] = df.apply(lambda x: datetime.datetime.strptime(x['year'] + "-" + x['month'], "%Y-%m"), axis=1) # read te date as a datetime object
    df = df.set_index('dt')
    return df


def select_cols_and_fix_types(df_0):
    df_o = df_0[['relative_price', 'area_and_rooms']]
    df_0['relative_price'] = df_0['relative_price'].apply(lambda x: x.replace(",", "").replace("-", ""))
    df_0.loc[df_0['relative_price'] == "", 'relative_price'] = 0
    df_0['relative_price'] = pd.to_numeric(df_0['relative_price'])
    df_0 = df_0[['relative_price', 'area_and_rooms']]
    return df_0


def px_vis_areas_averages(df_1):
    all_areas = ['1-2 (סך הכל)',
     '3-2.5 (סך הכל)',
     '4-3.5 (סך הכל)',
     '5-4.5 (סך הכל)',
     '6-5.5 (סך הכל)']
    all_areas_averages = df_1.loc[df_1['area_and_rooms'].isin(all_areas)]
    fig = px.line(all_areas_averages, y="relative_price", color='area_and_rooms') # , line_shape = 'spline'
    fig.show()


def sns_vis_all_areas_averages_line(df_2):
    # plot 1
    all_areas = ['1-2 (סך הכל)',
     '3-2.5 (סך הכל)',
     '4-3.5 (סך הכל)',
     '5-4.5 (סך הכל)',
     '6-5.5 (סך הכל)']
    all_areas_averages = df_2.loc[df_2['area_and_rooms'].isin(all_areas)]
    all_areas_averages['area_and_rooms'] = all_areas_averages['area_and_rooms'].apply(lambda x: x[0:3])
    print(all_areas_averages)
    all_areas_averages.rename(columns={'area_and_rooms': 'מספר חדרים'[::-1]}, inplace=True)
    all_areas_averages = all_areas_averages.reset_index()
    sns.lineplot(data=all_areas_averages, x="dt", y="relative_price", hue='מספר חדרים'[::-1])
    plt.xlabel("תאריך"[::-1])
    plt.ylabel("מחיר יחסי"[::-1])
    plt.show()


def sns_vis_all_areas_averages_total_change_bar_plot(df_2):
    # plot 2
    all_areas = ['1-2 (סך הכל)',
     '3-2.5 (סך הכל)',
     '4-3.5 (סך הכל)',
     '5-4.5 (סך הכל)',
     '6-5.5 (סך הכל)']
    all_areas_averages = df_2.loc[df_2['area_and_rooms'].isin(all_areas)]
    all_areas_averages['area_and_rooms'] = all_areas_averages['area_and_rooms'].apply(lambda x: x[0:3])
    df = pd.DataFrame({'number of rooms':[], 'total_change':[]})
    for room_number in all_areas_averages['area_and_rooms'].drop_duplicates():
        temp_df = all_areas_averages.loc[all_areas_averages['area_and_rooms'] == room_number]
        start_price = temp_df['relative_price'][0]
        end_price = temp_df['relative_price'][-1]
        total_change = (end_price - start_price) / start_price
        total_change = round(total_change, 4)
        dic = {'number of rooms': room_number, 'total_change': total_change}
        df = df.append(dic, ignore_index=True)
    df['number of rooms'] = df['number of rooms'].astype("string")
    sns.barplot(x="number of rooms", y="total_change", data=df)
    plt.xlabel("מספר חדרים"[::-1])
    plt.ylabel("אחוז שינוי כולל"[::-1])
    plt.show()


def calculate_total_change_per_group(df):
    df_for_bars = pd.DataFrame({'area_and_rooms': [], 'total_change': []})
    for value in df['area_and_rooms'].drop_duplicates():
        temp_df = df.loc[df['area_and_rooms'] == value]
        start_price = temp_df['relative_price'].iloc[0]
        end_price = temp_df['relative_price'].iloc[-1]
        total_change = (end_price - start_price) / start_price
        total_change = round(total_change, 4)
        dic = {'area_and_rooms': value, 'total_change': total_change}
        df_for_bars = df_for_bars.append(dic, ignore_index=True)
    return df_for_bars


def extract_name_for_districts(name):
    if sum([x.isdigit() for x in name]) == 1:
        return "ממוצע"[::-1]
    elif "1-2" in name:
        return "1-2"
    else:
        return name[:6]


def line_plot_all_districts(df_8):
    districts = ['מחוז חיפה','מחוז מרכז','מחוז צפון' ,'מחוז ירושלים','מחוז תל אביב','מחוז דרום']
    sns.set_style(style="whitegrid")
    plt.figure(figsize=(15, 15))
    rows_counter = 1
    for district in districts:
        temp_df = df_8.loc[df_8['area_and_rooms'].str.contains(district)]
        temp_df['area_and_rooms'] = temp_df['area_and_rooms'].apply(lambda x: extract_name_for_districts(x))
        temp_df = temp_df.reset_index()
        plt.subplot(len(districts), 1, rows_counter)
        temp_df = temp_df.rename(columns={'area_and_rooms':"מספר חדרים" [::-1]})
        sns.lineplot(data=temp_df, x="dt", y="relative_price", hue="מספר חדרים"[::-1])
        plt.yticks([80, 90, 100, 110, 120])
        plt.title(district[::-1], fontsize=18)
        plt.legend(fontsize=8, loc='center',  bbox_to_anchor=(1.05, 0.5))  # set the legend outside the plot
        plt.ylabel("מחיר יחסי"[::-1])
        if rows_counter < len(districts):  # not the last plot
            plt.xlabel("")
        else:
            plt.xlabel("תאריך"[::-1])
        rows_counter += 1
    plt.subplots_adjust(hspace=.6)
    plt.show()


def bar_plot_all_districts(df_8):
    districts = ['מחוז חיפה','מחוז מרכז','מחוז צפון' ,'מחוז ירושלים','מחוז תל אביב','מחוז דרום']
    sns.set_style(style="whitegrid")
    plt.figure(figsize=(15, 15))
    rows_counter = 1
    for district in districts:
        temp_df = df_8.loc[df_8['area_and_rooms'].str.contains(district)]
        temp_df['area_and_rooms'] = temp_df['area_and_rooms'].apply(lambda x: extract_name_for_districts(x))
        df_for_total_change = calculate_total_change_per_group(temp_df)
        plt.subplot(len(districts), 1, rows_counter)
        df_for_total_change = df_for_total_change.rename(columns={'area_and_rooms': "מספר חדרים"[::-1]})
        print(df_for_total_change)
        sns.barplot(x= "מספר חדרים"[::-1], y="total_change", data=df_for_total_change)
        plt.yticks([0.1, 0.2, 0.3])
        plt.title(district[::-1], fontsize=18)
        plt.ylabel("אחוז שינוי כולל"[::-1])
        if rows_counter < len(districts):  # not the last plot
            plt.xlabel("")
        else:
            plt.xlabel("מספר חדרים"[::-1])
        rows_counter += 1
    plt.subplots_adjust(hspace=.6)
    plt.show()


def sns_line_for_one_group(df, values):
    temp_df = df.loc[df['area_and_rooms'].isin(values)]
    temp_df = temp_df.reset_index()
    sns.lineplot(data=temp_df, x="dt", y="relative_price", hue='area_and_rooms')
    plt.xlabel("תאריך"[::-1])
    plt.ylabel("מחיר יחסי"[::-1])
    plt.show()


def sns_bar_plot_for_one_group(df, values):
    filtered_df = df.loc[df['area_and_rooms'].isin(values)]
    df_for_bars = pd.DataFrame({'area_and_rooms': [], 'total_change': []})
    for value in filtered_df['area_and_rooms'].drop_duplicates():
        temp_df = filtered_df.loc[filtered_df['area_and_rooms'] == value]
        start_price = temp_df['relative_price'][0]
        end_price = temp_df['relative_price'][-1]
        total_change = (end_price - start_price) / start_price
        total_change = round(total_change, 4)
        dic = {'area_and_rooms': value, 'total_change': total_change}
        df_for_bars = df_for_bars.append(dic, ignore_index=True)
    sns.barplot(x="area_and_rooms", y="total_change", data=df_for_bars)
    plt.xlabel("מספר חדרים"[::-1])
    plt.ylabel("אחוז שינוי כולל"[::-1])
    plt.show()




df = pd.read_csv("data\\prices_by_city_and_rooms.csv")
df = fix_dates(df)
df = select_cols_and_fix_types(df)
df = normalize_values(df)

#bar_plot_all_districts(df)
#line_plot_all_districts(df)
# px_vis_areas_averages()
# sns_vis_all_areas_averages_line(df)
# sns_vis_all_areas_averages_total_change_bar_plot(df)
# sns_line_for_one_group(df, ['1-2 (סך הכל)', '3-2.5 (סך הכל)'])
# sns_bar_plot_for_one_group(df, ['1-2 (סך הכל)', '3-2.5 (סך הכל)'])
