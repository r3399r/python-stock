import requests
from bs4 import BeautifulSoup as BS
import pandas
import json

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
}
res = requests.get(
    "https://goodinfo.tw/StockInfo/EquityDistributionClassHis.asp?STOCK_ID=1304&DISPLAY_CAT=%E6%8C%81%E6%9C%89%E5%BC%B5%E6%95%B8%E5%8D%80%E9%96%93%E5%88%86%E7%B4%9A%E4%B8%80%E8%A6%BD(%E5%AE%8C%E6%95%B4)", headers=headers)
res.encoding = 'utf-8'
# print(res.text)

soup = BS(res.text, 'lxml')
data = soup.select_one('#divEquityDistributionClassHis')
# print(data)

dfs = pandas.read_html(data.prettify())
df = dfs[2]
df.columns = df.columns.get_level_values(1)

df = df[df['週別'] != '週別']
df = df.rename(columns={
    '週別': 'weekNo',
    '統計  日期': 'date',
    '收盤': 'price',
    '漲跌  (元)': 'priceChange',
    '漲跌  (%)': 'priceChangePercent',
    '＜1張': 'lt1',
    '≧1張  ≦5張': '1to5',
    '＞5張  ≦10張': '5to10',
    '＞10張  ≦15張': '10to15',
    '＞15張  ≦20張': '15to20',
    '＞20張  ≦30張': '20to30',
    '＞30張  ≦40張': '30to40',
    '＞40張  ≦50張': '40to50',
    '＞50張  ≦100張': '50to100',
    '＞100張  ≦200張': '100to200',
    '＞200張  ≦400張': '200to400',
    '＞400張  ≦600張': '400to600',
    '＞600張  ≦800張': '600to800',
    '＞800張  ≦1千張': '800to1000',
    '＞1千張': 'gt1000',
    'Unnamed: 20_level_1': 'unknonw1',
    'Unnamed: 21_level_1': 'unknown2'
})

# print(df.head())
print(json.loads(df.to_json(orient='records')))
