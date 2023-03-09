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
        self.__opts = Options() 
        #self.__opts.add_argument('--headless')
        self.__opts.add_argument('--disable-gpu')
        self.__service = Service(GeckoDriverManager().install())
        self.__browser = webdriver.Firefox(service=self.__service, options=self.__opts)

    @property
    def get(self):
        return self.__browser
    


class DcardSeleniumCrawler:
    
    def __init__(self, browser):
        self._browser = browser
        self._url = "http://checkip.amazonaws.com/"
        self._result = []

    def _crawl(self):
        # browse the url and get json result
        self._browser.get(self._url)
        time.sleep(5)
        self._browser.find_element(By.CSS_SELECTOR, "#rawdata-tab").click()
        res = self._browser.find_element(By.CSS_SELECTOR, "#rawdata-panel pre.data").text
        self._result = json.loads(res)

    def check_ip(self):
        self._browser.get("http://checkip.amazonaws.com/")
        ip = self._browser.find_element(By.TAG_NAME, "pre").text
        print("Ip now: " + ip)


class DcardTopicsIdCrawler(DcardSeleniumCrawler):
    
    def __init__(self, browser, board:str, frequency:str):
        super().__init__(browser)
        self._url = "https://www.dcard.tw/service/api/v2/forums/" + board + "/posts?limit=" + frequency
        self.__topic_ids = []

    def __main(self):
        self._crawl()
        for i in range(len(self._result)):
            self.__topic_ids.append(self._result[i].get("id"))

    @property
    def result(self):
        self.__main()
        return self.__topic_ids


class DcardPostCrawler(DcardSeleniumCrawler):

    def __init__(self, browser, topic_id:str):
        super().__init__(browser)
        self._url = "https://www.dcard.tw/service/api/v2/" + "posts/" + topic_id
        self.__meta = {}
        self.__contents = ""

    def main(self):
        self._crawl()
        school = self._result.get("school")
        department = self._result.get("department")
        # if have "CardName"
        if(self._result.get("withNickname") == True):
            self.__meta["Author"] = school
            self.__meta["Author ID"] = department
        else:
            self.__meta["School"] = school
            self.__meta["Department"] = department
        # title
        self.__meta["Title"] = self._result.get("title")
        # created time
        self.__meta["Time"] = self._result.get("createdAt")
        # contents
        self.__contents = self._result.get("content").replace("\n", " ")

    @property
    def meta_result(self):
        return self.__meta

    @property
    def contents_result(self):
        return self.__contents


class DcardCommentsCrawler(DcardSeleniumCrawler):
    
    def __init__(self, browser, topic_id:str):
        super().__init__(browser)
        self._url = "https://www.dcard.tw/service/api/v2/" + "posts/" + topic_id + "/comments"
        self.__comments_list = []

    def __main(self):
        self._crawl()
        for i in range(len(self._result)):
            comment = {}
            id = self._result[i].get("id")
            comment["id"] = id
            content = self._result[i].get("content")
            if content == None:
                continue
            school = self._result[i].get("school")
            department = self._result[i].get("department")
            # if have "CardName"
            if(self._result[i]["withNickname"] == True):
                comment["Author"] = school
                comment["Author ID"] = department
            else:
                comment["School"] = school
                comment["Department"] = department
            comment["Content"] = content.replace("\n", " ")
            comment["SubComments"] = []
            # determine if have sub comments
            if self._result[i].get("subCommentCount") > 0:
                comment["has SubComments"] = True
            else: 
                comment["has SubComments"] = False
            self.__comments_list.append(comment)

    @property
    def result(self):
        self.__main()
        return self.__comments_list


class DcardSubCommentsCrawler(DcardSeleniumCrawler):
    
    def __init__(self, browser, topic_id:str, parent_comment_id:str):
        super().__init__(browser)
        self._url = "https://www.dcard.tw/service/api/v2/" + "posts/" + topic_id + "/comments" + "?parentId=" + parent_comment_id
        self.__parent_comment_id = parent_comment_id
        self.__sub_comments_list = []

    def __main(self):
        self._crawl()
        for i in range(len(self._result)):
            sub_comment = {}
            sub_comment["Parent Comment ID"] = self.__parent_comment_id
            content = self._result[i].get("content")
            if content == None:
                continue
            school = self._result[i].get("school")
            department = self._result[i].get("department")
            # if have "CardName"
            if(self._result[i]["withNickname"] == True):
                sub_comment["Author"] = school
                sub_comment["Author ID"] = department
            else:
                sub_comment["School"] = school
                sub_comment["Department"] = department
            sub_comment["Content"] = content.replace("\n", " ")
        self.__sub_comments_list.append(sub_comment)

    @property
    def result(self):
        self.__main()
        return self.__sub_comments_list
