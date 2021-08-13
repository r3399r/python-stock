import twstock
twstock.__update_codes()
print('hi')
stock = twstock.Stock('1313')
print(stock.price)
