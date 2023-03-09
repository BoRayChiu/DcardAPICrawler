from dcard_selenium_crawler import Browser
from dcard_selenium_crawler import DcardTopicsIdCrawler
from dcard_selenium_crawler import DcardPostCrawler
from dcard_selenium_crawler import DcardCommentsCrawler
from dcard_selenium_crawler import DcardSubCommentsCrawler
import time

class DcardCrawler:

    def __init__(self, board:str, frequency:str):
        self.__board = board
        self.__frequency = frequency
        self.__wanted_topic_ids = []
        self.__result = []

    def _main(self):
        browser = Browser()
        dcard_topics_id_crawler = DcardTopicsIdCrawler(browser.get, self.__board, self.__frequency)
        self.__wanted_topic_ids = dcard_topics_id_crawler.result
        time.sleep(60)
        for topic_id in self.__wanted_topic_ids:
            res = {}
            # post
            dcard_post_crawler = DcardPostCrawler(browser.get, topic_id)
            dcard_post_crawler.main()
            res["Meta Information"] = dcard_post_crawler.meta_result
            res["Contents"] = dcard_post_crawler.contents_result
            time.sleep(60)
            # comments
            dcard_comments_crawler = DcardCommentsCrawler(browser.get, topic_id)
            res["Comments"] = []
            res{"SubComments"} = []
            comments_list = dcard_comments_crawler.result
            time.sleep(60)
            for i in range(comments_list):
                res["Comments"].append(comments_list[i])
                if comments_list[i]["has SubComments"] == True:
                    dcard_sub_comments_crawler = DcardSubCommentsCrawler(browser.get, topic_id, comments_list[i]["id"])
                    res["SubComments"].append(dcard_sub_comments_crawler.result)
                    time.sleep(60)
        self.__result.append(res)

    def get_result(self):
        self._main()
        return self.__result