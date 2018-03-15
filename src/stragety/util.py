import sys,os

def read_csv(path):
    ret = []
    fin = open(path)
    for line in fin:
        cols = line.strip().split(',')
        if len(cols) > 0:
            ret.append([int(x) for x in cols])
    fin.close()
    return ret

def read_stock(root, symbol, start, end):
    ret = []
    for fn in os.listdir(root+'/'+symbol):
        if start+'.csv' <= fn <= end+'.csv':
            ret.extend(read_csv(root+'/'+symbol+'/'+fn))
    ret.sort(key=lambda x:x[0]) 
    return ret

def avg(quotes, period):
    total = 0.0
    ret = [0]*len(quotes)
    for i in range(period):
        total += quotes[i]
    ret[i] = total/period
    for i in range(period, len(quotes)):
        total -= quotes[i-period]
        total += quotes[i]
        ret[i] = total/period
    return ret

def ema(quotes, period):
    ret = []
    for i in range(len(quotes)):
        if i==0:
            val = quotes[i]
        else:
            val = (2.0*quotes[i]+(period-1)*ret[-1])/(period+1)
        ret.append(val)
    return ret

def mean(arr):
    return float(sum(arr)) / max(len(arr), 1)

def diff_mean(arr):
    m = mean(arr)
    return [x-m for x in arr]

def dot(arr1, arr2):
    return sum([arr1[i]*arr2[i] for i in range(len(arr1))])

def cov(arr1, arr2):
    return dot(diff_mean(arr1), diff_mean(arr2)) / (len(arr1)-1)

def var(arr):
    m = mean(arr)
    return sum([(x-m)**2 for x in arr]) / (len(arr)-1)

def std(arr):
    return var(arr)**0.5

def metrics(assets, quotes):
    if len(assets) != len(quotes):
        return
    N = len(assets)
    ret = {}
    ret['safe returns'] = 0.038
    ret['returns'] = float(assets[-1])/assets[0]-1
    ret['annual returns'] = ret['returns']/N*250
    ret['benchmark returns'] = (float(quotes[-1])/quotes[0]-1)/N*250
    ret['max drawdown'] = 0
    strategy, benchmark = [], []
    max_assets = 0
    for i in range(1,N):
        strategy.append(float(assets[i])/assets[i-1]-1)
        benchmark.append(float(quotes[i])/quotes[i-1]-1)
        max_assets = max(max_assets, assets[i])
        ret['max drawdown'] = max(ret['max drawdown'], 1-float(assets[i])/max_assets)
    ret['beta'] = cov(strategy, benchmark) / var(benchmark)
    ret['alpha'] = (ret['annual returns']-ret['safe returns']) - ret['beta']*(ret['benchmark returns']-ret['safe returns'])
    ret['volatility'] = std(strategy)*(250**0.5)
    ret['sharpe ratio'] = (ret['annual returns']-ret['safe returns'])/ret['volatility']
    diff = [strategy[i]-benchmark[i] for i in range(len(strategy))]
    down_risk = (sum([x**2 for x in diff if x < 0])/(N-1))**0.5*250
    ret['sortino ratio'] = (ret['annual returns']-ret['safe returns'])/down_risk
    ret['information ratio'] = mean(diff)*(250**0.5) / std(diff)
    
    return ret

if __name__ == '__main__':
    print read_csv('/home/ubuntu/kf-stock/data/AAPL/201801.csv')
    print read_stock('/home/ubuntu/kf-stock/data', 'AAPL', '201801','201802')
