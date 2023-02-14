# $pip selenium
# $pip webdriver_manger
# firefox must be ".deb" not "snap"from selenium import webdriver


from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
import time


def sub_comments_crawler(parent_comment_url:str, parent_comment_id:str)->list
    # get sub_comments.json and change it to list
    sub_comments_url = parent_comment_url+"?parentId="+parent_comment_id
    browser.get(sub_comments_url)
    time.sleep(5)
    browser.find_element(By.CSS_SELECTOR, "#rawdata-tab").click()
    sub_comments = browser.find_element(By.CSS_SELECTOR, "#rawdata-panel pre.data").text
    browser.quit()
    sub_comments= json.loads(sub_comments)
    time.sleep(10)
    # grab what we want in sub_comments.json
    sub_comments_list = []
    for s in range(len(sub_comments)):
        sub_comment_dict = {}
        content = sub_comments[s].get("content")
        # if comment has been removed 
        if(content == None):
            continue
        school = sub_comments[s].get("school")
        department = sub_comments[s].get("department")
        # if have "卡稱"
        if(sub_comments[s]["withNickname"] == True):
            sub_comment_dict["Author"] = school
            sub_comment_dict["Author ID"] = department
        else:
            sub_comment_dict["School"] = school
            sub_comment_dict["Department"] = department
        sub_comment_dict["Content"] = content.replace("\n", " ")
        # collect into list what we'll return 
        sub_comments_list.append(sub_comment_dict)

    return sub_comments_list


if __name__ == "__main__":
    # install the firefox which version is 0.32.2(equl to the version in local)
    browser = webdriver.Firefox(executable_path=GeckoDriverManager(version="v0.32.2").install())
    # test example
    print(sub_comments_crawler("https://www.dcard.tw/service/api/v2/posts/241147748/comments", "8ed9516e-5d48-456c-b886-daf0ad8ceef4"))
