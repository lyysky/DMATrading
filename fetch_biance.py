import ccxt
import time
from numpy import mean

#获取均线数据，i:k线数; j:级别。周线'w',日线'd', 小时线'h',分钟线'm'
def get_ma(symbol_v, i, j):
	ma_i = i
	candle_l = exchange.fetch_ohlcv(symbol_v, j) #爬交易所蜡烛图数据
	candle_l.reverse()
	candle_idays_l = []
	k = 0
	while k < ma_i:
		candle_idays_l.append(candle_l[k][4]) #列表第4个元素表示收盘价
		k += 1
	ma_i = mean(candle_idays_l)
	#print ("%s MA%d = %.2f" %(j, i, ma_i))
	return ma_i

#获取上一根均线数据，i:k线数; j:级别。周线'w',日线'd', 小时线'h',分钟线'm'
def get_ma_last(symbol_v, i, j):
	ma_i = i
	candle_l = exchange.fetch_ohlcv(symbol_v, j) #爬交易所蜡烛图数据
	candle_l.reverse()
	candle_idays_l = []
	k = 1
	while k <= ma_i:
		candle_idays_l.append(candle_l[k][4]) #列表第4个元素表示收盘价
		k += 1
	ma_i = mean(candle_idays_l)
	#print ("The last %s MA%d = %.2f" %(j, i, ma_i))	
	return ma_i

def cross(i, j, k):
	price_i = get_ma(symbol_v, i, k)
	price_j = get_ma(symbol_v, j, k)
	price_i_last = get_ma_last(symbol_v, i, k)
	price_j_last = get_ma_last(symbol_v, j, k)
	price_diff =  price_i - price_j
	price_diff_last = price_i_last - price_j_last
	if price_diff * price_diff_last < 0:    #cross= 0:no cross; 1:golden cross; 2:dead cross;
		if price_diff > 0:
			cross = 1
			if position == 0:
				print ("golden cross")
		else:
			cross = 2
			if position == 1:
				print ("dead cross")
	else:
		cross = 0
		#print ("no cross")
	return cross

#金叉开仓买入，死叉卖出，每次10000usd。
def open_or_close_position(if_cross, symbol_v, price_v):
	global position
	global amount_v
	global buy_price_d
	global sell_price_d
	if if_cross == 1:  #gloden cross
		#exchange.create_order(symbol=symbol_v, side='buy', type='limit', price=price_v[1], amount=amount_v)
		if position == 0:
			position += 1
			buy_or_sell = 1
			buy_price_d[str(price_v[2])] = price_v[1]
			amount_v = 10000 / price_v[1]
			print ("buy_price_d is %s" %(buy_price_d))
		else:
			buy_or_sell = 0
	elif if_cross == 2 :  #dead cross
		#exchange.create_order(symbol=symbol_v, side='sell', type='limit', price=price_v[0], amount=amount_v)
		if position >> 0:
			position -= 1
			buy_or_sell = 2
			sell_price_d[str(price_v[2])] = price_v[0]
			amount_v = 10000 / price_v[0]
			print ("sell_price_d is %s" %(sell_price_d))
	#return buy_or_sell

#获取当前的价格。bid: 买一价，ask: 卖一价
def get_price(symbol_v):
	fetchticker = exchange.fetchTicker(symbol=symbol_v)
	bid_and_ask = [fetchticker['bid'], fetchticker['ask'], fetchticker['datetime']]
	price_v = bid_and_ask
	#print ("bid_and_ask = %s" %(bid_and_ask))
	return price_v

#计算收益
def caculate_profit(sell_price_d, buy_price_d):
	global buy_price_l
	global sell_price_l
	global profit
	profit_one = 0
	j = 0
	if len(sell_price_d) >> 0:
		buy_price_l = list(buy_price_d.values())
		sell_price_l = list(sell_price_d.values())
		buy_price_d.clear()
		sell_price_d.clear()
		for i in sell_price_l:
			profit = (i - buy_price_l[j] - 0.0004*(i + buy_price_l[j])) * amount_v + profit
			profit_one = (i - buy_price_l[j] - 0.0004*(i + buy_price_l[j])) * amount_v
			print ("profit of this time = %.2f" %(profit_one))
			j += 1
	return profit




exchange = ccxt.binance()

#apiKey 和 secret 去交易所生成，可以通过这个apikey查看账户余额、下单等等，一定不能泄露
#exchange.apiKey = 'xxxxxxx'
#exchange.secret = 'xxxxxxx'
#balance = exchange.fetch_balance()
#exchange.create_order(symbol='EOS/USDT', side='buy', type='limit', price=2.9, amount=1)
#order_info = exchange.create_limit_buy_order(symbol, amount, price) #限价买单
#order_info = exchange.cancel_order(id='659521969', symbol="EOS/USDT") #撤单
#print(order_info)
#print (order_info['id'])
#print (balance['used'])

#data = exchange.fetchTicker(symbol='EOS/USDT')





symbol_v = 'BTC/USDT'
amount_v = 9
position = 0
profit = 0
buy_price_d ={}
sell_price_d ={}

t = 0
print ("--------START---------")
while t < 50000:
	price_v = get_price(symbol_v)
	if_cross = cross(5, 21, '1m')
	open_or_close_position(if_cross, symbol_v, price_v)
	profit = caculate_profit(sell_price_d, buy_price_d)
	t += 1
print ("profit = %.2f" %(profit))
print ("---------END----------")

exit()