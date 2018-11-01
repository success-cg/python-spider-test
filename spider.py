from urllib import request  # 获取 html 文本用 urllib 模块
import re

'''
Python 2.7.9 之后引入了一个新特性
当你urllib.urlopen一个 https 的时候会验证一次 SSL 证书 
当目标使用的是自签名的证书时就会爆出一个 
urllib2.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:581)> 的错误消息
下面2行代码用来【禁掉这个证书的要求】，可以解决这个报错
'''

import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class Spider():
    url = 'https://www.panda.tv/cate/lol'

    # 匹配的正则表达式，要注意【贪婪、非贪婪】，用 group 获取标签内部的内容
    root_pattern = '<div class="video-info">(.*?)</div>'
    name_pattern = '</i>(.*?)</span>'
    number_pattern = '<span class="video-number">(.*?)</span>'

    # 抓取htmls数据
    def __fetch_content(self):
        r = request.urlopen(self.__class__.url)  # 发起 request，获取 response
        htmls = r.read()  # 调用 read 方法获取html文本, htmls 这时候是 bytes（字节码）
        return str(htmls, encoding='utf-8')  # 转化成 utf-8 格式的字符串

    # 正则匹配需要内容，组织成 dict 数据格式
    def __analyse(self, htmls):
        # 正则匹配htmls的文本内容，re.S 模式 .（点）能匹配 \n
        root_html = re.findall(self.__class__.root_pattern, htmls, re.S)
        anchors = []
        for html in root_html:
            name = re.findall(self.__class__.name_pattern, html, re.S)[0]
            number = re.findall(self.__class__.number_pattern, html, re.S)[0]
            anchor = {'name': name, 'number': number}
            anchors.append(anchor)
        return anchors

    # 精炼数据，去除空格等
    def __refine(self, anchors):
        lam = lambda anch: {
            'name': anch['name'].strip(),
            'number': anch['number'].strip()
        }
        refined_anchors = list(map(lam, anchors))
        return refined_anchors

    def __sort(self, anchors):
        anchors = sorted(anchors, key=self.__sort_seed, reverse=True)
        pass
        return anchors

    def __sort_seed(self, anchor):
        number = re.findall('\d*\.*\d*', anchor['number'])[0]
        number = float(number)
        if '万' in anchor['number']:
            number *= 10000
        return number

    def __show(self, anchors):
        for i in range(0, len(anchors), 1):
            # print(anchor['name'] + '\t\t\t\t\t\t' + anchor['number'])
            print(
                'rank: ' + str(i+1) + '\t\t\t'
                + anchors[i]['name']
                + '\t\t\t' + anchors[i]['number']
            )

    # 对外暴露的实例方法，爬虫的执行入口
    def go(self):
        htmls = self.__fetch_content()  # 抓取 htmls 数据
        anchors = self.__analyse(htmls)  # 正则匹配需要内容，组织成 dict 数据格式
        anchors = self.__refine(anchors)  # 精炼数据，去除空格等
        anchors = self.__sort(anchors)
        self.__show(anchors)
        return anchors


spider = Spider()  # 实例化爬虫
anchors = spider.go()  # 爬取数据
pass
