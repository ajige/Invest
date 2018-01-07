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
import download

import pdb
#pdb.set_trace()
genddate = pd.datetime.today().date().strftime('%Y-%m-%d')
#genddate = '2017-12-31'

def plotpe(code, ax, name):
	global profit, hs300, basic, retpearray
	sz50code, namedf, price, volume = getdata.GetPriceVolume(code)
	
	print "PE: %s: %s" % (code, name)
	
	daterange = pd.date_range('01/01/2012', end = genddate, freq='B')
	convertrange = daterange.to_pydatetime()
	netprofit = profit.ix[code]/basic[code]/100
	
	#print netprofit
	
	#price = price.ix[convertrange[-1]:convertrange[0]]
	#print price
	peseries = Series()
	earningseries = Series()
	for date in convertrange:
		if date in price.index:
			if date.month % 3 == 0:
				quarter = date.month/3
			else:
				quarter = date.month/3 + 1
				
			if date.year == 2011:
				earning = netprofit[20114]
			elif (date.year == 2017 and quarter == 4) or date.year > 2017:
				earning = netprofit[20173] + netprofit[20164] - netprofit[20163]
				# earning = netprofit[20164]
				# if np.isnan(earning):
					# earning = netprofit[20163] + netprofit[20154] - netprofit[20153]
			else:	
				if quarter == 1:
					earning = netprofit[(date.year - 1) * 10 + 4]
				else:
					earning = netprofit[date.year * 10 + quarter - 1] + netprofit[(date.year - 1) * 10 + 4] - netprofit[(date.year - 1) * 10 + quarter - 1]
				
			temp = price[code][date] / earning
			#print date, price[code][date], earning
			
			peseries[date] = temp
			earningseries[date] = earning
			
	#print peseries.min(), peseries.max(), peseries.mean(), peseries.median()	
	#normalizedpe = (peseries - peseries.min()) / (peseries.max() - peseries.min())
	normalizedpe = peseries
	#print normalizedpe
	
	print code, normalizedpe.ix[-1], normalizedpe.mean(), normalizedpe.ix[-1] / normalizedpe.mean(), normalizedpe.std()/normalizedpe.mean();
	sortedpe = normalizedpe.sort_values();
	print code, sortedpe.index[0], sortedpe[sortedpe.index[0]], sortedpe.index[-1], sortedpe[sortedpe.index[-1]]
	
	retpearray[code] = normalizedpe.ix[-1] / sortedpe[sortedpe.index[0]]
	
	ax.set_title(code + ' PE')
	normalizedpe.plot(ax = ax, label = "PE")
	
	print '------------------------------------------'

def plotpb(code, ax, name):
	global profit, hs300, basic, roe, retpbarray
	sz50code, namedf, price, volume = getdata.GetPriceVolume(code)
	print "PB: %s: %s" % (code, name)
	
	daterange = pd.date_range('01/01/2012', end = genddate,freq='B')
	convertrange = daterange.to_pydatetime()
	
	netprofit = profit.ix[code]/basic[code]/100
	roeix = roe.ix[code]
	
	#print netprofit
	#print roeix
	#price = price.ix[convertrange[-1]:convertrange[0]]
	
	pbseries = Series()
	earningseries = Series()
	for date in convertrange:
		if date in price.index:
			if date.month % 3 == 0:
				quarter = date.month/3
			else:
				quarter = date.month/3 + 1
				
			if date.year == 2011:
				earning = netprofit[20114]
				temproe = roeix[20114]
			elif (date.year == 2017 and quarter == 4) or date.year > 2017:
				earning = netprofit[20173]
				temproe = roeix[20173] 
 			#	temproe = roeix[20163] + roeix[20172] - roeix[20162]
				# if np.isnan(earning):
					# earning = netprofit[20163] + netprofit[20154] - netprofit[20153]
				# temproe = roeix[20164]
				# if np.isnan(temproe):
					# temproe = roeix[20163] + roeix[20154] - roeix[20153]	
			else:	
				if quarter == 1:
					earning = netprofit[(date.year - 1) * 10 + 4]
					temproe = roeix[(date.year - 1) * 10 + 4]
				else:
					earning = netprofit[date.year * 10 + quarter - 1]
					temproe = roeix[date.year * 10 + quarter - 1]
			
			book = earning*100 / temproe
			#if code == '600340' and date.year == 2017 and quarter > 2 :
			#	print date, earning, temproe, earning * 100 / temproe, price[code][date], price[code][date] / book
				
			temp = price[code][date] / book
			#print code, date, price[code][date]
			pbseries[date] = temp
			#print date, earning, temproe, book, price[code][date], temp
			earningseries[date] = earning
			
	normalizedpe = pbseries
	
	print code, normalizedpe.ix[-1], normalizedpe.mean(), normalizedpe.ix[-1] / normalizedpe.mean(), normalizedpe.std()/normalizedpe.mean()
	sortedpe = normalizedpe.sort_values()
	print code, sortedpe.index[0], sortedpe[sortedpe.index[0]], sortedpe.index[-1], sortedpe[sortedpe.index[-1]]
	
	retpbarray[code] = normalizedpe.ix[-1] / sortedpe[sortedpe.index[0]]
	ax.set_title(code + ' PB')
	normalizedpe.plot(ax = ax, label = "PB")
	
	#normalizedpe = (peseries - peseries.min()) / (peseries.max() - peseries.min()) 
	#normalizedearning = (earningseries - earningseries.min()) / (earningseries.max() - earningseries.min())
	
	#ax.set_yticks(np.arange(0.,1.3,0.1))
	#normalizedprice.plot(ax = ax,  label="Price")
	
	print '------------------------------------------'	
	

