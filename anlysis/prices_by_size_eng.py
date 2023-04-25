import pandas as pd
from anlysis.prices_by_size import fix_dates, select_cols_and_fix_types, normalize_values
import seaborn as sns
import matplotlib.pyplot as plt


def vis_all_areas_averages_line(df):
    # plot 1
    all_areas = ['1-2 (סך הכל)',
     '3-2.5 (סך הכל)',
     '4-3.5 (סך הכל)',
     '5-4.5 (סך הכל)',
     '6-5.5 (סך הכל)']
    all_areas_averages = df.loc[df['area_and_rooms'].isin(all_areas)]
    all_areas_averages['area_and_rooms'] = all_areas_averages['area_and_rooms'].apply(lambda x: x[0:3])
    all_areas_averages.rename(columns={'area_and_rooms': 'Number of rooms'}, inplace=True)
    all_areas_averages = all_areas_averages.reset_index()
    ax = sns.lineplot(data=all_areas_averages, x="dt", y="relative_price", hue='Number of rooms')
    plt.xlabel("Date", fontsize=24)
    plt.ylabel("Price change (base 2017 = 100)", fontsize=16)
    ax.set_yticklabels(ax.get_yticks(), size=12)
    ax.legend(bbox_to_anchor=(0.25, 1), prop={'size': 15})
    plt.setp(ax.get_legend().get_title(), fontsize='20')  # for legend title
    ax.grid(axis='y')
    plt.show()


def vis_all_areas_averages_total_change_bar_plot(df_2):
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
    ax = sns.barplot(x="number of rooms", y="total_change", data=df)
    for i in ax.containers:
        ax.bar_label(i, )
    plt.xlabel("Number of rooms", fontsize=22)
    plt.ylabel("Total change", fontsize=22)
    plt.yticks([x * 0.025 for x in range(0, 10)], labels=[str(round(x * 0.025*100, 1))+'%' for x in range(0, 10)])
    plt.title("Total change from the start of 2017 to the end of 2021", fontsize=26)
    sns.set(font_scale=10)
    plt.show()


def extract_name_for_districts(name):
    if sum([x.isdigit() for x in name]) == 1:
        return "ממוצע"[::-1]
    elif "1-2" in name:
        return "1-2"
    else:
        return name[:6]


def line_plot_all_districts_one_joined_plot(df):
    districts = ['מחוז חיפה','מחוז מרכז','מחוז צפון' ,'מחוז ירושלים','מחוז תל אביב','מחוז דרום']
    dict = {'מחוז חיפה':'Haifa','מחוז מרכז':'The Center','מחוז צפון':'North' ,'מחוז ירושלים':'Jerusalem','מחוז תל אביב':'Tel-Aviv','מחוז דרום':'South'}
    sns.set_style(style="whitegrid")
    plt.figure(figsize=(15, 150))
    rows_counter = 1
    for district in districts:
        temp_df = df.loc[df['area_and_rooms'].str.contains(district)]
        temp_df['area_and_rooms'] = temp_df['area_and_rooms'].apply(lambda x: extract_name_for_districts(x))
        temp_df['area_and_rooms'] = temp_df['area_and_rooms'].apply(lambda x: "average" if x=="ממוצע"[::-1] else x)
        temp_df = temp_df.reset_index()
        plt.subplot(len(districts), 1, rows_counter)
        temp_df = temp_df.rename(columns={'area_and_rooms':"number of rooms"})
        sns.lineplot(data=temp_df, x="dt", y="relative_price", hue="number of rooms")
        plt.yticks([90, 100, 110, 120, 130])
        plt.title(dict[district], fontsize=18)
        plt.legend(fontsize=8, loc='center',  bbox_to_anchor=(1.05, 0.5))  # set the legend outside the plot
        plt.ylabel("Relative price")
        if rows_counter < len(districts):  # not the last plot
            plt.xlabel("")
        else:
            plt.xlabel("Date", fontdict={'size':'16'})
        rows_counter += 1
    plt.subplots_adjust(hspace=.6)
    plt.show()


