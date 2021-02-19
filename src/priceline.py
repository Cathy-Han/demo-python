import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.finance import candlesstick_ohlc
import datetime

def MA(csv_data):
    MAarray=[]
    MA=[]
    MAValue=0
    STime=datetime.datetime(2021,1,4)
    Cycle=1
    MAlen=5
    for i in csv_data:
        time=datetime.datetime.strptime(i[0],'%Y-%m-%d')
        price=round(float(i[4]))
        if len(MAarray)==0:
            MAarray+=[price]
        else:
            if time<STime+datetime.timedelta(Cycle,0):
                MAarray[-1]=price
            else:
                if len(MAarray)==MAlen:
                    MAarray=MAarray[1:]+[price]
                else:
                    MAarray+=[price]
        MAValue=float(sum(MAarray))/len(MAarray)
        MA.extend([MAValue])
    return MA


aapl = [line.strip('\n').split(",") for line in open('aapl.csv')][1:]
Time = [datetime.datetime.strptime(line[0],"%Y-%m-%d") for line in aapl]
Time1 = [mdates.date2num(line) for line in Time]
Price = [round(float(line[4])) for line in aapl]
#定义图标对象
ax = plt.figure(1)
ax = plt.subplot(111)
#绘制图案
ax.plot_date(Time1,Price,'k-')
MA=MA(aapl)
ax.plot_date(Time1,MA,'r-')
#定义Title
plt.title('Price Line')
#定义X轴
hfmt = mdates.DateFormatter('%Y-%m-%d')
ax.xaxis.set_major_formatter(hfmt)
#显示绘制
plt.show()
