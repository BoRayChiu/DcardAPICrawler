'''
$pip install selenium
$pip install webdriver-manger
firefox must be ".deb" not "snap"

'''
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
import json


class Browser:

    def __init__(self):
        '''
        # Proxy via privoxy through tor
        self.PROXY = "127.0.0.1:8118"
        webdriver.DesiredCapabilities.FIREFOX["proxy"] = {
        "httpProxy": self.PROXY,
        "proxyType": "MANUAL"
        }
        '''
        self.opts = Options() 
        self.opts.add_argument('--headless')
        self.opts.add_argument('--disable-gpu')
        self.service = Service(GeckoDriverManager().install())
        self.browser = webdriver.Firefox(service=self.service, options=self.opts)

    def get_browser(self):
        return self.browser


class DcardSeleniumCrawler:
    
    def __init__(self, browser):
        self.browser = browser
        self.url = "http://checkip.amazonaws.com/"
        self.result = []

    def crawl(self):
        # browse the url and get json result
        self.browser.get(self.url)
        time.sleep(5)
        self.browser.find_element(By.CSS_SELECTOR, "#rawdata-tab").click()
        res = self.browser.find_element(By.CSS_SELECTOR, "#rawdata-panel pre.data").text
        self.result = json.loads(res)

    def check_ip(self):
        self.browser.get("http://checkip.amazonaws.com/")
        ip = self.browser.find_element(By.TAG_NAME, "pre").text
        print("Ip now: " + ip)


class DcardTopicsIdCrawler(DcardSeleniumCrawler):
    
    def __init__(self, browser, board:str, frequency:str):
        super().__init__(browser)
        self.url = "https://www.dcard.tw/service/api/v2/forums/" + board + "/posts?limit=" + frequency
        self.topic_ids = []

    def main(self):
        self.crawl()
        for i in range(len(self.result)):
            self.topic_ids.append(self.result[i].get("id"))

    def get_topic_ids(self):
        return topic_ids


class DcardPostCrawler(DcardSeleniumCrawler):

    def __init__(self, browser, topic_id:str):
        super().__init__(browser)
        self.url = "https://www.dcard.tw/service/api/v2/" + "posts/" + topic_id
        self.meta = {}
        self.contents = ""

    def main(self):
        self.crawl()
        school = self.result.get("school")
        department = self.result.get("department")
        # if have "CardName"
        if(self.result.get("withNickname") == True):
            self.meta["Author"] = school
            self.meta["Author ID"] = department
        else:
            self.meta["School"] = school
            self.meta["Department"] = department
        # title
        self.meta["Title"] = self.result.get("title")
        # created time
        self.meta["Time"] = self.result.get("createdAt")
        # contents
        self.contents= self.result.get("content").replace("\n", " ")

    def get_meta(self):
        return self.meta

    def get_contents(self):
        return self.contents


class DcardCommentsCrawler(DcardSeleniumCrawler):
    
    def __init__(self, browser, topic_id:str):
        super().__init__(browser)
        self.url = "https://www.dcard.tw/service/api/v2/" + "posts/" + topic_id + "/comments"
        self.comments_list = []

    def main(self):
        self.crawl()
        for i in range(len(self.result)):
            comment = {}
            id = self.result[i].get("id")
            comment["id"] = id
            content = self.result[i].get("content")
            if content == None:
                continue
            school = self.result[i].get("school")
            department = self.result[i].get("department")
            # if have "CardName"
            if(self.result[i]["withNickname"] == True):
                comment["Author"] = school
                comment["Author ID"] = department
            else:
                comment["School"] = school
                comment["Department"] = department
            comment["Content"] = content.replace("\n", " ")
            comment["SubComments"] = []
            # determine if have sub comments
            if self.result[i].get("subCommentCount") > 0:
                comment["has SubComments"] = True
            else: 
                comment["has SubComments"] = False
            self.comments_list.append(comment)

    def get_comments_list(self):
        return comments_list


class DcardSubCommentsCrawler(DcardSeleniumCrawler):
    
    def __init__(self, browser, topic_id:str, parent_comment_id:str):
        super().__init__(browser)
        self.url = "https://www.dcard.tw/service/api/v2/" + "posts/" + topic_id + "/comments" + "?parentId=" + parent_comment_id
        self.parent_comment_id = parent_comment_id
        self.sub_comments_list = []

    def main(self):
        self.crawl()
        for i in range(len(self.result)):
            sub_comment = {}
            sub_comment["Parent Comment ID"] = self.parent_comment_id
            content = self.result[i].get("content")
            if content == None:
                continue
            school = self.result[i].get("school")
            department = self.result[i].get("department")
            # if have "CardName"
            if(self.result[i]["withNickname"] == True):
                sub_comment["Author"] = school
                sub_comment["Author ID"] = department
            else:
                sub_comment["School"] = school
                sub_comment["Department"] = department
            sub_comment["Content"] = content.replace("\n", " ")
        self.sub_comments_list.append(sub_comment)

    def get_sub_comments_list(self):
        return self.sub_comments_list


if __name__ == "__main__":
    b = Browser()
    tic = DcardSubCommentCrawler(b.browser, "241413053", "6f49247a-4bfb-4d21-974b-e4b2197535e8")
    #tic.check_ip()
    tic.main()
    for t in tic.sub_comment_list:
        print(t)