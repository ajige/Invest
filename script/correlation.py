import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import Series
from pandas import DataFrame
import tushare as ts
import getdata
from scipy.stats.stats import pearsonr 

def GetClose():
	global date,second
	ret = Series(index = date)
	prev = 0
	firstunzero = 0
	#print ret.index
	#print second.index
	#for d in ret.index:
	#	print d
		
	for d in ret.index:
		if d in second.index:
			#print second['close'][d]
			ret[d] = second['close'][d]
			#print d, ret[d]
			prev = ret[d]
			if firstunzero == 0:
				firstunzero = prev
		else:
			ret[d] = prev
	
	for d in date:
		if ret[d] == 0:
			ret[d] = firstunzero
	return ret

	
date = pd.date_range('01/01/2012', end='06/30/2017')
#sz50 = ts.get_sz50s()
sz50 = getdata.GetHs300()
#sz50 = getdata.GetHs300()
#sz50 = sz50.append({'code':'sh', 'name':'index','date': '2016-08-01','weight':0}, ignore_index=True)
sz50code = sz50.index

df = DataFrame(columns=sz50code)
rawdict = {}
namedf = {}
	

sz50code, nameseries, price, volume = getdata.GetPriceVolume()
corrdf = price.corr()
vvdf = volume.corr()
#print corrdf['000625']['sh']
#print corrdf['000423']['sh']
#print corrdf['000963']['sh']
#codelist = ['000625', '000423', '000963', '600887', '600048', '600066']
codelist = ['601668', '600887', '601166', '000001','600886', '000963','000423', '000625', '600066', '600048', '000538']

for code in codelist:
	for c2 in codelist:
		if code != c2:
			print "%s: %s : %f, %f"  %(sz50['name'][code].decode('UTF-8'), sz50['name'][c2].decode('UTF-8'), corrdf[code][c2], vvdf[code][c2])


			
	# for idx in range(0, sz50.index.size):
	# code = sz50.index[idx]
	# name = sz50['name'][code].decode('UTF-8')
	# print code, name
	# filename = 'C:\quant\\pv\\%s.csv' % (code)
	# print filename
	# #second = ts.get_h_data(code)
	
	# second = pd.read_csv(filename, encoding="gbk", index_col=0,parse_dates=True)
	# rawdict[code] = second
	# #ret2 = GetClose()
	# #df[code] = ret2
	# #print ret2
	# namedf[code] = name
	# print "code: %s, name %s finish downloading"%(code, namedf[code])
	
# price  = DataFrame({tick: data['close'] for tick, data in rawdict.iteritems()})
# volume = DataFrame({tick: data['volume'] for tick, data in rawdict.iteritems()})	
# final  = DataFrame(columns= sz50code, index=sz50code)


#0.886006129806
#0.546253346158
#0.673349483003
'''
#for code1 in ('000625', '000333', '600887', '600340', '000538', '000423', '600066', '601668', '601166', '600115'):
for code1 in ('600066',
'601668',
'002304',
'000538',
'002236',
'002294',
'002027',
'000963',
'000625',
'600276',
'002415',
'300017',
'000423',
'600340',
'601166',
'300015'):
	print '-------------------------'
	print code1
	corrseries = corrdf[code1]
	ret = corrseries.sort_values(axis=0, ascending=True, kind='quicksort', na_position='last', inplace=False)
	for i in range(0,5):
		code = ret.index[i]
		print code, sz50['name'][code].decode('UTF-8'), ret[i]
	print'----------------'
	for i in range(-5,0):
		code = ret.index[i]
		print code, sz50['name'][code].decode('UTF-8'), ret[i]

	#print ret[0:5]
	#print ret[-5:]
#print final
'''

#tempseries = final['601668']
#tempseries.sort(axis=0, ascending=True, kind='quicksort', na_position='last', inplace=False)
#print tempseries

# for code1 in sz50code:
	# max = 0
	# maxcode=code1
	# min = 0
	# mincode = code1
	# print "code: %s, name: %s" % (code1, namedf[code1])
	
	# for code2 in sz50code:
		# if final[code1][code2] > max:
			# max = final[code1][code2]
			# maxcode = code2		
		# elif final[code1][code2] < min:
			# min = final[code1][code2]
			# mincode = code2		
		
	# print "max positive similarity: maxcode %s, maxname: %s, similarity: %f" % (maxcode, namedf[maxcode], max)
	# print "max negative similarity: mincode %s, minname: %s, similarity: %f" % (mincode, namedf[mincode], min)
		
#price['601333'].plot()
#price['000002'].plot()

#plt.show()


# for code1 in sz50code:
	# for code2 in sz50code:
		# if code2 == code1:
			# continue
		# print price[code1]
		# print price[code2]
		# #print df[code1]
		# #print df[code2]
		# print pearsonr(price[code1], price[code2])
		# break
		# final[code1][code2] = pearsonr(price[code1], price[code2])[0]
	# break

	