# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import scrapy
import os
import re

from scrapy.utils.project import get_project_settings


class MeiziphotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):

        image_link = item["imageLink"]
        yield scrapy.Request(image_link,headers= {'Referer':item["imageLink"]})
        # return item

    def item_completed(self, results, item, info):
        image_path = [x["path"] for ok, x in results if ok]

        fileName = item["fileName"]
        titleName = item["titleName"]

        pattern = r'\u4e00-\u9fa5]|\w'
        re_compile = re.compile(pattern)

        newFileName = re_compile.findall(fileName)
        newTitleName = re_compile.findall(titleName)

        lastFileName = ""
        lastTitleName = ""

        for i in range(len(newFileName)):
            lastFileName = lastFileName.__add__(newFileName[i])
        for i in range(len(newTitleName)):
            lastTitleName = lastTitleName.__add__(newTitleName[i])

        os.renames(get_project_settings().get('IMAGES_STORE') + image_path[0], get_project_settings().get('IMAGES_STORE') + lastFileName + "/" + lastTitleName + ".jpg")
        return item
