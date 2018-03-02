#!/usr/bin/python
# encoding: utf-8

import sys,os,requests,arrow,json,urllib
from lxml import etree

class Object:
    pass

class Nasdaq100:

    def __init__(self):
        self.values = []
        self.__load__()

    def __load__(self):
        query = 'https://www.nasdaq.com/quotes/nasdaq-100-stocks.aspx'
        url = 'http://127.0.0.1:8888?url=%s' % urllib.quote(query)
        
        try:
            content = requests.get(url).content
            r = json.loads(content)
            
            if 'html' in r:
                html = etree.HTML(r['html'])
                rows = html.xpath("//div[@id='main-content-div']//tr[contains(@class,'flash100')]")
                for row in rows:
                    try:
                        cols = row.xpath("./td//text()")
                        if len(cols) == 9:
                            v = Object()
                            v.symbol = cols[0].strip()
                            v.name = cols[2].strip()
                            self.values.append(v)
                    except Exception, e:
                        print arrow.now(), e
        except Exception, e:
            print arrow.now(), e


if __name__ == '__main__':

        n = Nasdaq100()
        for v in n.values:
            print v.symbol+"\t"+v.name
