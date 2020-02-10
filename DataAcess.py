import psycopg2


def Connect_DB():
    try:
        conn = psycopg2.connect(database="Shuli_Base",
                                user="postgres", password="lsw")
    except Exception as e:
        print(e)
    else:
        return conn
    return None


def CloseDBConnect(conn):
    conn.commit()
    conn.close()

def SelectTable(a_TableName, a_Where = ""):
    ##EffectiveDate, StockId, StockName, Shares, SharesPercentRate
    if(a_Where != ""):
        Where = "Where " + a_Where
    return "Select * from {} {}".format(a_TableName, Where)

def InsertTableWithConFLict(a_TableName, a_FieldSet, a_DataSet, a_KeySet ="", a_NonKeySet =""):
    ##EffectiveDate, StockId, StockName, Shares, SharesPercentRate
    if (a_KeySet != ""):
        confict = "ON CONFLICT ({}) DO UPDATE SET {}".format(a_KeySet, a_NonKeySet)
    return "INSERT INTO {} ({}) VALUES ({}) {}".format(a_TableName, a_FieldSet, a_DataSet, confict)

def TruncateTable(a_TableName):
    return "Truncate table {}".format(a_TableName)
