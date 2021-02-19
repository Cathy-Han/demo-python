import numbers as np
import pandas as pd
from pandas_datareader import data as web
from pandas_datareader.yahoo.actions import YahooActionReader
from pandas_datareader.yahoo.quotes import YahooQuotesReader
import datetime
import time
import requests
import json

class DataPrepare():

    TimeStr = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    Time = datetime.datetime.strptime(TimeStr,"%Y-%m-%d %H:%M:%S")
    LastTime = Time-datetime.timedelta(0,3600)
    filename="data/SIF"+datetime.datetime.strftime(LastTime,"%Y%m%d%H")+".json"
    print(filename)

    def DataFrom_DataReader(self):
        start=datetime.datetime(2021,2,15)
        end=datetime.date.today()
        # data=web.DataReader('AAPL',data_source='yahoo',start=start,end=end)
        # data.to_csv('aapl2021.csv',columns=data.columns,index=True)

        # silver=web.DataReader('SI=F',data_source='yahoo',start=start,end=end)
        # silver.to_csv('silver2021.csv',columns=silver.columns,index=True)

        # df = web.get_data_yahoo('SI=F',start,end,interval="1H")
        # df = YahooActionReader('SI=F',start=start,interval="60m").read()
        df = YahooQuotesReader("SI=F",start=start,end=end).read()
        df.to_csv('silver_hours.csv',columns=df.columns,index=True)

    def DataReadPerHours(self):
        url="https://query1.finance.yahoo.com/v8/finance/chart/SI=F?symbol=SI%3DF&interval=60m"
        r=requests.get(url)
        print("Status Code:",r.status_code)
        response_json=r.json()
        print(response_json)
        with open(self.filename,'w') as f_obj:
            json.dump(response_json,f_obj)


    def Json2Csv(self):
        print("transfer begin")
        with open(self.filename) as f_obj:
            json_obj=json.load(f_obj)
        timestamp_array = json_obj["chart"]["result"][0]["timestamp"]
        open_array=json_obj["chart"]["result"][0]["indicators"]["quote"][0]["open"]
        volume_array=json_obj["chart"]["result"][0]["indicators"]["quote"][0]["volume"]
        low_array=json_obj["chart"]["result"][0]["indicators"]["quote"][0]["low"]
        close_array=json_obj["chart"]["result"][0]["indicators"]["quote"][0]["close"]
        high_array=json_obj["chart"]["result"][0]["indicators"]["quote"][0]["high"]
        d={'timestamp':timestamp_array,'open':open_array,'volume':volume_array,'low':low_array,'close':close_array,'high':high_array}
        df = pd.DataFrame(data=d)
        #print(df)
        csv_file=self.filename.replace(".json",".csv")
        df.to_csv(csv_file,columns=df.columns,index=True)


#DataPrepare().Json2Csv()