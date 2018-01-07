from __future__ import division
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import Series
from pandas import DataFrame
from scipy.stats.stats import pearsonr

def calcpe(n, g1, g2, g3, r, netasset, netprofit):
	gg = (1+g1)*(1+g2)*(1+g3)
	g = gg**(1.0/3) - 1 
	#print g1, g2, g3, g
	if(g > g3):
		g = g3
		
	a1 = netasset / netprofit
	a2 = 0
	a3 = 0
	for i in range(1, n+1):
		a2 = a2 + (1 + g)**i / (1 + r)**i
		#print i, a2
		
	g3 = (1+g)**n
	for i in range(n+1, 20):
		cg = g - 0.05 * (i - n)
		if(cg < 0):
			cg = 0
	
		a3 = a3 + g3 * (1 + cg)/((1+r)**i)
		g3 = g3 * (1 + cg)
		#print i, a3
		
	print n, g, r, netasset, netprofit, a1, a2, a3

	ret = a1 + a2 + a3
	print ret, ret * netprofit
	return ret

def calcpb(n, N, roe1, roe2, roe3, r):
	roe = (1+roe1)*(1+roe2)*(1+roe3)
	roe = roe**(1.0/3) - 1 
	#print g1, g2, g3, g
	# if(temproe > g3):
		# g = g3
	
	ret = 1
	for i in range(1, N+1):
		if i in range(1,n+1):
			temproe = roe
		else:
			temproe = temproe / (1 + temproe)
			#temproe = roe - (i - n) * 0.05
			
		if temproe < r:
			temproe = r
			
		ret = ret * (1 + temproe)
		#print i, temproe, ret
		
	ret = ret / ((1 + r)**N)
	print n, N, roe, r, ret
	return ret
	
if __name__ == "__main__": 
	

	# ret = calcpe(3, 0.316, 0.4497, 0.3189, 0.065, 14.97, 1.50)
	# print "huadongyiyao: %f" % ret, ret * 1.50  ##31,current 33
	
	# ret = calcpe(5, 0.316, 0.4497, 0.3189, 0.065, 14.97, 1.50)
	# print "huadongyiyao: %f" % ret, ret * 1.50
	
	# ret = calcpe(3, 0.30, 0.1176, 0.22, 0.065, 4.08, 0.93)
	# print "yiligufen: %f" % ret, ret * 0.93  ##31,current 33
	 
	# ret = calcpe(5, 0.30, 0.1176, 0.22, 0.065, 4.08, 0.93)
	# print "yiligufen: %f" % ret, ret * 0.93  ##31,current 33
	
	# ret = calcpe(3, 0.135, 0.19, 0.14, 0.065, 13.71, 2.83)
	# print "dongeejiao: %f" % ret, ret * 2.83  ##31,current 33
	
	# ret = calcpe(5, 0.135, 0.19, 0.14, 0.065, 13.71, 2.83)
	# print "dongeejiao: %f" % ret, ret * 2.83  ##31,current 33
	
	# ret = calcpe(3, 0.078, 0.078, 0.078, 0.065, 62.9, 13.31)
	# print "guizhoumaotai: %f" % ret, ret * 13.31  ##31,current 33
	
	# ret = calcpe(5, 0.078, 0.078, 0.078, 0.065, 62.9, 13.31)
	# print "guizhoumaotai: %f" % ret, ret * 13.31  ##31,current 33
	
	# ret = calcpe(10, 0.078, 0.078, 0.078, 0.065, 62.9, 13.31)
	# print "guizhoumaotai: %f" % ret, ret * 13.31  ##31,current 33
	
	#ret = calcpe(3, 0.107, 0.155, 0.146, 0.065, 6.02, 0.96)
	#print "zhongguojianzhu: %f" % ret, ret * 0.96  ##31,current 33
	
	# ret = calcpe(5, 0.107, 0.155, 0.146, 0.065, 6.02, 0.96)
	# print "zhongguojianzhu: %f" % ret, ret * 0.96  ##31,current 33
	
	
	#print "guotoudianli: %f" % calcpe(1, 0.0, 0.065, 4.36, 0.58)  ##19.5, current: 13.8
	# print "yiligufen: %f, %f" % (calcpe(3, 0.2, 0.065, 0.38, 0.93), calcpe(3, 0.2, 0.065, 0.38, 0.93) * 0.93)
	# print "yiligufen: %f, %f" % (calcpe(3, 0.15,0.065, 0.38, 0.93), calcpe(3, 0.15,0.065, 0.38, 0.93)*0.93)
	# print "zhongguojianzhu: %f, %f" % (calcpe(3, 0.146, 0.065, 5.78, 0.96), calcpe(3, 0.146, 0.065, 5.78, 0.96)*0.96)
	
	'''
	print "xingyeyinhang: %f, %f" % (calcpe(1, 0, 0, 0, 0.065, 17.02, 2.77), calcpe(1, 0, 0, 0, 0.065, 17.02, 2.77)*2.77)
	# print "zhaoshangyinhang: %f, %f" % (calcpe(1, 0, 0.065, 15.95, 2.46), calcpe(1, 0, 0.065, 15.95, 2.46)*2.46)
	# print "guizhoumaotai: %f, %f" % (calcpe(10, 0.078, 0.065, 58.03, 13.31), calcpe(10, 0.078, 0.065, 58.03, 13.31)*13.31)
	
	ret = calcpb(5, 20, 0.16, 0.25, 0.222, 0.065)
	print "huadongyiyao: %f, %f" % (ret, ret * 16.09)

	ret = calcpb(5, 20, 0.237, 0.2387, 0.266, 0.065)
	print "yiligufen: %f, %f" % (ret, ret * 4.08) ## 

	ret = calcpb(5, 20, 0.248, 0.248, 0.248, 0.065)
	print "dongeejiao: %f, %f" % (ret, ret * 13.7)
	
	ret = calcpb(5, 20, 0.147, 0.218, 0.269, 0.065)
	print "guotoudianli: %f, %f" % (ret, ret * 4.36) ## 
	
	ret = calcpb(5, 20, 0.1587, 0.16, 0.177, 0.065)
	print "zhongguojianzhu: %f, %f" % (ret, ret * 6.02) ##

	ret = calcpb(5, 20, 0.1728, 0.189, 0.212, 0.065)
	print "xingyeyinhang: %f, %f" % (ret, ret * 17.02) ## 
	
	ret = calcpb(10, 20, 0.244, 0.262, 0.32, 0.065)
	print "guizhoumaotai: %f, %f" % (ret, ret * 62.9) ## 
	'''
	ret = calcpb(5, 20, 0.125, 0.155, 0.186, 0.065)
	print "baolidichan: %f, %f" % (ret, ret * 7.94) ##
	
	ret = calcpb(5, 20, 0.1587, 0.16, 0.177, 0.065)
	print "zhongguojianzhu: %f, %f" % (ret, ret * 6.91) ##
	
	ret = calcpb(5, 20, 0.28, 0.295, 0.421, 0.065)
	print "huaxiaxingfu: %f, %f" % (ret, ret * 12.67)
	
	ret = calcpe(5, 0.437, 0.352, 0.357, 0.065, 12.67, 2.52)
	print "huaxiaxingfu: %f" % ret, ret * 2.52  ##31,current 33
	
	
	