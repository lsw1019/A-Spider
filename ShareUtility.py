INDEX_LABELS = ['sh', 'sz', 'hs300', 'sz50', 'cyb', 'zxb', 'zx300', 'zh500']
INDEX_LIST = {'sh': 'sh000001', 'sz': 'sz399001', 'hs300': 'sh000300',
              'sz50': 'sh000016', 'zxb': 'sz399005', 'cyb': 'sz399006', 
              'zx300': 'sz399008', 'zh500':'sh000905'}
              
def Code_to_symbol(code):
    if code in INDEX_LABELS:
        return INDEX_LIST[code]
    else:
        if len(code) != 6:
            return code
        else:
            return 'sh%s' % code if code[:1] in ['5', '6', '9'] or code[:2] in ['11', '13'] else 'sz%s' % code
