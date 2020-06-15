import scrapy

from ScrapyDemo.ResultItem import ResultItem


class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = [
        'http://hikki.top/'
    ]
    """
    start_urls 包含了Spider在启动时进行爬取的url列表。
    因此，第一个被获取到的页面将是其中之一。
    后续的URL则从初始的URL获取到的数据中提取。
    """

    """
     parse被调用时，每个初始URL完成下载后生成的Response对象将会作为唯一的参数传递给该函数。
     该方法负责解析返回的数据(response data)，
     提取数据(生成item)以及生成需要进一步处理的URL的 Request 对象。
     parse必须覆写
    """
    def parse(self, response):
        for title in response.css('.post_content>a'):
            # x>y  选择所有父级是 x 的元素的 y 元素
            """
            *全选 对象::text获得标签内的内容
            返回的是selector，用一些方法取值↓

            get() <=> extract_first()
            返回的是string，list里面第一个string

            getall() <=> extract()
            返回的是一个list，里面包含了多个string，如果只有一个string，则返回['string']这样的形式
            """
            yield {'title': title.css('*::text').get()}

        # for next_page in response.css('a.next-posts-link'):
        #     yield response.follow(next_page, self.parse)