def plotgrowth(code, ax):
	global profit, hs300, roe, growth_mbrg, growth_nprg
	print hs300['name'][code].decode('UTF-8')
	print growth_mbrg.ix[code]
	print growth_nprg.ix[code]
	ax.plot(growth_mbrg.ix[code], color='b', marker='o')
	#ax.plot(growth_nprg.ix[code], color='r', marker='o')
	ax.set_title(code + ' growth')
	print '------------------------------------------'	
 
	
if __name__ == "__main__":
	global profit, hs300,roe, growth_mbrg, growth_nprg
	
	profit = getdata.GetProfit('net_profits')
	basic = getdata.GetBasic()['totals']
	roe = getdata.GetProfit('roe')
	growth_mbrg = getdata.GetGrowth('mbrg')
	growth_nprg = getdata.GetGrowth('nprg')
	
	hs300 = getdata.GetHs300()
	zz500 = getdata.GetZz500()
	
	retpearray = Series()
	retpbarray = Series()
	
	#plot use subplot
	#fig, axes = plt.subplots(1,1)
	#plotpe('000538', axes)
	#plt.show()
	#fig, axes = plt.subplots(2,2)
	
	codelist = download.LoadCodelist('Appliances.txt')
	fig, axes = plt.subplots(2, len(codelist))
	
	cnt = 0
	for code in codelist:
		#plotpe(code, axes[1][cnt])
		#plotpb(code, axes[0][cnt])
		if code in hs300.index:
			name = hs300['name'][code].decode('UTF-8')
		elif name in zz500.index:
			name = zz500['name'][code].decode('UTF-8')

		plotpe(code, axes[0][cnt], name)
		plotpb(code, axes[1][cnt], name)
		#plotgrowth(code, axes[2][cnt])
		cnt = cnt + 1

	plt.show()
	
	#for code in codelist:
	#	print code, hs300['name'][code].decode('UTF-8'),  retpbarray[code], retpearray[code]
	#print retpearray.mean()
		
	#normalizedpe = (peseries - peseries.min()) / (peseries.max() - peseries.min()) 
	#normalizedearning = (earningseries - earningseries.min()) / (earningseries.max() - earningseries.min())
	#normalizedprice = (price[code] - price[code].min()) / (price[code].max() - price[code].min())

	#ax.set_yticks(np.arange(0.,1.3,0.1))
	#normalizedprice.plot(ax = ax,  label="Price")
	
	#earningseries.plot(ax = ax,  label="Earning")
	
	#n, bins, patches = ax.hist(list(normalizedpe), 10, cumulative= True, normed = True)
	#plt.show()
	#normalizedpe.plot.hist(ax=ax, label="PE", bins = 10)	
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
'''	
2017-06-12运行结果：
['000423', '000538', '000963', '600887', '601166', '600048', '000069', '600066']
000423: 东阿阿胶
000423 5.61172436313 4.98260708452 1.12626267092 0.1612572364
000423 2014-06-04 00:00:00 3.59433630868 2013-03-27 00:00:00 7.87259517788
------------------------------------------
000423: 东阿阿胶
000423 25.3236658986 21.1869160588 1.19525021142 0.142269202699
000423 2014-06-04 00:00:00 15.2109027028 2013-03-27 00:00:00 32.146162425
------------------------------------------
000538: 云南白药
000538 6.33913036331 6.07628726765 1.04325718717 0.204406543178
000538 2016-02-29 00:00:00 4.22050890968 2013-09-27 00:00:00 10.2058083742
------------------------------------------
000538: 云南白药
000538 34.1547972161 27.0758372999 1.26144934458 0.181718728209
000538 2014-07-10 00:00:00 19.5399615782 2013-09-27 00:00:00 44.3537956289
------------------------------------------
000963: 华东医药
000963 3.33711600723 4.36635019989 0.764280429755 0.314671683155
000963 2017-01-16 00:00:00 2.36381831999 2015-08-17 00:00:00 8.95350885505
------------------------------------------
000963: 华东医药
000963 16.7947458844 16.2454240704 1.03381394118 0.161058539721
000963 2012-01-19 00:00:00 10.6522882693 2014-09-19 00:00:00 22.6388252037
------------------------------------------
600887: 伊利股份
600887 5.38981070657 4.90222128106 1.09946295721 0.172281259255
600887 2014-06-03 00:00:00 3.39225437859 2013-03-26 00:00:00 8.23510392432
------------------------------------------
600887: 伊利股份
600887 21.9812834689 21.5721184244 1.0189673094 0.18132347129
600887 2014-11-07 00:00:00 14.8982443622 2013-03-26 00:00:00 35.1777186003
------------------------------------------
601166: 兴业银行
601166 0.90436182195 0.906597958157 0.997533486385 0.143392478158
601166 2013-12-26 00:00:00 0.725583149353 2015-06-08 00:00:00 1.36237354655
------------------------------------------
601166: 兴业银行
601166 5.88011587744 5.04370529195 1.16583256496 0.190993727411
601166 2014-03-10 00:00:00 3.55049282958 2015-06-08 00:00:00 7.80282672707
------------------------------------------
600048: 保利地产
600048 1.28539943003 1.5145363377 0.84870821388 0.227561586798
600048 2014-03-10 00:00:00 0.88645354472 2015-04-30 00:00:00 2.61333538946
------------------------------------------
600048: 保利地产
600048 9.24082983485 8.02682758595 1.15124309522 0.211004759947
600048 2014-03-10 00:00:00 4.27000744085 2015-04-30 00:00:00 12.8230392025
------------------------------------------
000069: 华侨城Ａ
000069 1.7824452114 1.95828182679 0.910208728397 0.26027597223
000069 2016-10-17 00:00:00 1.23284585366 2015-06-25 00:00:00 3.86996773481
------------------------------------------
000069: 华侨城Ａ
000069 11.3171124534 11.7216109053 0.965491223413 0.242452102372
000069 2014-03-10 00:00:00 7.78104352032 2015-06-25 00:00:00 24.0969348369
------------------------------------------
600066: 宇通客车
600066 3.72642927092 2.98666830705 1.24768768669 0.190075081654
600066 2012-01-06 00:00:00 1.95471043797 2015-05-26 00:00:00 4.54682196001
------------------------------------------
600066: 宇通客车
600066 12.5216037329 12.5578985965 0.997109798002 0.140441169782
600066 2012-01-06 00:00:00 9.22903889505 2015-05-26 00:00:00 18.6421564576


000625 长安汽车 0.199731440771 0.741824384651
000423 东阿阿胶 0.513276722289 0.419137205498
000963 华东医药 0.42685883736 0.277128547579
600066 宇通客车 0.310643060736 0.861385423368
600048 保利地产 1.00250688391 0.531782722374
600887 伊利股份 0.359908508739 0.472400033849
600340 华夏幸福 2.25993938045 0.96211743446
000538 云南白药 0.541821647026 0.387679854216
601668 中国建筑 1.78262594229 1.57555862004
601166 兴业银行 0.655352199677 0.227169335831
------------------------------------------
000963: 华东医药
000963 6.1281706234 8.95786339371 2.79031952077
000963 0.684110747626
000963 2017-01-16 00:00:00 4.79839765153 2015-08-17 00:00:00 18.1733402115
------------------------------------------
000963: 华东医药
000963 30.8413217081 33.0466185815 5.3874311247
000963 0.933267094545
000963 2012-01-19 00:00:00 21.614837362 2014-09-19 00:00:00 45.9473470387
------------------------------------------
------------------------------------------
601166: 兴业银行
601166 0.890413391482 0.908164137337 0.131851467676
601166 0.980454253669
601166 2013-12-26 00:00:00 0.725583149353 2015-06-08 00:00:00 1.36237354655
------------------------------------------
601166: 兴业银行
601166 5.87731611539 5.02931747987 0.977650700461
601166 1.16861107673
601166 2014-03-11 00:00:00 3.55049282958 2015-06-08 00:00:00 7.80282672707

000625: 长安汽车
000625 1.88672938693 2.30898861448 0.668301529814
000625 0.817123729019
000625 2012-01-04 00:00:00 1.0831915109 2015-04-28 00:00:00 4.17606811967
------------------------------------------
000625: 长安汽车
000625 6.96467104809 12.8286646992 5.61951340168
000625 0.542899141212
000625 2015-08-25 00:00:00 5.80519173826 2013-03-28 00:00:00 29.3212171711
------------------------------------------
600887: 伊利股份
600887 5.16299985636 5.08598689117 0.884027202438
600887 1.01514218712
600887 2014-06-03 00:00:00 3.50651978924 2013-03-26 00:00:00 8.51622192977
------------------------------------------
600887: 伊利股份
600887 20.9622405861 22.4223744753 4.06427380902
600887 0.934880496676
600887 2014-11-07 00:00:00 15.4144491717 2013-03-26 00:00:00 36.3785644159
------------------------------------------
------------------------------------------
[program] c:\quant\script>python pe.py
['000625', '000423', '000963', '600066', '600048', '600887']
000625: 长安汽车
000625 6.80678178 12.8875668591 11.7963693083 5.61607256891 29.3212171711 5.80519173826
000625 0.528166554202
------------------------------------------
000423: 东阿阿胶
000423 22.2486745424 21.1031222493 21.2715241609 3.04811282251 32.146162425 15.2109027028
000423 1.05428354533
------------------------------------------
000963: 华东医药
000963 28.8490663952 33.0751793465 33.6859045224 5.40565410555 45.9473470387 21.614837362
000963 0.872227058632
------------------------------------------
600066: 宇通客车
600066 11.5798209742 12.6256716804 12.4472764467 1.77044079958 18.6421564576 9.22903889505
600066 0.917164747137
------------------------------------------
600048: 保利地产
600048 8.79230217689 8.2308354972 8.40319487359 1.77477442854 13.2439267036 4.41344438331
600048 1.0682150287
------------------------------------------
600887: 伊利股份
600887 20.5004179832 22.4426984727 21.7029290581 4.0901355517 36.3785644159 15.4144491717
600887 0.913456018143
------------------------------------------
0.892252158691

pb:
000625: 长安汽车
000625 1.88672938693 2.30898861448 0.668301529814
000625 0.817123729019
000625 2012-01-04 00:00:00 1.0831915109 2015-04-28 00:00:00 4.17606811967
------------------------------------------
000423: 东阿阿胶
000423 5.10085638472 4.97734946495 0.8158039071
000423 1.02481379309
000423 2014-06-04 00:00:00 3.59433630868 2013-03-27 00:00:00 7.87259517788
------------------------------------------
000963: 华东医药
000963 6.1281706234 8.95786339371 2.79031952077
000963 0.684110747626
000963 2017-01-16 00:00:00 4.79839765153 2015-08-17 00:00:00 18.1733402115
------------------------------------------
600066: 宇通客车
600066 3.63846951615 2.98062358237 0.577417168967
600066 1.22070748473
600066 2012-01-06 00:00:00 1.95471043797 2015-05-26 00:00:00 4.54682196001
------------------------------------------
600048: 保利地产
600048 1.40346689818 1.57943201226 0.353471471268
600048 0.888589624172
600048 2014-03-10 00:00:00 0.916231053974 2015-04-30 00:00:00 2.6991122622
------------------------------------------
600887: 伊利股份
600887 5.16299985636 5.08598689117 0.884027202438
600887 1.01514218712
600887 2014-06-03 00:00:00 3.50651978924 2013-03-26 00:00:00 8.51622192977
------------------------------------------
600340: 华夏幸福
600340 4.72805018626 4.96245366079 1.3064012927
600340 0.952764601838
600340 2012-01-16 00:00:00 2.40966728251 2015-06-16 00:00:00 9.40109499924
------------------------------------------
000538: 云南白药
000538 5.8567151885 6.09246533442 1.25761032965
000538 0.961304638929
000538 2016-02-29 00:00:00 4.22050890968 2013-09-27 00:00:00 10.2058083742
------------------------------------------
601668: 中国建筑
601668 1.59053861398 0.989479329816 0.304424335803
601668 1.60745006596
601668 2014-03-11 00:00:00 0.617550927244 2015-05-04 00:00:00 2.30600742615
------------------------------------------
601166: 兴业银行
601166 0.890413391482 0.908164137337 0.131851467676
601166 0.980454253669
601166 2013-12-26 00:00:00 0.725583149353 2015-06-08 00:00:00 1.36237354655
------------------------------------------
'''	