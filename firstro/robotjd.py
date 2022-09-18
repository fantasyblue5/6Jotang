import scrapy
import json
from ..items import FirstroItem
from loguru import logger


# 基本设置
class RobotjdSpider(scrapy.Spider):
    comments = 0
    name = 'robotjd'
    allowed_domains = ['www.jd.com', 'club.jd.com', 'club.jd.com.comment']

   # 这里将url拆成三段，是为了添加page后数字变量，实现多页面爬取
    url_head ='https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=100019125569&score=0&sortType=5'
    url_middle ='&page='
    url_end ='&pageSize=10&isShadowSku=0&fold=1'
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'shshshfp=eebbb2bba5ed808f2cf74ac04a1df067; shshshfpa=1b93245b-9987-86b0-8235-1fbfa6607b11-1661658873; shshshfpb=ddIlFZEKSz4TPbxdUZhX8vA; areaId=52993; __jdu=265529881; ipLoc-djd=52993-52994-53014-54727; unpl=JF8EAJBnNSttCkxWA08FHRJCQlhSW1oOTkQHbGVSAFsLQgABSQBOExR7XlVdXhRKHx9vZBRUXFNIUg4YCysSEXteVV5UD00QC2tkNWRaWEIZRElPKxEQe11Vbl4PTxMAZ24MVG1oTFQMKzIrFxBKXFNWWQFLEzNuVwdVXF1DVA0ZBxwiWyVcGV1aDE8UC2ZuBWRcaEg; CCC_SE=ADC_rsq9qW44goHc%2fMXZdC3FhPNDBzNPSZDBSvQksh1M%2bwf6EtRHamxogBaYlwBBcEMuBCwnH0z%2fzvNSbsv2gEr%2fRel5bcba5zQKAFaaleK4NtTwuc0vr%2be1oXlC%2bagxqJ%2fHBaeI3aGurMiA8CKXSzWCb1bMY3OtKPlI%2bQiQBYH9cSRxK26qrynCJlHKkA2hZLwVaBiG31xWPQQrNrQ61TLujPLTYxJkJoLue9CMBdoFE67GPcHrcBWMLMbPrPWtzJHMaPVRvQWQzIjIgClN4Nev%2fxR2Vu1OVGtNqWdKzA4xPtgDnlpgQkl1c52N6pKCWWTwf5rDSNV4xN3ObY6ULaPiC3xcBQbIL9D9P5PmYg53b6LWpN0aQoAAT8Kg79r0HlbHpI%2bGILPpuCR8N1oXhtummh8RfU6awNWe1wsbyKdbICyeuVS3xPAwF8UnE4zp%2bXe1x2AsIr9LM1Iom1pUSRvPpQ%3d%3d; __jdv=122270672|wjhsh.net|t_2018676952_|tuiguang|c637e671c8474674b523fe7b8e5c3d05|1662949649076; __jdc=122270672; jsavif=1; __jda=122270672.265529881.1661658870.1662949649.1663469141.3; ip_cityCode=2951; token=2e4d842f705a93d9059a05f66566ab63,2,924149; __tk=ArtujYfrkujE4zkpjVbqjz4wkUAqAzptjzayBVptAUn,2,924149; shshshsID=1bd45ad48f205f7987a6be227dfb460c_2_1663469167176; __jdb=122270672.2.265529881|3.1663469141; 3AB9D23F7A4B3C9B=5G27U7QJ7CB73IPSNX7PUDRHXRURIWUBYN6F2DXX2TTUUSYVKFGL4ELIWRQ532DUSHZNAM4ALBN5PPAVCRZFCZ7ND4',
        'referer': 'https://item.jd.com/',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'script',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    }


    # 请求访问
    def start_requests(self):
        # logger.info()
        for i in range(0,70):
            logger.info("当前爬取到第{}页".format(i))
            url = self.url_head + self.url_middle + str(i) + self.url_end
            yield scrapy.Request(url=url, callback=self.parse)


    # 数据解析
    def parse(self, response):
        json_str = response.text
        logger.info(json_str)
        logger.info(json_str)
        # 这里是为了让网页里的文件能被解析，前面有20个无意义字符和{}
        data = json.loads(json_str[20:-2])


        # 封装数据
        comment_list = data['comments']
        for com in comment_list:
                self.comments += 1
                user = com['nickname']
                content = com['content']
                times = com['creationTime']

                item = FirstroItem()
                item['user'] = user
                item['content'] = content
                item['times'] = times
                logger.info("当前第{}条数据".format(self.comments))

                yield item














