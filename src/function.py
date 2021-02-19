import time
import datetime
import tailer

#获取当天日期
Date=time.strftime('%Y%m%d')
#设置文件位置
DataPath="/workspaces/demo-aqf/data/"
# 开启这3个文件
MatchFile=open(DataPath+Date+'_Match.txt')
OrderFile=open(DataPath+Date+'_Commission.txt')
UpDn5File=open(DataPath+Date+'_UpDn5.txt')

# 持续获取成交信息
def getMatch(): 
 return tailer.follow(MatchFile,0)

# 持续获取委托信息
def getOrder(): 
 return tailer.follow(OrderFile,0)

# 持续获取上下五档价信息
def getUpDn5(): 
 return tailer.follow(UpDn5File,0) 
 return tailer.follow(UpDn5File,0) 

# 获取最新一笔成交信息
def getLastMatch(): 
 return tailer.tail(MatchFile,3)[-2].split(",") 

# 获取最新一笔委托信息
def getLastOrder(): 
 return tailer.tail(OrderFile,3)[-2].split(",") 

# 获取最新一笔上下五档价信息
def getLastUpDn5(): 
 return tailer.tail(UpDn5File,3)[-2].split(",")


