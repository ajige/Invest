# coding=utf-8
##plot the price, earning picture

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from pandas import Series
#from pandas import DataFrame
#import tushare as ts
import datetime
import getdata
from math import isnan

def plotpe(ax):
	global profit, hs300
		
	daterange = pd.date_range('01/01/2012', end = '03/03/2017', freq='B')
	#daterange = pd.date_range('03/01/2014', end = '05/20/2014', freq='B')
	convertrange = daterange.to_pydatetime()
	sz50code, namedf, price, volume = getdata.GetPriceVolume()
	
	epsall = getdata.GetProfit('eps')
	peseries = Series()
	validpe = Series()
	
	for date in convertrange:
		if date not in price.index:
			continue
		combinepe = 0
		for code in hs300.index:
			weight = hs300['weight'][code] 
			eps = epsall.ix[code]
					
			quarter = date.month/4 + 1
			if date.year == 2012:
				earning = eps[20124]
			elif date.year > 2016:
				earning = eps[20163] + eps[20154] - eps[20153]
			else:	
				if quarter == 1:
					earning = eps[(date.year - 1) * 10 + 4]
				else:
					earning = eps[date.year * 10 + quarter - 1] + eps[(date.year - 1) * 10 + 4] - eps[(date.year - 1) * 10 + quarter - 1]
						
			temppe = float(price[code][date])/earning
				
			if not isnan(temppe):
				validpe[code] = temppe
					
			if isnan(temppe) and code in validpe.index:
				temppe = validpe[code]
					
			if (not isnan(temppe) ) and temppe > 0:
				combinepe = combinepe + weight * temppe
					#print combinepe
			#if date.year == 2014 and date.month==4  and date.day == 3 and temppe < 0:
			#	print date, code, temppe, earning 
				
		peseries[date] = combinepe	
		print date, combinepe 
	#normalizedpe = (peseries - peseries.min()) / (peseries.max() - peseries.min())
	
	ax.set_title("hs300PE")
	peseries.plot(ax = ax)
	
	#binned = pd.cut(peseries.values, 10)
	#print binned
	#dist_10 = pd.value_counts(binned).reindex(binned.categories)
	#print dist_10
	#dist_10.plot()
	
	#uniformpeseries = peseries/ peseries.mean()
	#uniformpeseries.plot()
	#uniformprice = price[code] / price[code].mean()
	#uniformprice.plot()
	#plt.show()

if __name__ == "__main__":
	
	global profit, hs300
	profit = getdata.GetProfit('eps')
	hs300 = getdata.GetHs300()
	
	#plot use subplot
	fig, axes = plt.subplots(1,1)
	#plotpe(axes)
	sz50code, namedf, price, volume = getdata.GetPriceVolume('hs300')
	price['hs300'].plot(ax = axes)
	plt.show()
	
	