# -*- coding: utf-8 -*-
import scrapy
import re,os,json
from wybk.items import WyItem

class WybkSpider(scrapy.Spider):
    name = 'wy'
    allowed_domains = ['blog.163.com']
    start_urls = ['http://blog.163.com/blogger.html']

    # 获取每个名博的前缀
    def parse(self, response):
        # print response.body
        qz_list = response.xpath('//ol/li/a/@href').extract()
        mz_list = response.xpath('//ol/li/a/text()').extract()
        # print qz_list
        qianzhui_list = []
        #找到每个前缀,并加入到列表
        for x in qz_list:
            res = re.compile(r'http\:\/\/(.*)\.blog')
            qianzhui = res.findall(x)
            #判断有的是否为空
            if qianzhui:
                # print qianzhui[0]
                qianzhui_list.append(qianzhui[0])

            else:
                pass
        #测试出三个人物
        for y in qianzhui_list[:3]:

            base_url = 'http://%s.blog.163.com/?fromBlogger'
            print y
            url = base_url % y
            print url

            yield scrapy.Request(url=url,callback=self.wzh_parse,meta={'meta':y})


    #爬取页面文章号,找到数据接口
    def wzh_parse(self,response):
        meta1 = response.meta['meta']

        # print meta1,type(meta1)
        print response.body

        html = response.xpath('//a[@class="m2a fc03 fs1 ztag"]/@href').extract()
        print html,2
        res1 = re.compile(r'static/(\d{9})')
        wzh1 = res1.findall(html[0])
        wzh = wzh1[0]

        # base_url = 'http://api.blog.163.com/%s/dwr/call/plaincall/BlogBeanNew.getComments.dwr'
        base_url = 'http://api.blog.163.com/%s/dwr/call/plaincall/BlogBeanNew.getBlogs.dwr'
        start_url = base_url % meta1

        header = {
            "Host":"api.blog.163.com",
            "Connection":"keep-alive",
            # "Content-Length":"187",
            "Origin":"http://api.blog.163.com",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
            "Content-Type":"text/plain",
            "Accept":"*/*",
            "Referer":"http://api.blog.163.com/crossdomain.html?t=20100205",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.8",
        }

        yield scrapy.FormRequest(
                url=start_url,
                callback=self.content_parse,
                headers=header,
                formdata={
                            "callCount":"1",
                            "scriptSessionId":"${scriptSessionId}187",
                            "c0-scriptName":"BlogBeanNew",
                            "c0-methodName":"getBlogs",
                            "c0-id":"0",
                            "c0-param0":wzh,
                            "c0-param1":"number:0",
                            "c0-param2":"number:20",
                            "batchId":'1'},
                meta={'meta':meta1})

    #进入数据接口找到所有文章的编号
    def content_parse(self,response):
        # print response.body,
        meta1 = response.meta['meta']
        # name = response.meta['name']
        # 获取该人物的所有文章编号
        res = re.compile('permaSerial=\"(\d+)')
        wzbh = res.findall(response.body)
        # print wzbh
        # print ('*')*100
        for x in wzbh:

            # base_url = 'http://%s.blog.163.com/blog/static/%d/'
            start_url = 'http://'+meta1+'.blog.163.com/blog/static/'+x+'/'
            yield scrapy.Request(url=start_url,callback=self.wz_parse)


    def wz_parse(self,response):
        # name = response.meta['name']
        # print response.body.decode('gbk')
        data = response.xpath('//div[@class="bct fc05 fc11 nbw-blog ztag"]')
        content = data.xpath('string(.)').extract()[0]
        title = response.xpath('//h3[@class="title pre fs1"]/span[@class="tcnt"]/text()')[0].extract()

        item = WyItem()
        item['title'] = ''.join(title)
        item['content'] = ''.join(content)
        yield item

