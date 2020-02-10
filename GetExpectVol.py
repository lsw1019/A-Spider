import tushare as ts
import pandas as pd
import DataAcess
import datetime
import requests

TOKEN = '9bf5a41c3ec3db9f4c29470727b20527faf34fa594af19dbd7713057'
INDEX_LABELS = ['sh', 'sz', 'hs300', 'sz50', 'cyb', 'zxb', 'zx300', 'zh500']
INDEX_LIST = {'sh': 'sh000001', 'sz': 'sz399001', 'hs300': 'sh000300',
              'sz50': 'sh000016', 'zxb': 'sz399005', 'cyb': 'sz399006', 
              'zx300': 'sz399008', 'zh500':'sh000905'}
AMStartTime = int(93000)
AMEndTime = int(113000)
PMStartTime = int(130000)
PMEndTime = int(150000)
TotalTime = int(40000)

def Code_to_symbol(code):
    if code in INDEX_LABELS:
        return INDEX_LIST[code]
    else:
        if len(code) != 6:
            return code
        else:
            return 'sh%s' % code if code[:1] in ['5', '6', '9'] or code[:2] in ['11', '13'] else 'sz%s' % code

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
    vol = requests.get("http://hq.sinajs.cn/list={}".format(Code_to_symbol(code))).text.split('"')[1].split(',')[8]
    df = GetLastDataFrame(code)
    timerate= GetTimeRate(nowtime)
    result = pd.DataFrame({'MA5':[df['v_ma5'].values[0]],
                      'MA10':[df['v_ma10'].values[0]],
                      'MA20':[df['v_ma20'].values[0]],
                      '今天预计成交量':[int(vol)/(timerate*100)]})
    print(result)

if __name__ == "__main__":
    main()
