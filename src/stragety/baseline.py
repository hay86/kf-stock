import sys, os
from util import read_stock, avg, ema, metrics

if len(sys.argv) < 4:
    print 'Usage: python baseline.py symbol start_date:YYYYMM end_date:YYYYMM'
    sys.exit()

root = '/'.join(os.getcwd().split('/')[:-2]) + '/data'
symbol = sys.argv[1]
start = sys.argv[2]
end = sys.argv[3]

quotes = read_stock(root, symbol, start, end)
# date open high low close adjclose volume
close = [(x[0],x[5]) for x in quotes]

def optimal(quotes, invest=1000000):
    bank,share,assets = invest,0,[invest]
    for i in range(1,len(quotes)):
        if share > 0 and quotes[i][1] < quotes[i-1][1]:
            bank += share*quotes[i-1][1]
            share = 0
        elif bank >= quotes[i-1][1] and quotes[i][1] > quotes[i-1][1]:
            share += bank/quotes[i-1][1]
            bank -= share*quotes[i-1][1]
        assets.append(bank+share*quotes[i][1])
    return assets

def macd_avg(quotes, invest=1000000, short=12, long=26):
    bank,share,assets = invest,0,[invest]*long
    avg_short = avg([x[1] for x in quotes], short)
    avg_long = avg([x[1] for x in quotes], long)
    for i in range(long, len(quotes)):
        if avg_short[i] > avg_long[i] and bank >= quotes[i][1]:
            share += bank/quotes[i][1]
            bank -= share*quotes[i][1]
        elif avg_short[i] < avg_long[i] and share > 0:
            bank += share*quotes[i][1]
            share = 0
        assets.append(bank+share*quotes[i][1])
    return assets

def macd_dif(quotes, invest=1000000, short=12, long=26, M=9):
    bank,share,assets = invest,0,[]
    ema_short = ema([x[1] for x in quotes], short)
    ema_long = ema([x[1] for x in quotes], long)
    diff = [ema_short[i] - ema_long[i] for i in range(len(quotes))]
    for i in range(len(diff)):
        macd = diff[i]
        if macd > 0 and bank >= quotes[i][1]:
            share += bank/quotes[i][1]
            bank -= share*quotes[i][1]
        elif macd < 0 and share > 0:
            bank += share*quotes[i][1]
            share = 0
        assets.append(bank+share*quotes[i][1])
    return assets

def macd_dea(quotes, invest=1000000, short=12, long=26, M=9):
    bank,share,assets = invest,0,[]
    ema_short = ema([x[1] for x in quotes], short)
    ema_long = ema([x[1] for x in quotes], long)
    diff = [ema_short[i] - ema_long[i] for i in range(len(quotes))]
    dea = ema(diff, M)
    for i in range(len(diff)):
        macd = 2.0*(diff[i]-dea[i])
        if macd > 0 and bank >= quotes[i][1]:
            share += bank/quotes[i][1]
            bank -= share*quotes[i][1]
        elif macd < 0 and share > 0:
            bank += share*quotes[i][1]
            share = 0
        assets.append(bank+share*quotes[i][1])
    return assets
    
def turtle_raw(quotes, invest=1000000, short=10, long=20):
    def pmax(quotes, period):
        stk = []
        for i in range(period):
            pass

def print_metrics(assets, close, label):
    print '[',label,']'
    m = metrics(assets, [x[1] for x in close])
    print '%20s' % 'Returns', '=>', '%.2f%%' % (100*m['returns'])
    print '%20s' % 'Annual Returns', '=>', '%.2f%%' % (100*m['annual returns'])
    print '%20s' % 'Benchmark Returns', '=>', '%.2f%%' % (100*m['benchmark returns'])
    print '%20s' % 'Alpha', '=>', '%.4f' % m['alpha']
    print '%20s' % 'Beta', '=>', '%.4f' % m['beta']
    print '%20s' % 'Sharpe Ratio', '=>', '%.4f' % m['sharpe ratio']
    print '%20s' % 'Volatility', '=>', '%.4f' % m['volatility']
    print '%20s' % 'Information Ratio', '=>', '%.4f' % m['information ratio']
    print '%20s' % 'Max Drawdown', '=>', '%.2f%%' % (100*m['max drawdown'])
    print ''

print_metrics(optimal(close), close, 'Optimal')
print_metrics(macd_avg(close), close, 'MACD AVG')
print_metrics(macd_dif(close), close, 'MACD DIF')
print_metrics(macd_dea(close), close, 'MACD DEA')
