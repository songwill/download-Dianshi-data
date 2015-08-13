#Author:songwill
# -*- coding:utf-8 -*-

import urllib
import urllib2
import re
from bs4 import BeautifulSoup


import datetime
import calendar
def add_months(sourcedate,months):
     month = sourcedate.month - 1 + months
     year = int(sourcedate.year + month / 12 )
     month = month % 12 + 1
     day = min(sourcedate.day,calendar.monthrange(year,month)[1])
     return datetime.date(year,month,day)
    
#d1=datetime.date(2012,1,1)
urllist=[]    
for i in range(7):
    d1=datetime.date(2015,i%12+1,1)
    d2=add_months(d1,1)
    url='http://www.100ppi.com/monitor/get_ptable.php?pid=420&ds='+str(d1)+'&de='+str(d2) #通过Firfox查看反馈内容找到
    urllist.append(url)

#获取html文档
def gethtml(url):
    request=urllib2.Request(url)
    response=urllib2.urlopen(request)
    html=response.read()
    return html


#url='http://www.100ppi.com/monitor/detail-420-20140601-20140631.html'
#url='http://www.100ppi.com/monitor/get_ptable.php?pid=420&ds=2014-06-01&de=2014-06-31'
def getdayprice(url):
    html=gethtml(url)
    soup=BeautifulSoup(html)
    t=soup.find_all("tr")
    n=len(t)
    daylist=[]
    for i in range(2,n-1):
        #print t[i].text
        td=t[i].find_all("td")
        l=[]
        for s in td:
            l.append(s.text)
        #print pricelist
        print l[0]
        daylist.append(l)
    return daylist

pricelist=[]
for url in urllist:
    pricelist += getdayprice(url)

#print pricelist
import csv ,codecs     #不导入codecs输出的csv文件中文会显示乱码
csvfile = open('E:/mygit/dec-data/dianshi.csv', 'wb')
csvfile.write(codecs.BOM_UTF8)
writer = csv.writer(csvfile)
s1=['日期','白雁湖化工','英力特','兴平化工','榆电阳光','鄂尔多斯']
writer.writerow(s1)
#for item in pricelist:
#    writer.writerow(item)
writer.writerows(pricelist)
csvfile.close()


#注意：获取价格表单的反馈链接时，事在firfox中逐个查找找到的
#日期增加月份时，用了几种方法一直反馈错误，但没有注意 for i in range(12)中，i的第一个取值为0，月份没有0马上报错
#i%12为取余数
