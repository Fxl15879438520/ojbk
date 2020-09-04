import requests  # 导入requests库，用于小规模爬取
import re  # 导入正则表达式


# 获取网页信息
def getHtmlText(url):
    try:
        header = {
            'authority': 's.taobao.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'referer': 'https://s.taobao.com/search?q=%E4%B9%A6%E5%8C%85&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': 'cna=v1iCFj5e5HUCAWp5DX0quDsv; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; tracknick=shaon1992; tg=0; miid=1632897152788742981; UM_distinctid=16f88fb7505647-021c8a4768c455-c383f64-1fa400-16f88fb7506a97; lgc=shaon1992; enc=bTD3YQaxUUPgMwDFOzNQb7gq%2FH5pgW5AsroLZZNZWAol%2F%2Bq%2FnesRJw6MtTZsB9Nr694mCB7jvjlmb3PQSo3OVA%3D%3D; mt=ci=23_1; t=f85195559e028f48ad19815224752b39; _m_h5_tk=f61d8dd502cb28f5d6db372130b5d45e_1584960506160; _m_h5_tk_enc=a36c7546e631f9f340b6dc44c895175f; tfstk=cC6GBWq-X1R_yzhqNf91DL3u9YeRZEM2rtWCLORQY8cl6tBFilcEa5iTxFbGHj1..; uc3=id2=UUGq1RsrN4lVRg%3D%3D&vt3=F8dBxd9gD5LRH%2BhN35Q%3D&nk2=EFY19v%2BIN9jj&lg2=U%2BGCWk%2F75gdr5Q%3D%3D; uc4=id4=0%40U2OdIeIjT8V0ugGcC5lw5EpiSlBQ&nk4=0%40Eo9LPCpw%2BKOBalOW5iTVFcrXPNw%3D; _cc_=UtASsssmfA%3D%3D; sgcookie=EHwF2Jp4HScWqZwBHzOfu; cookie2=157515f6c454549c82338d09b1970007; _tb_token_=76fe5a3ffb3e8; v=0; alitrackid=item.taobao.com; lastalitrackid=www.taobao.com; uc1=cookie14=UoTUP2D5qVEqyw%3D%3D; JSESSIONID=C3FB11DB6A138C4FEBEEB6CF68BA9B04; l=dBMg_kwlqqvYK87zKOCwdykmBh_OLIRfguyeoWKwi_5Q4_L1lU7OoyHxmEp6cjWAMIxH4cjscS2tZeJgJso4ne2e4AadZxDDB; isg=BBQUyTYnNrtGL6HwNFoBuS4w5VKGbThXLBPCq671_x8imbXjxXzw5_dbmZEBYXCv',
        }  # 隐去了cookie信息和referer信息
        r = requests.get(url, headers=header)  # 获得网页文本
        r.raise_for_status()  # 抛出错误
        r.encoding = r.apparent_encoding  # 编码

        return r.text  # 返回文本
    except:
        print("爬取失败")
        return ""  # 如果错误返回空字符串


# 获取商品信息
def parsePage(ilist, html):
    try:
        plt = re.findall(r'\"view_price\":\"\d+\.\d*\"', html)  # 正则匹配，返回值是列表形式
        tlt = re.findall(r'\"raw_title\":\".*?\"', html)
        # print(tlt)
        print(len(plt))
        for i in range(len(plt)):  # 遍历所有的列表中的项
            price = eval(plt[i].split('\"')[3])  # 去掉双引号，以：分割字符串
            title = tlt[i].split('\"')[3]
            ilist.append([title, price])  # 把商品信息添加到ilt中
        # print(ilist)
    except:
        print("解析出错")


# 打印信息
def printGoodsList(ilist, num):
    print("=====================================================================================================")
    tplt = "{0:<3}\t{1:<30}\t{2:>6}"  # 规定一定的format格式
    print(tplt.format("序号", "商品名称", "价格"))  # 表头
    count = 0
    for g in ilist:
        count += 1
        if count <= num:
            print(tplt.format(count, g[0], g[1]))
    print("=====================================================================================================")



# 主函数
def main():
    goods = input("请输入商品名: ")
    depth = 2  # 爬取深度
    start_url = "https://s.taobao.com/search?q=" + goods  # 第一页
    infoList = []
    num = 20
    for i in range(depth):
        try:
            url = start_url + '$S=' + str(44 * i)  # 翻页
            html = getHtmlText(url)
            parsePage(infoList, html)
        except:
            continue

    printGoodsList(infoList, num)


main()
