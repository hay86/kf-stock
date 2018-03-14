import sys, os
from util import read_stock

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
    bank,share = invest,0
    for i in range(1,len(quotes)):
        if share > 0 and quotes[i][1] < quotes[i-1][1]:
            bank += share*quotes[i-1][1]
            share = 0
        elif bank >= quotes[i-1][1] and quotes[i][1] > quotes[i-1][1]:
            share += bank/quotes[i-1][1]
            bank -= share*quotes[i-1][1]
    return 10000*(bank+share*quotes[i][1]-invest)/invest/100.0

def macd_raw(quotes, invest=1000000, short=12, long=26):
    def macd(quotes, period):
        total = 0
        macd = [0]*len(quotes)
        for i in range(period):
            total += quotes[i][1]
        macd[i] = total/period
        for i in range(period, len(quotes)):
            total -= quotes[i-period][1]
            total += quotes[i][1]
            macd[i] = total/period
        return macd
    macd_short = macd(quotes, short)
    macd_long = macd(quotes, long)
    bank,share = invest,0
    for i in range(long, len(quotes)):
        if macd_short[i] > macd_long[i] and bank >= quotes[i][1]:
            share += bank/quotes[i][1]
            bank -= share*quotes[i][1]
        elif macd_short[i] < macd_long[i] and share > 0:
            bank += share*quotes[i][1]
            share = 0
    return 10000*(bank+share*quotes[i][1]-invest)/invest/100.0

def macd_std(quotes, invest=1000000, short=12, long=26, M=9):
    def ema(quotes, period):
        ret = []
        for i in range(len(quotes)):
            dema = quotes[i][1] if i==0 else (2.0*quotes[i][1]+(period-1)*ret[-1])/(period+1)
            ret.append(dema)
        return ret
    ema_short = ema(quotes, short)
    ema_long = ema(quotes, long)
    bank,share = invest,0
    diff = [ema_short[i] - ema_long[i] for i in range(len(quotes))]
    dea = []
    for i in range(len(diff)):
        ddea = diff[i] if i==0 else (2.0*diff[i]+(M-1)*dea[-1])/(M+1)
        dea.append(ddea)
        macd = 2.0*(diff[i]-dea[i])
        if macd > 0 and bank >= quotes[i][1]:
            share += bank/quotes[i][1]
            bank -= share*quotes[i][1]
        elif macd < 0 and share > 0:
            bank += share*quotes[i][1]
            share = 0
    return 10000*(bank+share*quotes[i][1]-invest)/invest/100.0
    
def turtle(quotes, invest=1000000, short=10, long=20):
    def pmax(quotes, period):
        stk = []
        for i in range(period):
            pass

def stupid_1(quotes, invest=1000000):
    share = invest/quotes[0][1]
    bank = invest-share*quotes[0][1]
    return 10000*(bank+share*quotes[-1][1]-invest)/invest/100.0

def stupid_2(quotes, invest=1000000):
    pass

print 'Optimal Performance:',optimal(close),'%'
print 'MACD RAW Performance:',macd_raw(close),'%'
print 'MACD STD Performance:',macd_std(close),'%'
print 'Stupid #1 Performance:',stupid_1(close),'%'
