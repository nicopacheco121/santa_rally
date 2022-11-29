import pandas as pd
from api_yfinance import yfinance_data
import matplotlib.pyplot as plt


def run_monthly(data_copy):
    data = data_copy.copy()

    # Filter by monthly values Nov and Dic
    data = data.resample('M').ffill()
    data.reset_index(inplace=True)
    data = data[(data['Date'].dt.month == 11) | (data['Date'].dt.month == 12)]

    # Calculate monthly result
    data['Prev_Close'] = data['Close'].shift()
    data['change'] = round((data['Close'] / data['Prev_Close'] - 1) * 100, 2)

    # Filter and clean data
    data.dropna(inplace=True)
    data = data[(data['Date'].dt.month == 12)]
    data.set_index('Date', inplace=True)

    return data


def run_two_weeks(data_copy):
    data = data_copy.copy()

    # Complete the index to have always days 15 and 31
    data = data.asfreq('D')
    data = data.fillna(method='ffill')

    # Filter by month 12 and days 15 and 31
    data.reset_index(inplace=True)
    data = data[(data['Date'].dt.month == 12) & ((data['Date'].dt.day == 15) | (data['Date'].dt.day == 31))]

    # Calculate result
    data['Prev_Close'] = data['Close'].shift()
    data['change'] = round((data['Close'] / data['Prev_Close'] - 1) * 100, 2)

    # Filter and clean data
    data.dropna(inplace=True)
    data = data[(data['Date'].dt.day == 31)]
    data.set_index('Date', inplace=True)

    return data


def box_plot(data):

    columns = list(data.columns)

    plt.style.use('dark_background')

    # Create the plot
    fix, ax = plt.subplots(figsize=(14, 6))

    # Create the boxplot
    bp = ax.boxplot(data, vert=True, whis=1.5, showmeans=True, showfliers=True)
    line = ax.plot([1, len(columns)], [0, 0], 'k--', lw=1, color='white')
    plt.xticks([i for i in range(1, len(columns)+1)], columns)

    plt.show()


def run():
    # Get the data
    data = yfinance_data(['SPY'], interval='1d', years_data=30)
    data = data.loc[:, ['Close']]

    # Make operations
    data_monthy = run_monthly(data_copy=data)
    data_two_weeks = run_two_weeks(data_copy=data)

    print(f'The monthly analys mean is {data_monthy.change.mean()} and the two weeks analys mean is {data_two_weeks.change.mean()}')

    # Arragement for the plot
    data_concat = pd.DataFrame()
    data_concat['change_monthy'] = data_monthy['change']
    data_concat['change_two_weeks'] = data_two_weeks['change']
    box_plot(data=data_concat)


if __name__ == '__main__':

    run()