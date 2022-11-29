import datetime as dt
import yfinance as yf
import pandas as pd
from api_yfinance import data_etfs, yfinance_data
import matplotlib.pyplot as plt


def run_monthly(data_copy):
    data = data_copy.copy()

    data = data.resample('M').ffill()
    data.reset_index(inplace=True)
    data = data[(data['Date'].dt.month == 11) | (data['Date'].dt.month == 12)]

    data['Prev_Close'] = data['Close'].shift()
    data['change'] = round((data['Close'] / data['Prev_Close'] - 1) * 100, 2)

    data.dropna(inplace=True)
    data = data[(data['Date'].dt.month == 12)]
    data.set_index('Date', inplace=True)

    return data


def run_two_weeks(data_copy):

    data = data_copy.copy()
    data = data.asfreq('D')
    data = data.fillna(method='ffill')
    data.reset_index(inplace=True)

    data = data[(data['Date'].dt.month == 12) & ((data['Date'].dt.day == 15) | (data['Date'].dt.day == 31))]

    data['Prev_Close'] = data['Close'].shift()
    data['change'] = round((data['Close'] / data['Prev_Close'] - 1) * 100, 2)
    data.dropna(inplace=True)

    data = data[(data['Date'].dt.day == 31)]
    data.set_index('Date', inplace=True)

    return data

    # print(data)
    # print(data.change.mean())


def box_plot(data):

    columns = list(data.columns)

    plt.style.use('dark_background')

    fix, ax = plt.subplots(figsize=(14, 6))
    bp = ax.boxplot(data, vert=True, whis=1.5, showmeans=True, showfliers=True)
    line = ax.plot([1, len(columns)], [0, 0], 'k--', lw=1, color='white')
    plt.xticks([i for i in range(1, len(columns)+1)], columns)
    plt.show()




def run():
    data = yfinance_data(['SPY'], interval='1d', years_data=30)
    data.to_pickle('data_spy')

    # data = pd.read_pickle('data_spy')
    data = data.loc[:, ['Close']]

    data_monthy = run_monthly(data_copy=data)
    data_two_weeks = run_two_weeks(data_copy=data)
    # print(data_two_weeks)
    # print(data_two_weeks.change.mean())

    print(f'La media de data monthy es {data_monthy.change.mean()} y la media de la data two weeks es {data_two_weeks.change.mean()}')

    data_concat = pd.DataFrame()
    data_concat['change_monthy'] = data_monthy['change']
    data_concat['change_two_weeks'] = data_two_weeks['change']

    box_plot(data=data_concat)



if __name__ == '__main__':

    run()