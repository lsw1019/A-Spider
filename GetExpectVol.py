import tushare as ts
import pandas as pd
import DataAcess
import datetime
import requests
import ShareUtility

AMStartTime = int(93000)
AMEndTime = int(113000)
PMStartTime = int(130000)
PMEndTime = int(150000)
TotalTime = int(40000)

def GetTimeRate(time):
    inttime = int(time)
    if inttime < AMStartTime:
        return 0
    elif inttime < AMEndTime:
        return (AMEndTime-inttime)/TotalTime
    elif inttime < PMStartTime:
        return 0.5
    elif inttime < PMEndTime:
        return (inttime-PMStartTime)/TotalTime + 0.5
    else:
        return 1

def GetLastDataFrame(code):
    Iday = datetime.date.today()
    df = ts.get_hist_data(code, Iday.strftime('%Y-%m-%d'))
    while(df.empty):
        Iday = Iday - datetime.timedelta(days=1)
        df = ts.get_hist_data(code, '2020-02-07')
    return df

def main():
    code = input("请输入股票代码:")
    nowtime = datetime.datetime.now().strftime('%H%M%S')
    vol = requests.get("http://hq.sinajs.cn/list={}".format(ShareUtility.Code_to_symbol(code))).text.split('"')[1].split(',')[8]
    df = GetLastDataFrame(code)
    timerate= GetTimeRate(nowtime)
    result = pd.DataFrame({'MA5':[df['v_ma5'].values[0]],
                      'MA10':[df['v_ma10'].values[0]],
                      'MA20':[df['v_ma20'].values[0]],
                      '今天预计成交量':[int(vol)/(timerate*100)]})
    print(result)

if __name__ == "__main__":
    main()
