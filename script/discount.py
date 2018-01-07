
## money means amount in year years later
## year means years
## avg means average of society
def discount(money, year, avg)
	return round(money / (1+avg)**year, 3)

## money means amount in current
## year means years
## avg means average of society 
def rediscount(money, year, avg)
	return round(money*(1+avg)**year, 3)
	
	
	