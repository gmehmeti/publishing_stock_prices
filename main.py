import pandas as pd
from datetime import date, datetime
import models as m

# pd.options.display.max_rows = 9999

def read_stock_data():
    data = pd.read_csv("Stock_quotes_2011.csv", sep=",")
    # data['Date_Input'] = date_input
    data['Difference'] = 0
    return data


def get_stock_by_serialno(serialNo: str, date_input: str):

    date_input = datetime.strptime(date_input, '%d/%m/%Y %H:%M')
    m.api_result["shifra"] = serialNo
    m.api_result["date_input"] = date_input

    data = read_stock_data()
    data['Date_Input'] = date_input
    data = data[data["SerialNo"].str.strip().str.lower() ==
                serialNo.strip().lower()]
    
    data['Date'] = pd.to_datetime(data.Date, dayfirst=True)
    data['Date'] = data['Date'].dt.floor('Min')

    for index, row in data.iterrows():
        data.at[index, 'Difference'] = (
            (date_input - row.Date).total_seconds()//60)

    data = data[data['Difference'] >= 0]
    data.sort_values(by=['Difference'], inplace=True, ascending=True)
    price_exist_len = len(data.index)
    if price_exist_len > 0:
        exists = 0 in data.Difference.values
        if exists:
            data = data[data['Difference'] == 0]
            data.sort_values(by=['No'], inplace=True, ascending=False)

        # print(data.head(10))
        result = data.head(1)
        result = result.fillna(0)
        m.api_result['qmimi_bleres'] = result["CostPrice"].item()
        m.api_result['qmimi_shites'] = result["SalePrice"].item()
        m.api_result["no"] = result["No"].item()
        m.api_result["date"] = result["Date"].item()

    return m.api_result


def get_stock_price(serialNo: str, date_input: str, take: int):

    date_input = datetime.strptime(date_input, '%d/%m/%Y %H:%M')
    data = read_stock_data()

    data['Date_Input'] = date_input
    data = data[data["SerialNo"].str.strip().str.lower() ==
                serialNo.strip().lower()]

    # data['Date'] = pd.to_datetime(data.Date, format='%d/%m/%Y %H:%M:%S')
    data['Date'] = pd.to_datetime(data.Date, dayfirst=True)
    data['Date'] = data['Date'].dt.floor('Min')

    for index, row in data.iterrows():
        data.at[index, 'Difference'] = (
            (date_input - row.Date).total_seconds()//60)

    # data["Difference"] = data["Difference"].apply(
    #     lambda cell: ((date_input - cell).total_seconds()//60))

    data = data[data['Difference'] >= 0]
    data.sort_values(by=['Difference'], inplace=True, ascending=True)
    price_exist_len = len(data.index)
    if price_exist_len > 0:
        result = data.head(take)
        result = result.fillna(0)
        # print(result)
        for index, row in result.iterrows():
            key = row.No
            output = {}
            output["no"] = key
            output["date"] = row["Date"]
            output["serialno"] = serialNo
            output['costprice'] = row["CostPrice"]
            output['saleprice'] = row["SalePrice"]
            output["date_input"] = date_input
            output['difference'] = row["Difference"]
            m.stock_price_model[str(key)] = output

    return m.stock_price_model


# print(get_stock_by_serialno('NZTPWDT100C7', "12/07/2011 12:47"))
# print(get_stock_price('NZTPWDT100C7', "12/07/2011 12:47", 10))
