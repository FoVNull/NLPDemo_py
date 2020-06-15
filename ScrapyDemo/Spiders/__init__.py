import ScrapyDemo.Spiders.BlogSpider
import os

if __name__ == '__main__':
    res = os.system("scrapy runspider BlogSpider.py")
    print(res)

