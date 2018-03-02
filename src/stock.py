#!/usr/bin/python
# encoding: utf-8

import sys,os,requests,arrow,json,urllib
from lxml import etree

class Stock:

    def __init__(self, symbol, fromdate=None, todate=None):
        self.symbol     = symbol
        self.now        = arrow.now()
        self.fromts     = arrow.get(fromdate,'YYYYMMDD').timestamp if fromdate else self.now.shift(months=-1).timestamp
        self.tots       = (arrow.get(todate,'YYYYMMDD').timestamp + 24*3600) if todate else self.now.timestamp
        self.values     = []
        self.__load__()

    def __load__(self):
        param = 'period1=%d&period2=%d&interval=1d&filter=history&frequency=1d' % (self.fromts, self.tots)
        query = 'https://finance.yahoo.com/quote/%s/history?%s' % (self.symbol, param)
        url = 'http://127.0.0.1:8888?url=%s' % urllib.quote(query)
        
        try:
            content = requests.get(url).content
            r = json.loads(content)
            
            if 'html' in r:
                html = etree.HTML(r['html'])
                rows = html.xpath("//div[@id='Main']//tr")
                for row in rows:
                    try:
                        cols = row.xpath("./td//text()")
                        if len(cols) == 7:
                            date        = arrow.get(cols[0], 'MMM DD, YYYY').format('YYYYMMDD')
                            open        = int(cols[1].replace(',','').replace('.',''))
                            high        = int(cols[2].replace(',','').replace('.',''))
                            low         = int(cols[3].replace(',','').replace('.',''))
                            close       = int(cols[4].replace(',','').replace('.',''))
                            adjclose    = int(cols[5].replace(',','').replace('.',''))
                            volume      = int(cols[6].replace(',','').replace('.',''))
                            self.values.append((date,open,high,low,close,adjclose,volume))
                    except Exception, e:
                        print arrow.now(), e
        except Exception, e:
            print arrow.now(), e


if __name__ == '__main__':
        if len(sys.argv) < 2:
            print 'Usage: python stock.py symbol [fromdate:YYYYMMDD, [todate:YYYYMMDD]]'
            sys.exit()

        if len(sys.argv) == 2:
            symbol, fromdate, todate = sys.argv[1], None, None
        elif len(sys.argv) == 3:
            symbol, fromdate, todate = sys.argv[1:3], None
        else:
            symbol, fromdate, todate = sys.argv[1:4]
        
        s = Stock(symbol, fromdate, todate)
        for v in s.values:
            print v
