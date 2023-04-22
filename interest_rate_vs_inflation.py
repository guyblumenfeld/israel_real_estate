from cpi import get_cpi
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns


if __name__ == '__main__':
    df_cpi = get_cpi().reset_index()
    df_interest = pd.read_csv("C:\\Users\\guybl\\Downloads\\interest_rates - Sheet1.csv")
    df_interest['date'] = df_interest['date'].apply(lambda x: datetime(year=int(x.split('/')[2]), month=int(x.split('/')[0]), day=int(x.split('/')[1])))
    #df = df_cpi.merge(df_interest)
    df_interest['interest'] = df_interest['interest']*0.85
    plt.plot(df_interest['date'], df_interest['interest'])
    plt.plot(df_cpi['dt'], df_cpi['inflation'])
    plt.show()


