import pandas as pd
from datetime import datetime

date_input = "30/08/2010 13:43"
serialNo = 'AU000000AFI5'

date_input = datetime.strptime(date_input, '%d/%m/%Y %H:%M')
# print(date_input)

# python -m pip install pandas

output = \
{
	"shifra" : "",
	"qmimi_bleres" : "",
	"qmimi_shites" : "",
}
output["shifra"] = serialNo

data = pd.read_csv("StockData.csv", sep=",", parse_dates=['Date'])
data['Date'] = data['Date'].dt.floor('Min')
data['Date_Input'] = date_input
data['Difference'] = 0

for index, row in data.iterrows():
    data.at[index, 'Difference'] = ((date_input - row.Date).total_seconds()//60)
  
data = data[(data['Difference'] >= 0) & (data["SerialNo"] == serialNo)]
data.sort_values(by=['Difference'], inplace=True, ascending=True)
data = data[data['Difference'] >= 0]
price_exist_len = len(data.index)
if price_exist_len > 0:    
    data.sort_values(by=['No'], inplace=True, ascending=False)   
    result = data.head(1)
    output['qmimi_bleres'] = result["CostPrice"].item()
    output['qmimi_shites'] = result["SalePrice"].item()

print(output)