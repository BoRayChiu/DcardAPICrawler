# $pip selenium
# $pip webdriver_manger
# firefox must be ".deb" not "snap"


from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
import time


def post_crawler(post_id:str)->dict:
    # get post.json and change it to list
    post_url = f"https://www.dcard.tw/service/api/v2/posts/{post_id}"
    browser.get(post_url)
    time.sleep(5)
    browser.find_element(By.CSS_SELECTOR, "#rawdata-tab").click()
    post = browser.find_element(By.CSS_SELECTOR, "#rawdata-panel pre.data").text
    browser.quit()
    post = json.loads(post)
    time.sleep(10)
    # grab what we want in post.json
    # meta information
    post_box = {}
    meta_box = {}
    school = post.get("school")
    department = post.get("department")
    # if have "卡稱"
    if(post["withNickname"] == True):
        meta_box["Author"] = school
        meta_box["Author ID"] = department
    else:
        meta_box["School"] = school
        meta_box["Department"] = department
    # title
    meta_box["Title"] = post["title"]
    # created time
    meta_box["Time"] = post["createdAt"]
    # collect into dict what we'll return
    post_box["MetaInformation"] = meta_box
    # contents
    post_box["Contents"] = post["content"].replace("\n", " ")

    return post_box

if __name__ == "__main__":
    # install the firefox which version is 0.32.2(equl to the version in local)
    browser = webdriver.Firefox(executable_path=GeckoDriverManager(version="v0.32.0").install())
    # test example
    print(post_crawler("241178376"))
