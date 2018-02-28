import calendar,arrow,sys,os,time
from stock import Stock

if len(sys.argv) < 2:
    print 'Usage: python max.py symbol'
    sys.exit()

symbol = sys.argv[1]
now = arrow.now()
year = int(now.format('YYYY'))
month = int(now.format('MM'))
dates = []

for y in range(1980,year):
    for m in range(1,13):
        start = '%04d%02d01'%(y,m)
        end = '%04d%02d%02d'%(y,m,calendar.monthrange(y,m)[1])
        dates.append((start, end))

for m in range(1,month+1):
    start = '%04d%02d01'%(year,m)
    end = '%04d%02d%02d'%(year,m,calendar.monthrange(year,m)[1])
    dates.append((start, end))

root = '/home/ubuntu/kf-stock/data/'+symbol
if not os.path.isdir(root):
    os.mkdir(root)

for start,end in dates:
    out = '%s/%s.csv' % (root,start[:-2])
    if os.path.isfile(out):
        continue
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
