import datetime
import time
import pandas as pd
from matplotlib import pyplot
from matplotlib import dates
import mplfinance as mpf

class Quota(object):
    def __init__(self,hours):
        self.hours=hours
        self.csv_data=[line.strip('\n').split(",") for line in open('data/SIF.csv')][-hours*2:]
        self.begin=int(self.csv_data[-hours][0])
        #print(self.begin)
    
    def MA_Hour(self,cycle):
        #取最近24h为MA起点
        STime=self.begin
        MAarray=[]
        MA=[]
        for i in self.csv_data:
            ts=int(i[0])
            t=time.strftime('%Y-%m-%d %H:%M',time.gmtime(ts))
            price=float(i[4])
            if len(MAarray)<cycle-1:
                MAarray+=[price]
            else:
                if len(MAarray)==cycle-1:
                    MAarray+=[price]
                else:
                    MAarray=MAarray[1:]+[price]
            if ts>=STime:
                MAValue=sum(MAarray)/len(MAarray)
                MA.extend([[datetime.datetime.strptime(t,'%Y-%m-%d %H:%M'),MAValue]])
        return MA

    def Show(self):
        #1h蜡烛图和均线图
        # h=48
        # qt=Quota(hours=h)
        show_data=self.csv_data[-self.hours:]
        #print(show_data[0])
        Time=[datetime.datetime.strptime(time.strftime('%Y-%m-%d %H:%M',time.gmtime(int(line[0]))),'%Y-%m-%d %H:%M') for line in show_data]
        Time1=[dates.date2num(line) for line in Time]   #转换为图形需要的时间格式
        Price=[round(float(line[4]),2) for line in show_data]
        #计算5周期MA
        MA5=self.MA_Hour(5)
        ma_df5 = pd.DataFrame({'time':[line[0] for line in MA5],'price':[line[1] for line in MA5]})
        ma_df5.to_csv('data/MA5.csv',columns=ma_df5.columns,index=False)
        MA5Value=[round(line[1],2) for line in MA5]
        #计算10周期MA
        MA10=self.MA_Hour(10)
        ma_df = pd.DataFrame({'time':[line[0] for line in MA10],'price':[line[1] for line in MA10]})
        ma_df.to_csv('data/MA10.csv',columns=ma_df.columns,index=False)
        MA10Value=[round(line[1],2) for line in MA10]
        #计算20周期MA
        MA20=self.MA_Hour(20)
        ma_df2 = pd.DataFrame({'time':[line[0] for line in MA20],'price':[line[1] for line in MA20]})
        ma_df2.to_csv('data/MA20.csv',columns=ma_df.columns,index=False)
        MA20Value=[round(line[1],2) for line in MA20]

        #计算均线差值
        df_all=pd.merge(ma_df5,ma_df,on="time")
        df_all=pd.merge(df_all,ma_df2,on="time")
        pieces=[]
        last_diff=0
        last_diff2=0
        last_diff3=0
        for index,row in df_all.iterrows():
            cur_diff=row["price_x"]-row["price_y"]
            cur_diff2=row["price_x"]-row["price"]
            cur_diff3=row["price_y"]-row["price"]
            #5周期、10周期交叉判断
            if last_diff>0 and cur_diff<=0:
                dead_cross=row
                #print(datetime.datetime.strftime(row["time"],"%Y-%m-%d %H:%M"))
                pieces.extend([[datetime.datetime.strftime(row["time"],"%Y-%m-%d %H:%M"),row["price_x"]]])
            elif last_diff<0 and cur_diff>=0:
                glod_cross=row
                pieces.extend([[datetime.datetime.strftime(row["time"],"%Y-%m-%d %H:%M"),row["price_x"]]])
            
            #5周期、20周期交叉判断
            if last_diff2>0 and cur_diff2<=0:
                dead_cross2=row
                pieces.extend([[datetime.datetime.strftime(row["time"],"%Y-%m-%d %H:%M"),row["price_x"]]])
            elif last_diff2<0 and cur_diff2>=0:
                glod_cross2=row
                pieces.extend([[datetime.datetime.strftime(row["time"],"%Y-%m-%d %H:%M"),row["price_x"]]])

            #10周期、20周期交叉判断
            if last_diff3>0 and cur_diff3<=0:
                dead_cross3=row
                pieces.extend([[datetime.datetime.strftime(row["time"],"%Y-%m-%d %H:%M"),row["price_y"]]])
            elif last_diff3<0 and cur_diff3>=0:
                glod_cross3=row
                pieces.extend([[datetime.datetime.strftime(row["time"],"%Y-%m-%d %H:%M"),row["price_y"]]])
            
            last_diff=cur_diff
            last_diff2=cur_diff2
            last_diff3=cur_diff3

        #print(pieces)
        TimeNew=[datetime.datetime.strptime(line[0],"%Y-%m-%d %H:%M") for line in pieces]
        TimeNew1=[dates.date2num(line) for line in TimeNew]   #转换为图形需要的时间格式
        PointValue=[round(line[1],2) for line in pieces]
        print(TimeNew[-1])
        if TimeNew[-1]>=(datetime.datetime.now()-datetime.timedelta(0,3600)):
            print("达成下单条件")

        ax=pyplot.figure(1)
        ax=pyplot.subplot(111)
        #绘制k线图
        ax.plot_date(Time1,Price,'k-')
        ax.plot_date(Time1,MA5Value,'y-')
        ax.plot_date(Time1,MA10Value,'r-')
        ax.plot_date(Time1,MA20Value,'b-')
        ax.plot_date(TimeNew1, PointValue, 'r.',markersize='8') 
        #candlesstick_ohlc(ax,qt.csv_data,width=0.0005,colorup='r',colordown='g')
        #定义X轴
        hfmt=dates.DateFormatter("%Y-%m-%d %H:M")
        ax.xaxis.set_major_formatter(hfmt)
        pyplot.show()

