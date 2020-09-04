import requests
import re
import time
import csv
from bs4 import BeautifulSoup

goods = input("请输入商品名: ")  # 搜索关键字
depth = 1  # 搜索深度为2，即爬取第1页，第2页
start_url = 'https://youhui.pinduoduo.com/search/landing?keyword=' + goods
infoList = []
hd = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36'}
for j in range(depth):  # 对每一个页面进行处理，使用for循环
    try:
        url = start_url
        try:
            r = requests.get(url, headers=hd, timeout=30)
            r.raise_for_status()
            r.encoding = r.apparent_encoding  # 把获取到的页面信息 替换成utf-8信息，这样就不会乱码
            print(r.status_code)
            html = r.text
            print(r.url)
            #print(r.text)
        except:
            print("抓取异常")
        try:
            plt = re.findall(r'<span>￥<!-- -->.*?\.\d\d</span></p>', html)  # 获取商品价格
            tlt = re.findall(r'"goodsName":"[^\x00-\xff]+', html)   #商品名
            jlt =  re.findall(r'ImageUrl":"https://.+?.jpeg', html)   #商品图片地址
            wlt = re.findall(r'goodsId=[1-9]\d*', html)   #商品链接
            for i in range(len(plt)):
                price = plt[i].split('-->')[1].split('</span>')[0]
                title = tlt[i].split(':"')[1]
                img = jlt[i].split(':"')[1]
                spid = wlt[i].split('=')[1]
                infoList.append([price, title, img, spid])
        except:
            print("分析异常")
    except:
        continue  # 如果某一个页面解析出了entity，那么继续解析下一个页面。
    time.sleep(2)

tplt = "{:^10}\t{:^10}\t{:^40}\t{:^60}\t{:^60}"
print(start_url)
print(tplt.format("序号", "价格","商品名称","商品图片","商品链接"))
count = 0
for g in infoList:
    count = count + 1
    print(tplt.format(count, g[0], g[1], g[2], 'https://youhui.pinduoduo.com/goods/goods-detail?goodsId='+g[3]))  # 打印商品信息
with open("pdd.txt","w") as f:                                                   #设置文件对象
    for i in infoList:                                                                 #对于双层列表中的数据
        i = str(i).strip('[').strip(']').replace(',','').replace('\'','')+'\n'  #将其中每一个列表规范化成字符串
        f.write(i)