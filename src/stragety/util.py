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

if __name__ == '__main__':
    print read_csv('/home/ubuntu/kf-stock/data/AAPL/201801.csv')
    print read_stock('/home/ubuntu/kf-stock/data', 'AAPL', '201801','201802')
