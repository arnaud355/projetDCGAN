# -*- coding: utf-8 -*-
"""
Created on Wed May 20 10:25:15 2020

@author: arnaud.baleh
"""

import scrapy
from scrapy.spiders import Spider
from ..items import SampleItem
#from PIL import Image
#import PIL 
import re
import csv

#http://www.pinterest.fr

class ImgSpider(Spider):
    name = "img_spider"
    
    def start_requests(self):
        urls = ['https://www.pinterest.fr/search/pins/?q=reine%20des%20neiges&rs=rs&eq=&etslf=1766&term_meta[]=reine%7Crecentsearch%7C0&term_meta[]=des%7Crecentsearch%7C0&term_meta[]=neiges%7Crecentsearch%7C0',]
     
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
    def parse(self,response):
        
        item = SampleItem()
        img_urls = []
        txt_urls = []
        ele_to_add = [["index"]]
                  
        txt_urls = response.css('*').xpath('@src').getall()
        txt_string = " "
        txt_string = ' '.join([str(elem) for elem in txt_urls])
        
        images_urls = re.findall('(https?://\S*[jpg|jpg|png])', txt_string)
    
        for ele in images_urls:
            ele_to_add.append([(ele)])
            
        with open('cartoonTest.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(ele_to_add)
        
        
        item["images_urls"] = img_urls
        
        for img in img_urls:
            img.save('/arnaud.baleh/Desktop/dataIA/scrapyTuto/imagesProjet','JPG')
        return item
    
'''  
    def parse(self,response):
        item = SampleItem()
        img_urls = []
        for img in response.css('#thumbs_list_frame > li'):
            img_urls.append(img.css('a::attr(href)')).get()
        item["img_urls"] = img_urls
        return item
'''