# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

"""
{'image_urls': ['http://books.toscrape.com/media/cache/ba/a6/baa64eeda5e10952da4610f8efc1be76.jpg'],
 'images': [{'checksum': '4f33d9c0d49c915983a46a97814bfac6',
             'path': 'full/3fa711805177ba5b0a1e0c02d94e28f094a6adcc.jpg',
             'url': 'http://books.toscrape.com/media/cache/ba/a6/baa64eeda5e10952da4610f8efc1be76.jpg'}],
 'price': ['£39.24'],
 'rating': ['Three'],
 'title': ['<h1>Fighting Fate (Fighting #6)</h1>']}
"""

import os

class BooksCrawlerScrapyPipeline:

    def __init__(self):
        self.ndir = '/home/zinonas/Documents/Scrapy/books_crawler_scrapy_pipelines/images'
        self.ndir_full = self.ndir + '/full'

    def process_item(self, item, spider):
        os.chdir(self.ndir)
        #check existence of url before renaming
        #access images key, access first element of list, access path key
        image_name = item['images'][0]['path']
        if image_name:
            new_image_name = item['title'][0].replace("'", "") +'.jpg'  #pick first element of list
            new_image_full_name = self.ndir_full + '/' + new_image_name

            os.rename(image_name, new_image_full_name)
            print('New image name', image_name)
        else:
            print('Image name not found!')

