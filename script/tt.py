import numpy as np  
import matplotlib.mlab as mlab  
import matplotlib.pyplot as plt  
from matplotlib.ticker import  MultipleLocator
from matplotlib.ticker import  FormatStrFormatter

xmajorLocator = MultipleLocator(10);

# example data  
#mu = 100 # mean of distribution  
#sigma = 15 # standard deviation of distribution  
#x = mu + sigma * np.random.randn(10000)  
#num_bins = 100 


#reader number
def latency_reader():
	x=[1,10,100,1000,2000]
	y=[845,997,1188,1495,2154]

	fig, ax = plt.subplots()
	plt.plot(x,y,marker='*')
	ax.set_xscale('log')
	plt.xlabel('Reader process number\n write speed = 1000')  
	plt.ylabel('Latency(ms)')  
	plt.title('Latency -- Reader number')

def latency_writespeed():
	x=[30,100,1000,2000,5000,10000]
	y=[1000, 1065, 1164, 1165, 1267, 1987]

	fig, ax = plt.subplots()
	plt.plot(x,y,marker='*')
	ax.set_xscale('log')
	plt.xlabel('Write speed per second\n reader number = 100')  
	plt.ylabel('Latency(ms)')  
	plt.title('Latency -- Write speed')

latency_writespeed()
plt.show()
	
#zz=np.arange(1.,10.,0.5)
#print zz
#the histogram of the data  
#n, bins, patches = ax.hist(x, zz,facecolor='blue', normed=1, cumulative=1, align='mid') 
#ax.set_yticks(np.arange(0,1.2,0.1))
#print n

# value=[100,200,1200,1600,1900,2000,3000,4200,5500,5800,9000]
# fig = plt.figure("zz")
# plt.hist(value, normed=1, cumulative=1, bins=20, align='right')
# ax = plt.gca()
# ax.set_xticks([1000,2000,3000,4000,5000,6000,7000,8000,9000,1000])
# # add a 'best fit' line  
# #y = mlab.normpdf(bins, mu, sigma)  
# #ax.plot(bins, y, 'r--')  
# plt.xlabel('Smarts')  
# plt.ylabel('Probability')  
# #fig.tight_layout()
# plt.title(r'Histogram of IQ: $\mu=100$, $\sigma=15$')  
#ax.xaxis.set_major_locator(xmajorLocator)
#plt.xticks(x, [40,50,60,70,75,80,90,100,150], rotation=0)
# Tweak spacing to prevent clipping of ylabel  
#plt.subplots_adjust(left=0.15)  
  