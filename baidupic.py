#coding=utf-8
'''
作者：herrylee
功能说明：爬取百度上指定关键词的图片，存放到本地路径下
运行环境：Python 3.6
运行环境：需要按照selenium：pip install selenium
命名规范：Pascal Camera命名规范
命名规范：函数与变量的命名要求全拼
需要使用者明确的参数：
    #图片存储路径
    imageSavePath='D:\\ImageDowload\\%s'
    #搜索关键词列表
    searchKeyWords = ['迈腾', '速腾']
    #chromerdriver.exe 文件存储路径
    locationDriverFullFilePath = '.\\chromedriver.exe'
    #每个关键词爬几页
    pageMoveCount=5
'''


from selenium import webdriver
import time
import urllib
from bs4 import BeautifulSoup as bs
import re
import os


#爬虫类
class BaiduImageCrawLer:
    base_url_part1 = 'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=index&fr=&hs=0&xthttps=111111&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word='
    base_url_part2 = '&oq=bagua&rsp=0'

    # 初始化函数
    def __init__(self,imageSavePath,searchKeyWords,locationDriverFullFilePath,pageMoveCount):
        self.imageSavePath=imageSavePath
        self.searchKeyWords=searchKeyWords
        self.locationDriverFullFilePath=locationDriverFullFilePath
        self.pageMoveCount=pageMoveCount

    # 模拟开启浏览器函数，返回驱动
    def startBrower(self,keyWord):
        driver = webdriver.Chrome(self.locationDriverFullFilePath)
        driver.maximize_window()
        driver.get(self.base_url_part1+keyWord+self.base_url_part2)
        print(self.base_url_part1+keyWord+self.base_url_part2)
        return driver

    # 下载图片函数，返回驱动
    def downloadImages(self, driver,keyWord):
        folderName=keyWord
        saveImagePath =self.imageSavePath %(folderName)
        if not os.path.exists(saveImagePath):
            os.makedirs(saveImagePath)
        imageUrlDictionary={}
        x=0
        pos=0
        for i in range(pageMoveCount):
            pos = pos+500
            js = "document.documentElement.scrollTop=%d"%pos
            driver.execute_script(js)    
            time.sleep(2) 
            htmlImage=driver.page_source   
            soup=bs(htmlImage,"html.parser")  
            imglist=soup.findAll('img',{'src':re.compile(r'https:.*\.(jpg|png)')})
            for imageUrl in imglist:    
                if imageUrl['src'] not in imageUrlDictionary:  
                    target = saveImagePath+'\\%s.jpg' % x    
                    imageUrlDictionary[imageUrl['src']] = ''   
                    urllib.request.urlretrieve(imageUrl['src'], target)    
                    x += 1

    #运行函数
    def run(self):
        for i in range(len(self.searchKeyWords)):
            browserDriver=self.startBrower(self.searchKeyWords[i])
            self.downloadImages(browserDriver,self.searchKeyWords[i])
            browserDriver.close()
        print("Dowload has finished.")

#主函数入口
if __name__=='__main__':
    imageSavePath='D:\\ImageDowload\\%s'
    searchKeyWords = ['迈腾', '速腾']
    locationDriverFullFilePath = 'D:\\MyDrivers\\chromedriver.exe'
    pageMoveCount=5
    craw =BaiduImageCrawLer(imageSavePath,searchKeyWords,locationDriverFullFilePath,pageMoveCount)
    craw.run()
