import pandas as pd
from datetime import date, datetime
import models as m

# pd.options.display.max_rows = 9999

# date_input = "12/07/2011 12:47"
# serialNo = 'NZTPWDT100C7'
# Rezultati i pritur (No. 616306) :
# 'shifra': 'NZTPWDT100C7', 'data': Timestamp('12/07/2011 12:32:25'),
# 'qmimi_bleres': 6.65, 'qmimi_shites': 6.6
# Rezultati aktual:
# 'shifra': 'NZTPWDT100C7', 'data': Timestamp('2011-07-12 10:05:00'), 'qmimi_bleres': '', 'qmimi_shites': 6.25

# date_input = "12/07/2011 12:47"  # 30/12/2011 13:43
# serialNo = 'NZTPWDT100C7'  # NZTPWDT100C7  #AU000000AFI5


def get_stock(serialNo, date_input):
    # date_input = "12/07/2011 12:47"  # 30/12/2011 13:43
    # serialNo = 'NZTPWDT100C7'  # NZTPWDT100C7  #AU000000AFI5

    date_input = datetime.strptime(date_input, '%d/%m/%Y %H:%M')
    # print(date_input, type(date_input),
    #       date_input.date(), type(date_input.date()))

    # python -m pip install pandas

    m.api_result["shifra"] = serialNo   
    m.api_result["date_input"] = date_input

    # data = pd.read_csv("Stock_quotes_2011.csv", sep=",", parse_dates=['Date'])
    # data = pd.read_csv("Stock_quotes_2011.csv", sep=",", index_col="No")
    data = pd.read_csv("Stock_quotes_2011.csv", sep=",")
    data['Date_Input'] = date_input
    data['Difference'] = 0
    data = data[data["SerialNo"].str.strip().str.lower() ==
                serialNo.strip().lower()]
    # df = data[data["No"] == 616306]
    # print(df)
    # print(data.loc['No'])
    # print(data.iloc['616306'])
    # subset = movies_df[['genre', 'rating']]
    # df[df['date'].dt.month == 12]

    # data['Date'] = pd.to_datetime(data.Date)
    data['Date'] = pd.to_datetime(data['Date'], format="%d/%m/%Y %H:%M")

    # data['Date'] = data['Date'].dt.floor('Min')
    print(data)
    # print(data.info())

    # data = data[(data['Date'].dt.date == date_input.date()) & (data["SerialNo"] == serialNo)]
    # data = data[data['Date'].dt.date == date_input.date()]
    # data = data[data['Date'].dt.to_period('M') == '2011-07']
    # data = data.index[data['Date'].dt.date < date_input.date()]
    # df = data[data["No"] == 616306]
    # print(df)

    # print("Data", data['Date'], data['Date'].dt.date, date_input.date())
    # print("DATA", data)

    for index, row in data.iterrows():
        data.at[index, 'Difference'] = (
            (date_input - row.Date).total_seconds()//60)

    # print(data)

    # data = data[(data['Difference'] >= 0) & (data["SerialNo"] == serialNo)]
    data = data[data['Difference'] >= 0]
    data.sort_values(by=['Difference'], inplace=True, ascending=True)
    # print(data)
    data = data[data['Difference'] >= 0]
    price_exist_len = len(data.index)
    if price_exist_len > 0:
        data.sort_values(by=['No'], inplace=True, ascending=False)
        result = data.head(1)
        m.api_result['qmimi_bleres'] = result["CostPrice"].item()
        m.api_result['qmimi_shites'] = result["SalePrice"].item()
        m.api_result["no"] = result["No"].item()
        m.api_result["date"] = result["Date"].item()

    return m.api_result

get_stock('NZTPWDT100C7', "12/07/2011 12:47")