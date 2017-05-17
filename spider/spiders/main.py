# -*- coding: utf-8 -*-
import datetime
from collections import OrderedDict

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from spider.items import MovieItem


class MySpider(CrawlSpider):
    name = "monkey"
    allowed_domains = ["btbtdy.com"]
    start_urls = [
        "http://www.btbtdy.com/screen/0-----time-1.html"
    ]

    # href="0-----time-2.html"
    rules = (
        Rule(LinkExtractor(allow=r'/0-----time-\d+\.html'), callback="parse_page", follow=True),
        Rule(LinkExtractor(allow=r'/btdy/dy\d+\.html'), callback='parse_movie', follow=True),
    )

    def parse_page(self, response):
        self.log("parsing page %s:" % response.url)

    def parse_movie(self, response):
        root_selector = response.xpath("//div[contains(@class,'vod_intro')]")
        # 标题
        title = root_selector.xpath("h1/text()").extract()[0]
        # 上映时间
        time = root_selector.xpath("h1/span/text()").extract()[0].strip()[1:][:-1]
        # 更新时间
        update_time_str = root_selector.xpath("dl/dd[1]/text()").extract()[0]
        update_time = datetime.datetime.strptime(update_time_str, "%Y-%m-%d %H:%M")
        # 简介
        introduce = response.xpath("//div[@class='c05']/p | /div").xpath("text()").extract()
        # 封面连接
        image_url = response.xpath("//div[contains(@class, 'vod_img')]/img/@src").extract()[0]
        # 评分 (js生成的页面,暂时无法抓取)
        # star = response.xpath("//span[@id='filmStarScore']/text()").extract()[0]
        # 类型
        types = root_selector.xpath("dl/dd[3]/a/text()").extract()
        # 国家
        countries = root_selector.xpath("dl/dd[4]/a/text()").extract()
        # 演员
        actors = root_selector.xpath("dl/dd[7]/a/text()").extract()
        # 语言
        languages = root_selector.xpath("dl/dd[5]/a/text()").extract()
        # 种子
        links = []
        download_titles = response.xpath("//div[@class='p_list']/h2/text()").extract()
        for index, download_title in enumerate(download_titles):
            select_titles = response.xpath("//div[@class='p_list'][%d]/ul/li/a/text()" % (index + 1)).extract()
            select_magnets = response.xpath("//div[@class='p_list'][%d]/ul/li/span/a/@href" % (index + 1)).extract()
            magnet_dict = OrderedDict()

            magnet_dict["label"] = download_title
            torrent_list = []
            if len(select_titles) == len(select_magnets):
                for i, select_title in enumerate(select_titles):
                    torrent_dict = OrderedDict()
                    torrent_dict["title"] = select_title
                    torrent_dict["value"] = select_magnets[i]
                    torrent_list.append(torrent_dict)
            magnet_dict["torrents"] = torrent_list
            links.append(magnet_dict)

        # 爬虫地址
        crawl_url = response.url
        return MovieItem(title=title, time=time, update_time=update_time, introduce=introduce,
                         types=types, image_url=image_url, countries=countries,
                         actors=actors, languages=languages, links=links, crawl_url=crawl_url)
