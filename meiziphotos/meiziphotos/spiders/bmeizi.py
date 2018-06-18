# -*- coding: utf-8 -*-
import scrapy
import re

class BmeiziSpider(scrapy.Spider):
    name = 'bmeizi'
    allowed_domains = ['www.mzitu.com']
    start_urls = ['http://www.mzitu.com/']
    def parse(self, response):
        newUrls = response.xpath("//ul[@id='pins']/li/a/@href").extract()


        for urls in newUrls:
                yield response.follow(urls,callback = self.newPage)
                break
        # if len(response.xpath("//a[@class='next page-numbers']/@href")) != 0:
        # print(response.xpath("//a[@class='next page-numbers']/@href"))
        yield response.follow(response.xpath("//a[@class='next page-numbers']/@href").extract_first(), callback = self.parse)
        print(response.xpath("//a[@class='next page-numbers']/@href"))



    def newPage(self,response):
        # a = int(response.xpath("//div[@class='pagenavi']/a[last()-1]/span/text()").extract_first())
        for i in range(int(response.xpath("//div[@class='pagenavi']/a[last()-1]/span/text()").extract_first())):
            try:
                # print(i+1)
                yield response.follow(response.url + "/" + str(i+1), callback=self.runSave, dont_filter=True)

        # if self.number > a:
        #     self.number = 1
        # else:
        #得改 response.url
                # yield {
                #     'titleName' : response.xpath("//h2[@class='main-title']/text()").extract_first(),
                #     'imageLink' : response.xpath("//div[@class='main-image']/p/a/img/@src").extract_first(),
                #       }
                # self.number = self.number + 1
                # yield response.follow(response.url + "/" + str(i+1),callback = self.newPage)
            except:
                pass

    def runSave(self,response):
        yield {
            'fileName': response.xpath("//div[@class='currentpath']/text()[3]").extract_first().strip(' » '),
            'titleName': response.xpath("//h2[@class='main-title']/text()").extract_first(),
            'imageLink': response.xpath("//div[@class='main-image']/p/a/img/@src").extract_first(),
        }


# www.mzitu.com/137677

#首页点击链接 //ul[@id='pins']/li/a/@href
#首页标题 //ul[@id='pins']/li/a/img/@alt
#首页标题图片 //ul[@id='pins']/li/a/img/@src
#首页下一页链接 //a[@class='next page-numbers']/@href
#没有下一页是上诉链接不存在匹配

#详情页图片链接 //div[@class='main-image']/p/a/img/@src

#详情页图片数量为 //div[@class="pagenavi"]/a[last()-1]/span
#详情页每张图片标题 //h2[@class="main-title"]
#详细页获取总标题  //div[@class='currentpath']      //div[@class='currentpath']/text()[3]

#response.xpath("//div[@class='currentpath']/text()[3]").extract_first().strip(' » ')
#<a class="next page-numbers" href="http://www.mzitu.com/page/2/">下一页»</a>


# string_test = "This is test string 这是测试字符串"
# string_test = string_test.decode('utf-8')  # 转码
#
# pattern = ur'[\u4e00-\u9fff]+'  # 汉字正则表达式
# re_compile = re.compile(pattern)
#
# res = re_compile.findall(string_test)
# print res

#勾人小妖精LULU小璐璐: 你看到我饥渴的眼神了吗?