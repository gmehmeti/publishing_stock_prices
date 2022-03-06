import pandas as pd
from datetime import datetime

date_input = "30/12/2011 13:43"
serialNo = 'AU000000AFI5'

date_input = datetime.strptime(date_input, '%d/%m/%Y %H:%M')
# print(date_input)

print(date_input.date())

# python -m pip install pandas

output = \
{
	"shifra" : "",
	"qmimi_bleres" : "",
	"qmimi_shites" : "",
}
output["shifra"] = serialNo

# data = pd.read_csv("Stock_quotes_2011.csv", sep=",", parse_dates=['Date'])
data = pd.read_csv("Stock_quotes_2011.csv", sep=",")
data['Date_Input'] = date_input
data['Difference'] = 0
data = data[data["SerialNo"] == serialNo]
print(data)
data['Date'] = pd.to_datetime(data.Date)
data['Date'] = data['Date'].dt.floor('Min')

# data = data[(data['Date'].dt.date == date_input.date()) & (data["SerialNo"] == serialNo)]
data = data[(data['Date'].dt.date == date_input.date())]
print(data)