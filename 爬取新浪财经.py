import requests
import pandas as pd

result = []
# r = requests.get('http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeDataSimple?page=2&num=40&sort=symbol&asc=1&node=hs_z&_s_r_a=page')
for i in range(1, 11):
    url = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeDataSimple?page=' + str(i) + '&num=40&sort=symbol&asc=1&node=hs_z&_s_r_a=page'
    r = requests.get(url)
    r_json = r.json()
    per_debt = []
    for idx in range(len(r_json)):
        debt_dict = r_json[idx]
        per_debt = list(debt_dict.values())
        per_debt[12] = per_debt[12]/10000
        result.append(per_debt[:13])
print(result[0])
name = ['代码','名称','最新价','涨跌额','涨跌幅','买入','卖出','昨收','今开','最高','最低','成交量/手','成交额/万']
console = pd.DataFrame(columns = name, data = result)
console.to_csv(r'C:\Users\xucha\Documents\找工作\嘉竹\沪深债券爬虫结果.csv', encoding='utf_8_sig')

# print(r.text)
# print(type(r.text))
# print(r.text[0])
# print(type(r.text[0]))
# r_str = r.text.split('},{')
# print(r_str)
# print(r_str[0])
# print(r_str[1])
# print(r_str[2])
# print(r_str[39])

# r_json = r.json()
# print(r_json)
# print(r_json[0])
# print(type(r_json[0]))
# print(r_json[0]['symbol'])
# symbol = r_json[0]['symbol']
# name = r_json[0]['name']
# trade = r_json[0]['trade']
# pricechange = r_json[0]['pricechange']
# changepercent = r_json[0]['changepercent']
# buy = r_json[0]['buy']
# sell = r_json[0]['sell']
# settlement = r_json[0]['settlement']
# open = r_json[0]['open']
# high = r_json[0]['high']
# low = r_json[0]['low']
# volume = r_json[0]['volume']
# amount = r_json[0]['amount']
