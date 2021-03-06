
# 可以自己import我们平台支持的第三方python模块，比如pandas、numpy等。
import pandas as pd
import numpy as np
import datetime
import math
import talib
CAP=0
OBSERVATION = 40
SMA5 = 5
SMA10=10
# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    context.fja_list=['150283.XSHE','150249.XSHE','502007.XSHG','150259.XSHE','150217.XSHE','150245.XSHE','502049.XSHG','150241.XSHE','150231.XSHE','150257.XSHE','150169.XSHE','150177.XSHE','150243.XSHE','150329.XSHE','150051.XSHE','150179.XSHE','150186.XSHE','150255.XSHE','150171.XSHE','150315.XSHE','150227.XSHE','150018.XSHE','150237.XSHE','150235.XSHE','150279.XSHE','150305.XSHE','150269.XSHE','150181.XSHE','502004.XSHG','150229.XSHE','150173.XSHE','150277.XSHE','150200.XSHE','150209.XSHE','150194.XSHE','150273.XSHE','150184.XSHE','150205.XSHE','150309.XSHE','150275.XSHE']

    context.cur_stock=''
    update_universe(context.fja_list)
    scheduler.run_daily(rebalance)
    context.flag=True
                     

# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):

    pass
    
def before_trading(context):
    
    
    
    
    num_stocks = 20
    
    #删选股票
    fundamental_df = get_fundamentals(
        query(
            fundamentals.eod_derivative_indicator.dividend_yield,
            fundamentals.financial_indicator.inc_operating_revenue,
            fundamentals.eod_derivative_indicator.market_cap 
        ).filter(
            fundamentals.financial_indicator.inc_operating_revenue >5
        ).filter(
            fundamentals.eod_derivative_indicator.dividend_yield > 4.5
        )
        
        .order_by(
            fundamentals.eod_derivative_indicator.dividend_yield .desc()
        ).limit(
            num_stocks
        )
    )
    
    li=list(fundamental_df.columns.values)
    if context.flag:
        dividend = []
        for stock in li:
          di = float(fundamental_df[stock]['dividend_yield'])/100
          di = di*float(fundamental_df[stock]['market_cap'])
          dividend.append([di])
        div=np.array(dividend)
        context.df = pd.DataFrame(div.T,index=['dividend'],columns=li)
        logger.info(context.df)
        context.flag = False
    else:
        li2 = list(context.df.columns.values)
        for stock in li:
            if stock not in li2:
                di = float(fundamental_df[stock]['dividend_yield'])/100
                di = di*float(fundamental_df[stock]['market_cap'])
                context.df.insert(0,stock,[di])
            else:
                di = float(fundamental_df[stock]['dividend_yield'])/100
                di = di*float(fundamental_df[stock]['market_cap'])
                context.df[stock]['dividend']=di
    #logger.info(context.df)
    
    stocks=context.df.columns.values
    
    fundamental_df = get_fundamentals(
        query(
            fundamentals.eod_derivative_indicator.market_cap,fundamentals.financial_indicator.inc_operating_revenue
        ).filter(
            fundamentals.financial_indicator.inc_operating_revenue >5
        ).filter(
            fundamentals.income_statement.stockcode.in_(stocks)
        )
    )
    stocks=fundamental_df.columns.values
    
    dividend_yield=[]
    for stock in stocks:
        rate=context.df[stock]['dividend']/float(fundamental_df[stock]['market_cap'])
        dividend_yield.append(rate)
    
    df = pd.DataFrame(dividend_yield,index=stocks,columns=['dividend_yield'])
    df=df[df['dividend_yield']>0.06]
    logger.info(df)
    
    context.fundamental_df = fundamental_df
    
    context.stocks = df.T.columns.values
	
def rebalance(context,bar_dict):
    stocks = set(list(context.stocks))
    num = 0
    num=len(stocks)
    if num>9:
        num=0
    else:
        num=(10-num)/10
    holdings = set(get_holdings(context))
    
    to_buy = stocks - holdings
    to_sell = holdings - stocks
    if not context.cur_stock=='':
        logger.info(num)
        order_target_percent(context.cur_stock,num)
        if context.cur_stock in to_sell:
            to_sell.remove(context.cur_stock)
    to_buy=list(to_buy)

    for stock in to_sell:
        high = history(OBSERVATION,'1d','high')[stock].values
        low = history(OBSERVATION,'1d','low')[stock].values
        close = history(OBSERVATION,'1d','close')[stock].values
        MIX = (high + low +close)/3   
        sma = talib.SMA(MIX,20) 
        currentPrice = bar_dict[stock].close
        if sma[-1]>0:
            if currentPrice < sma[-1]:
                if  (bar_dict[stock].low<bar_dict[stock].high*0.995):
                    order_target_percent(stock , 0)       
    if len(to_buy) == 0:
        return
    
    to_buy = get_trading_stocks(to_buy, context, bar_dict)
    cash = context.portfolio.cash
    portfolio_value=context.portfolio.portfolio_value
    if len(to_buy) >0:
        average_value = context.portfolio.cash*0.95/len(to_buy)
        if average_value>context.portfolio.portfolio_value *0.1:
            average_value=context.portfolio.portfolio_value *0.1
            
    for stock in to_buy:
        if bar_dict[stock].is_trading:
            if (bar_dict[stock].low<bar_dict[stock].high*0.995)and(history(3,'1d','close')[stock].ix[1]>0):
                    order_target_value(stock, average_value)
            
    
    min_stock='150283.XSHE'#当日最小折价率基金
    min_discount=0#当日最小折价率
    cur_discount=0#当前持仓基金折价率
    #获得当前持仓基金折价率
    if context.cur_stock!='':
        cur_discount=bar_dict[context.cur_stock].discount_rate
    #获得当日最小折价率基金代码及折价率
    for stock in context.fja_list:
        if min_discount>bar_dict[stock].discount_rate:
            min_stock=stock
            min_discount=bar_dict[stock].discount_rate
    #第一次买入       
    if context.cur_stock=='':
        shares = context.portfolio.cash/bar_dict[min_stock].close
        order_shares(min_stock,shares)
        logger.info("买入:"+min_stock+str(shares))
        context.cur_stock=min_stock
    else:
        #如果当日最小折价率与当前持仓折价率相差超过1则轮仓
        if context.cur_stock!=min_stock and bar_dict[min_stock].is_trading and bar_dict[context.cur_stock].is_trading and cur_discount-min_discount>1:
            order_target_percent(context.cur_stock,0)
            logger.info("卖出:"+context.cur_stock)
            shares = context.portfolio.cash/bar_dict[min_stock].close
            order_shares(min_stock,shares)
            logger.info("买入:"+min_stock+str(shares))
            context.cur_stock=min_stock
    logger.info(context.cur_stock+str(cur_discount))     
    
def get_trading_stocks(to_buy, context, bar_dict):
    trading_stocks = []
    for stock in to_buy:
        if bar_dict[stock].is_trading:
            trading_stocks.append(stock)
    
    return trading_stocks

def get_holdings(context):
    positions = context.portfolio.positions
    
    holdings = []
    for position in positions:
        if positions[position].quantity > 0:
            holdings.append(position)
    
    return holdings