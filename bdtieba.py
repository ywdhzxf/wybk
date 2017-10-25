#coding:utf8

import urllib2,urllib
import re
import random
import os
# 搜索哪个贴吧
def tieba(wz):
    base_url = 'http://tieba.baidu.com/f?'
    #贴吧名字
    tbmz = {
        'kw':wz,
    }
    tbmz = urllib.urlencode(tbmz)
    tb_url = base_url + tbmz
    print tb_url

    #根据贴吧名字建立一个文件夹
    path = './' + wz
    if not os.path.exists(path.decode('utf8')):
        os.makedirs(path.decode('utf8'))
    return tb_url

#查询当前页的内容
def search(key,base_url):
    base_url = base_url

    xq = {
        'pn':key,
    }
    xq = urllib.urlencode(xq) #进行编码
    fullurl = base_url + xq
    print fullurl
    # request = urllib2.Request(fullurl)  #构建对象
    # response = urllib2.urlopen(request)
    # print response.read()
    base_url = fullurl
    print base_url
    response = urllib2.urlopen(base_url)
    html = response.read()

    # 正则帖子的网址数
    tezi_pattern = re.compile(r'/p/[0-9]{10}')
    tezi_url = tezi_pattern.findall(html)
    # print tezi_url #获取到每个帖子的路径

    for item in tezi_url:
        mvtz_url = 'https://tieba.baidu.com'
        mv_url = mvtz_url + item  #获取到美女贴吧每个帖子的全部网址
        # print mv_url

        response = urllib2.urlopen(mv_url)
        html = response.read()

        img_pattern = re.compile(r'class="BDE_Image".*?src="(.*?)"')
        img_urls = img_pattern.findall(html) #需要下载的图片地址

        for img_url in img_urls:
            fname = img_url.split('/')[-1] #图片名字
            fullname = os.path.join('./',context.decode('utf8'),fname.decode('utf8'))

            print 'downloading...'  +  fname
            urllib.urlretrieve(img_url,fullname)


if __name__ == '__main__':
    context = raw_input('请输入要查询的贴吧: ')
    base_url = tieba(context)

    ys = raw_input('请输入要查询的页数:')
    ys1 = ys.split(',')
    print ys1
    x1 = int(ys1[0])
    x2 = int(ys1[1])
    if x2 >= x1:
        while x1 <= x2:
            key = (x1-1)*50
            result = search(key,base_url)
            print ('当前页数'+str(x1))
            x1 += 1
    else:
        while x2 <= x1:
            key = (x2-1)*50
            result = search(key)
            print('当前页数'+str(x2))
            x2 += 1
