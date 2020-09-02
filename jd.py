# 爬取的代码
import requests
import re
import time

goods = '小米9'  # 搜索关键字
depth = 1  # 搜索深度为2，即爬取第1页，第2页
start_url = 'https://search.jd.com/Search?keyword=' + goods + '&enc=utf-8&wq=' + goods
infoList = []
hd = {'user-agent': 'Mozilla/5.0'}
for j in range(depth):  # 对每一个页面进行处理，使用for循环
    try:
        url = start_url + '&page=' + str(j)
        try:
            r = requests.get(url, headers=hd, timeout=30)
            r.raise_for_status()
            r.encoding = r.apparent_encoding  # 把获取到的页面信息 替换成utf-8信息，这样就不会乱码
            print(r.status_code)
            html = r.text
            print(r.url)
            print(r.text)
        except:
            print("抓取异常")
        try:
            plt = re.findall(r'<em>￥</em><i>.*?\.\d\d', html)  # 获取商品价格,搜索以<em>￥</em><i>开头，以.数字数字结尾的字符串
            tlt = re.findall(r'[^(<em>￥</em>)]<em>.*?[\u4e00-\u9fa5].*?</em>',
                             html)
            for i in range(len(plt)):
                price = plt[i].split('<i>')[1]
                title = tlt[i]
                infoList.append([price, title])
        except:
            print("分析异常")
    except:
        continue  # 如果某一个页面解析出了entity，那么继续解析下一个页面。
    time.sleep(2)

tplt = "{:^10}\t{:^10}\t{:^20}"
print(tplt.format("序号", "价格",
                  "商品名称"))
count = 0
for g in infoList:
    count = count + 1
    print(tplt.format(count, g[0], g[1]))  # 打印商品价格、名称，字符串没做处理
