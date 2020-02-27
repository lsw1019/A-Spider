import pandas as pd
import datetime
import requests
from bs4 import BeautifulSoup
import ShareUtility

def OutputAveragePrice(a_Url, a_Element, a_Id):
    html = requests.get(a_Url).text
    table = BeautifulSoup(html,'lxml').find(a_Element,id=a_Id).find('tbody').find_all('tr')
    totalShare = int(0)
    totalValue = float(0)
    lists=[]
    for tr in table:
        td = tr.find_all('td')
        share = int(td[1].get_text())
        value = float(td[0].get_text().replace(',','')) * float(td[1].get_text().replace(',',''))
        totalShare += share
        totalValue += value
        lists.append((share, value))

    return totalValue/totalShare

def GetHistroricalURL(a_Code, a_day):
    Yesterday = datetime.date.today() - datetime.timedelta(days=1)
    Endday = Yesterday.strftime('%Y-%m-%d')
    Startday = (Yesterday - datetime.timedelta(days=a_day)).strftime('%Y-%m-%d')
    
    return "http://market.finance.sina.com.cn/pricehis.php?symbol={}&startdate={}&enddate={}".format(ShareUtility.Code_to_symbol(a_Code), Startday, Endday)

def main():    
    code = input("请输入股票代码:")
    url = "https://vip.stock.finance.sina.com.cn/quotes_service/view/cn_price.php?symbol={}".format(ShareUtility.Code_to_symbol(code))
    averagePrice = OutputAveragePrice(url, 'div', 'divListTemplate')
    print("今日该股的平均交易价格：{}".format(averagePrice))

    url = GetHistroricalURL(code, 5)
    averagePrice = OutputAveragePrice(url, 'table', 'datalist')
    print("近5日该股的平均交易价格：{}".format(averagePrice))

    url = GetHistroricalURL(code, 15)
    averagePrice = OutputAveragePrice(url, 'table', 'datalist')
    print("近15日该股的平均交易价格：{}".format(averagePrice))

    url = GetHistroricalURL(code, 30)
    averagePrice = OutputAveragePrice(url, 'table', 'datalist')
    print("近一月该股的平均交易价格：{}".format(averagePrice))

    url = GetHistroricalURL(code, 90)
    averagePrice = OutputAveragePrice(url, 'table', 'datalist')
    print("近三月该股的平均交易价格：{}".format(averagePrice))

    url = GetHistroricalURL(code, 182)
    averagePrice = OutputAveragePrice(url, 'table', 'datalist')
    print("近半年该股的平均交易价格：{}".format(averagePrice))

    url = GetHistroricalURL(code, 365)
    averagePrice = OutputAveragePrice(url, 'table', 'datalist')
    print("近一年该股的平均交易价格：{}".format(averagePrice))

if __name__ == "__main__":
    main()
