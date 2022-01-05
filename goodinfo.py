import requests
from bs4 import BeautifulSoup as BS
import pandas
import json

stock_no = 4953

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
}
res = requests.get(
    f'https://goodinfo.tw/StockInfo/EquityDistributionClassHis.asp?STOCK_ID={stock_no}&DISPLAY_CAT=%E6%8C%81%E6%9C%89%E5%BC%B5%E6%95%B8%E5%8D%80%E9%96%93%E5%88%86%E7%B4%9A%E4%B8%80%E8%A6%BD(%E5%AE%8C%E6%95%B4)', headers=headers)
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
    '週別': 'week#',
    '統計  日期': 'date',
    '收盤': 'price',
    '漲跌  (元)': '±price',
    '漲跌  (%)': '±price%',
    '＜1張': '<1',
    '≧1張  ≦5張': '1~5',
    '＞5張  ≦10張': '5~10',
    '＞10張  ≦15張': '10~15',
    '＞15張  ≦20張': '15~20',
    '＞20張  ≦30張': '20~30',
    '＞30張  ≦40張': '30~40',
    '＞40張  ≦50張': '40~50',
    '＞50張  ≦100張': '50~100',
    '＞100張  ≦200張': '100~200',
    '＞200張  ≦400張': '200~400',
    '＞400張  ≦600張': '400~600',
    '＞600張  ≦800張': '600~800',
    '＞800張  ≦1千張': '800~1000',
    '＞1千張': '>1000',
    'Unnamed: 20_level_1': 'unknown1',
    'Unnamed: 21_level_1': 'unknown2'
})
del df["unknown1"]
del df["unknown2"]

# print(df.head())
print(df)
# print(json.loads(df.to_json(orient='records')))
