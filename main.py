from dcard_selenium_crawler import Browser
from dcard_selenium_crawler import DcardTopicsIdCrawler
from dcard_selenium_crawler import DcardPostCrawler
from dcard_selenium_crawler import DcardCommentsCrawler
from dcard_selenium_crawler import DcardSubCommentsCrawler
import time

class DcardCrawler:

    def __init__(self, board:str, frequency:str):
        self.board = board
        self.frequency = frequency
        self.wanted_topic_ids = []
        self.result = []

    def main(self):
        b = Browser()
        browser = b.get_browser()
        dcard_topics_id_crawler = DcardTopicsIdCrawler(self.browser, self.frequency)
        self.wanted_topic_ids = dcard_topics_id_crawler.get_topic_ids()
        time.sleep(60)
        for topic_id in self.wanted_topic_ids:
            res = {}
            # post
            dcard_post_crawler = DcardPostCrawler(browser, topic_id)
            dcard_post_crawler.main()
            res["Meta Information"] = dcard_post_crawler.get_meta()
            res["Contents"] = dcard_post_crawler.get_contents()
            time.sleep(60)
            # comments
            dcard_comments_crawler = DcardCommentsCrawler(browser, topic_id)
            dcard_comments_crawler.main()
            res["Comments"] = []
            res{"SubComments"} = []
            comments_list = dcard_comments_crawler.get_comments_list()
            time.sleep(60)
            for i in range(comments_list):
                res["Comments"].append(comments_list[i])
                if comments_list[i]["has SubComments"] == True:
                    dcard_sub_comments_crawler = DcardSubCommentsCrawler(browser, topic_id, comments_list[i]["id"])
                    dcard_sub_comments_crawler.main()
                    res["SubComments"].append(dcard_sub_comments_crawler.get_sub_comments_list)
                    time.sleep(60)
        self.result.append(res)

    def get_result(self):
        return self.result