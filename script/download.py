# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import Series
from pandas import DataFrame
import tushare as ts
from scipy.stats.stats import pearsonr 
import pdb 
# date = pd.date_range('10/01/2012', end='26/01/2017')
#sz50 = ts.get_hs300s();
#sz50code = sz50['code']

sz50code = ['000300']
#pdb.set_trace()
#download div data
# for y in [2016]:
	# filename = "C:\quant\\basic\\div\\%d.csv" % y
	# df = ts.profit_data(year = y, top = 3000)
	# df.to_csv(filename)
	# print "%d finish download" % y

'''
df = ts.profit_data()
filename = "C:\quant\\basic\divid.csv"
df.to_csv(filename)
print "%s finish" % filename
'''	
def GetHs300():
	hs300 = pd.read_csv('c:\\quant\\basic\\hs300.csv', index_col=0, encoding='utf-8', dtype={'code':np.str})
	hs300 = hs300.set_index('code')
	return hs300

def GetZz500():
	hs300 = pd.read_csv('c:\\quant\\basic\\zz500.csv', index_col=0, encoding='utf-8', dtype={'code':np.str})
	hs300 = hs300.set_index('code')
	return hs300
	
def loadpv():
	start = True
	ff = open('c:\\quant\\script\\bankcode', 'r')
	codelist = []
	for line in ff:
		print line
		if line[-1] == '\n':
			codelist.append(line[0:-1])
	
	print pd.datetime.today().date().strftime('%Y-%m-%d')
	
	#codelist = GetHs300().index
	#codelist = GetZz500().index

	#codelist = ['000423', '600519']		
	codelist = ['000625', '000423', '000963', '600066', '600048', '600887', '600340', '000538', '601668', '000001',  '601166', '600886', '600016', '600104', '000883']	
	#codelist=['600000', '600036', '600016', '601818', '601998']
	#codelist = ['000538', '000423','000963', '600887', '601166', '601668', '600886', '600048','000069', '600066']
	#codelist = ['601668', '600887', '601166', '000001','600886', '000963','000423', '000625', '600066', '600048', '000538']
	#codelist = ['601166', '000001', '600036']
	#codelist = ['000900']
	for code in codelist:
		print "code: %s" % code
		#if code == '600109':
		#	start = True
		if start:
			filename = "C:\quant\\pv\%s.csv" % code
			print filename
			#df = ts.get_h_data(code, start="2010-01-01",  end = pd.datetime.today().date().strftime('%Y-%m-%d'))
			df = ts.get_k_data(code, start="2011-01-01",  end = pd.datetime.today().date().strftime('%Y-%m-%d'))
			df.to_csv(filename)
			print "%s finish" % filename
			
def loadprofit():
	for year in [2017]:
	  for quarter in [3]:
		 profit = ts.get_profit_data(year, quarter)
		 filename = "C:\quant\\basic\\profit\\%s%s.csv" % (year, quarter)
		 print filename
		 profit.to_csv(filename, encoding='utf-8')

def loadgrowth():
	for year in [2017]:
	  for quarter in [3]:
		 profit = ts.get_growth_data(year, quarter)
		 filename = "C:\quant\\basic\\growth\\%s%s.csv" % (year, quarter)
		 print filename
		 profit.to_csv(filename, encoding='utf-8')
		 
def loadreport():
	for year in [2017]:
	  for quarter in [3]:
		 profit = ts.get_report_data(year, quarter)
		 filename = "C:\quant\\basic\\report\\%s%s.csv" % (year, quarter)
		 print filename
		 profit.to_csv(filename, encoding='utf-8')
		 
loadpv()
#loadprofit()
#loadgrowth()
#loadreport()

#code = 'sh'
#filename = "C:\quant\\tsdata\%s.csv" % code
#df = ts.get_hist_data(code, start="2012-01-01",  end="2016-11-20")
#df.to_csv(filename)
#print "%s finish" % filename

		
#classify = ts.get_industry_classified()
#filename = "C:\quant\\basic\\classified.csv"
#classify.to_csv(filename, encoding='utf-8')
		
#hs300 = ts.get_hs300s()
#hs300 =ts.get_h_data('399106', start="2012-01-01",  end="2017-01-26", index=True)
#filename = "C:\quant\\pv\\hs300.csv"
#hs300.to_csv(filename)

#sz50 = ts.get_sz50s()
#filename = "C:\quant\\basic\\sz50.csv"
#sz50.to_csv(filename, encoding='utf-8')

#basic = ts.get_stock_basics()
#filename = "C:\quant\\basic\\basic.csv"
#basic.to_csv(filename)

# zz500 = ts.get_zz500s()
# print zz500.sort(['weight'], ascending= False)
# filename = "C:\quant\\basic\\zz500.csv"
# zz500.to_csv(filename, encoding='utf-8')



