import calendar,arrow,sys,os,time
from stock import Stock

if len(sys.argv) < 2:
    print 'Usage: python max.py symbol [fromdate:YYYYMMDD [todate:YYYYMMDD]]'
    sys.exit()

now = arrow.now()
year = int(now.format('YYYY'))
month = int(now.format('MM'))

symbol = sys.argv[1]
start = sys.argv[2] if len(sys.argv) > 2 else '%04d%02d01'%(year, month)
end = sys.argv[3] if len(sys.argv) > 3 else '%04d%02d%02d'%(year, month, calendar.monthrange(year, month)[1])
dates = []

root = '/home/ubuntu/kf-stock/data/'+symbol
if not os.path.isdir(root):
    os.mkdir(root)

out = '%s/%s.csv' % (root,start[:-2])
print arrow.now(), 'fetch', symbol, start, '-', end
for i in range(3):
    try:
        s = Stock(symbol, start, end)
        if len(s.values) > 0:
            break
    except Exception, e:
        print arrow.now(), 'retry#%d'%i
        print e
    time.sleep(10)
if len(s.values) == 0:
    print arrow.now(), 'no values'
else:
    print arrow.now(), 'write', symbol, '=>', out
    fout = open(out,'w')    
    for v in s.values:
        fout.write(','.join([str(x) for x in v]))
        fout.write("\n")
    fout.close()
