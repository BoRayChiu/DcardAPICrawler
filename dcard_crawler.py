# $pip selenium
# $pip webdriver_manger
# firefox must be ".deb" not "snap"


from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
import time
import json
from post_crawler import post_crawler
from comments_crawler import comments_crawler


def dcard_crawler(board:str, frequency:int)->list:
    board_url = f"https://www.dcard.tw/service/api/v2/forums/{board}/posts?limit={frequency}"
    browser.get(board_url)
    time.sleep(5)
    browser.find_element(By.CSS_SELECTOR, "#rawdata-tab").click()
    posts = browser.find_element(By.CSS_SELECTOR, "#rawdata-panel pre.data").text
    browser.quit()
    posts = json.loads(posts)
    time.sleep(10)
    # save every demand topic id
    post_ids = []
    for f in range(frequency):
        post_ids.append(posts[f]["id"])
    # request every topic in topic_ids
    posts_list = []
    for post_id in post_ids:
        post_dict = {}
        post_dict["Post"] = post_crawler(post_id)
        post_dict["Comments"] = comments_crawler(post_id)
        posts_list.append(post_dict)

    return posts_list

if __name__ == "__main__":
    # install the firefox which version is 0.32.0
    browser = webdriver.Firefox(executable_path=GeckoDriverManager(version="v0.32.0").install())