def line_plot_all_districts(df):
    districts = ['מחוז חיפה','מחוז מרכז','מחוז צפון' ,'מחוז ירושלים','מחוז תל אביב','מחוז דרום']
    dict = {'מחוז חיפה':'Haifa','מחוז מרכז':'The Center','מחוז צפון':'North' ,'מחוז ירושלים':'Jerusalem','מחוז תל אביב':'Tel-Aviv','מחוז דרום':'South'}
    sns.set_style(style="whitegrid")
    plt.figure(figsize=(15, 150))
    rows_counter = 1
    for district in districts:
        temp_df = df.loc[df['area_and_rooms'].str.contains(district)]
        temp_df['area_and_rooms'] = temp_df['area_and_rooms'].apply(lambda x: extract_name_for_districts(x))
        temp_df['area_and_rooms'] = temp_df['area_and_rooms'].apply(lambda x: "average" if x=="ממוצע"[::-1] else x)
        temp_df = temp_df.reset_index()
        temp_df = temp_df.rename(columns={'area_and_rooms':"number of rooms"})
        sns.lineplot(data=temp_df, x="dt", y="relative_price", hue="number of rooms")
        plt.yticks([90, 100, 110, 120, 130], fontsize=14)
        plt.title(dict[district], fontsize=26)
        plt.legend(fontsize=14, loc='center',  bbox_to_anchor=(.1, 0.8))  # set the legend outside the plot
        plt.ylabel("Price change (base 2017 = 100)", fontsize=18)
        plt.xlabel("Date", fontsize=24)
        if rows_counter < len(districts):  # not the last plot
            plt.xlabel("")
        else:
            plt.xlabel("Date", fontdict={'size':'16'})
        rows_counter += 1
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


def bar_plot_all_districts(df):
    districts = ['מחוז חיפה','מחוז מרכז','מחוז צפון' ,'מחוז ירושלים','מחוז תל אביב','מחוז דרום']
    dict = {'מחוז חיפה':'Haifa','מחוז מרכז':'The Center','מחוז צפון':'North' ,'מחוז ירושלים':'Jerusalem','מחוז תל אביב':'Tel-Aviv','מחוז דרום':'South'}
    sns.set_style(style="whitegrid")
    plt.figure(figsize=(15, 15))
    rows_counter = 1
    for district in districts:
        temp_df = df.loc[df['area_and_rooms'].str.contains(district)]
        temp_df['area_and_rooms'] = temp_df['area_and_rooms'].apply(lambda x: extract_name_for_districts(x))
        temp_df['area_and_rooms'] = temp_df['area_and_rooms'].apply(lambda x: "average" if x == "ממוצע"[::-1] else x)
        df_for_total_change = calculate_total_change_per_group(temp_df)
        plt.subplot(len(districts), 1, rows_counter)
        df_for_total_change = df_for_total_change.rename(columns={'area_and_rooms': "Number of rooms"})
        sns.barplot(x="Number of rooms", y="total_change", data=df_for_total_change)
        plt.yticks([0.1, 0.2, 0.3])
        plt.title(dict[district], fontsize=20)
        plt.ylabel("")
        if rows_counter < len(districts):  # not the last plot
            plt.xlabel("")
        else:
            plt.xlabel("Number of rooms", fontsize=16)
        rows_counter += 1
    plt.subplots_adjust(hspace=.7)
    plt.ylabel("                                                                         Total change", fontsize=16)
    plt.show()


df = pd.read_csv("../data/prices_by_city_and_rooms.csv")
df = fix_dates(df)
df = select_cols_and_fix_types(df)
df = normalize_values(df)

#vis_all_areas_averages_line(df)
#vis_all_areas_averages_total_change_bar_plot(df)
line_plot_all_districts(df)
#bar_plot_all_districts(df)

"""
#import warnings
#warnings.filterwarnings('ignore')
warnings.filterwarnings(action='once')
"""