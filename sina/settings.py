# -*- coding: utf-8 -*-

BOT_NAME = 'sina'

SPIDER_MODULES = ['sina.spiders']
NEWSPIDER_MODULE = 'sina.spiders'

ROBOTSTXT_OBEY = False

# 请将Cookie替换成你自己的Cookie
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Cookie':"_T_WM=58006532587; ALF=1585301661; SCF=AjabaJ3W4osx7tpQ4xq_rAVYErRASfHxEnVdDoUfV3IcqxewXA9HlH5ldaSKFHiqr0Fps6IQdCRd5MPTDLVHxlU.; SUB=_2A25zUkxjDeRhGeBL61cY9yfEyTyIHXVQvVQrrDV6PUJbktANLVfukW1NR0y2uFT55l8UjjMDkwrmEjtysP8_mpk1; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhAldxrE9pWK80Q1QBzH_TD5JpX5K-hUgL.Foqfeh-4S0.Reo52dJLoI7_bUg8ydsLAIgfDdntt; SUHB=0auASus_sq3Hbl; SSOLoginState=1582709811"
}

# 当前是单账号，所以下面的 CONCURRENT_REQUESTS 和 DOWNLOAD_DELAY 请不要修改

CONCURRENT_REQUESTS = 16

DOWNLOAD_DELAY = 3

DOWNLOADER_MIDDLEWARES = {
    'weibo.middlewares.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None
}

ITEM_PIPELINES = {
    'sina.pipelines.MongoDBPipeline': 300,
}

# MongoDb 配置

LOCAL_MONGO_HOST = '127.0.0.1'
LOCAL_MONGO_PORT = 27017
DB_NAME = 'Sina'
