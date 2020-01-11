import requests
import time
from bs4 import BeautifulSoup
import socket
from decimal import Decimal
from selenium import webdriver
import time
import datetime
from dateutil.relativedelta import relativedelta
from selenium.webdriver.chrome.options import Options

import psycopg2

year = int(input("please input the beginning year:"))
month = int(input("please input the beginning month:"))
day = int(input("please input the beginning day:"))
# year=2019
# month = 1
# day = 1
BeginDate = datetime.datetime(year, month, day)
now = datetime.datetime.now()

def GetBrower(URL):
    browser = webdriver.Chrome()    

    browser.get(URL)

    return browser

def GetHtml(browser, year, month, day):
    browser.find_element_by_id("txtShareholdingDate").click()

    browser.find_element_by_xpath("//b[@class='year']/ul/li[{}]/button".format(now.year - year + 1)).click()

    browser.find_element_by_xpath("//b[@class='month']/ul/li[{}]/button".format(month)).click()

    browser.find_element_by_xpath("//b[@class='day']/ul/li[{}]/button".format(day)).click()

    browser.find_element_by_id("btnSearch").click()    

    return browser.page_source

def Connect_DB():
    try:
        conn = psycopg2.connect(database="Shuli_Base", user = "postgres", password="lsw")
    except Exception as e:
        print(e)
    else:
        return conn
    return None

def CloseDBConnect(conn):
    conn.commit()
    conn.close()

def InsertTable(a_TableName, a_FieldSet, a_EffectiveDate, a_StockId, a_StockName, a_Shares, a_SharesPercentRate, a_KeySet, a_NonKeySet):
    ##EffectiveDate, StockId, StockName, Shares, SharesPercentRate
    dataSet="'{}', \
              {}, \
             '{}', \
              {}, \
              {}".format(a_EffectiveDate, a_StockId, a_StockName, a_Shares, a_SharesPercentRate)
    
    nonKeySet = a_NonKeySet.format(a_StockName, a_Shares, a_SharesPercentRate)

    return "INSERT INTO {} ({}) VALUES ({}) ON CONFLICT ({}) DO UPDATE SET {};".format(a_TableName, a_FieldSet, dataSet, a_KeySet, nonKeySet)

def Crawl(URL):
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    conn = Connect_DB()
    cur = conn.cursor()

    DateRange = (now - BeginDate).days
    browers = GetBrower(URL)


    for i in range(0, DateRange + 1):
        date = BeginDate +  relativedelta(days=i)
        html = GetHtml(browers, date.year, date.month, date.day)

        effectiveDate = "{}".format(BeautifulSoup(html,'lxml').find('input', attrs={"name" :"txtShareholdingDate"})["value"])

        table=BeautifulSoup(html,'lxml').find('table',id='mutualmarket-result').find('tbody').find_all('tr')
        for tr in table:
            td=tr.find_all("td")
            try:                    
                stockID = td[0].find('div', attrs={"class" :"mobile-list-body"}).get_text()
                shareName = "{}".format(td[1].find('div', attrs={"class" :"mobile-list-body"}).get_text())
                shares = Decimal(td[2].find('div', attrs={"class" :"mobile-list-body"}).get_text().replace(",", ""))
                sharespecentrate =  Decimal(td[3].find('div', attrs={"class" :"mobile-list-body"}).get_text().replace("%", ""))/100

                OriginalDataField = "EffectiveDate, \
                                 StockId, \
                                 StockName, \
                                 Shares,\
                                 SharesPercentRate"                                                
                TableName= "OriginalData"
                KeySet = "EffectiveDate, \
                        StockId"
            
                NonKeySet = "StockName = '{}', Shares = {}, SharesPercentRate = {}"

                sql =InsertTable(TableName, OriginalDataField, effectiveDate, stockID, shareName, shares, sharespecentrate, KeySet, NonKeySet)
                cur.execute(sql)
                
                ##使改变永久存入数据库
 
                conn.commit()           
            except:
                continue
     
 
    ##关闭到数据库的通信
 
    cur.close()
    conn.close()

def main():
    Crawl("https://www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=sh&t=sh")
    Crawl("https://www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=sz")
    
   
if __name__ == "__main__":
    main()