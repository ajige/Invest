# coding=utf-8
##plot the price, earning picture

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from pandas import Series
from pandas import DataFrame
import tushare as ts
import datetime
import getdata
	
def GetHighestDiv():		
	global divi, hs300
	sz50code, namedf, price, volume = getdata.GetPriceVolume()
	dt = datetime.datetime(2017,04,28)
	df = DataFrame(columns=[2013,2014,2015,'avg', 'price', 'ratio', 'name'], index=hs300.index)
	
	for ii in df.index:
		for year in [2013,2014,2015]:
			df[year][ii] = divi[year][ii]
			
		#print ii, 	df[2013][ii] , df[2014][ii] , df[2015][ii]
		df['avg'][ii] = float(df[2013][ii] + df[2014][ii] + df[2015][ii]) / 3
		df['price'][ii] = price[ii][dt]
		df['ratio'][ii] = df['avg'][ii] / price[ii][dt]
		df['name'][ii] = hs300['name'][ii]
		#print df.ix[ii]
	
	topcode = df.sort(columns='ratio', ascending=False)[0:50]
	for code in topcode.index:
		if not np.isnan(divi[2016][code]):
			print code, divi[2016][code]/price[code][dt], df['name'][code]

def plotdivratio(code):
	sz50code, namedf, price, volume = getdata.GetPriceVolume(code)
	div = getdata.GetDiv('divi').ix[code]
	reportdate = getdata.GetDiv('report_date').ix[code]
	
	print div, reportdate
		
	##do backfill
	divvalue= Series()
	
	for idx in range(0, len(reportdate.index)):
		if idx != len(reportdate.index) - 1:
			startdate = reportdate[reportdate.index[idx]]
			enddate = reportdate[reportdate.index[idx + 1]]
		else:
			startdate = reportdate[reportdate.index[idx]]
			enddate = '2017-04-28'
			
		print startdate, enddate
		dr = pd.date_range(startdate, end = enddate, freq='B')
		ctr = dr.to_pydatetime()	
		for date in ctr:
			divvalue[date] = div[div.index[idx]]
	
	daterange = pd.date_range('01/01/2012', end = '04/28/2017',freq='B')
	convertrange = daterange.to_pydatetime()	
	ratio = Series()
	for date in convertrange:
		if date in price.index and date in divvalue.index:
			ratio[date] = divvalue[date] / price[code][date]
	
	#print ratio
	fig, ax = plt.subplots()
	ratio.plot(ax=ax)
	plt.show()

def calcdivratio(code):
	global divi, hs300,eps
	zzidx = [2012,2013,2014,2015,2016]
	codelist=['600015', '601166', '000001', '600000', '600036', '600016', '601818','601998']
	ret = DataFrame(index = codelist, columns = zzidx)
	#print divi.ix[code]
	#print eps.ix[code]
	
	
	for code in ret.index:
		for year in zzidx:
			ret[year][code] = divi[year][code]/eps[year*10+3][code]*10
		print hs300['name'][code].decode('UTF-8'), ret.ix[code]
	
if __name__ == "__main__":
	
	global divi, hs300,eps
	divi = getdata.GetDiv('divi')
	eps = getdata.GetProfit('eps')
	#print divi
	hs300 = getdata.GetHs300()
	#plotdivratio('601166')
	calcdivratio('601166')
	
	
	