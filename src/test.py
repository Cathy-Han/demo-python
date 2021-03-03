import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime
import pandas as pd

# Data for plotting

log_list = pd.read_csv('aoi_logs.csv')
log_list.plot(x="receive_time",y="process_time")
# print(log_list["receive_time"])
# Time = [datetime.datetime.strptime(line[8],"%Y-%m-%d %H:%M:%S") for line in log_list]
# xdata = [mdates.date2num(line[0]) for line in Time]
# ydata = [float(line[12]) for line in log_list]

# # t = np.arange(0.0, 2.0, 0.01)
# # s = 1 + np.sin(2 * np.pi * t)

# fig, ax = plt.subplots()
# ax.plot(xdata, ydata)

# ax.set(xlabel='datetime', ylabel='time(s)',
#        title='About as simple as it gets, folks')
# ax.grid()
# plt.show()