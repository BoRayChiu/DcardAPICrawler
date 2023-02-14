# $pip selenium
# $pip webdriver_manger
# firefox must be ".deb" not "snap"


from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
import time
#from sub_comments_crawler import sub_comments_crawler


def comments_crawler(post_id:str)->list:
    # get comments.json and change it to list
    comments_url = f"https://www.dcard.tw/service/api/v2/posts/{post_id}/comments"
    browser.get(comments_url)
    time.sleep(5)
    browser.find_element(By.CSS_SELECTOR, "#rawdata-tab").click()
    comments = browser.find_element(By.CSS_SELECTOR, "#rawdata-panel pre.data").text
    browser.quit()
    comments= json.loads(comments)
    time.sleep(10)
    # grab what we want in comments.json
    comments_list = []
    for c in range(len(comments)):
        comment_dict = {}
        content = comments[c].get("content")
        # if comment has been removed
        if(content == None):
            continue
        school = comments[c].get("school")
        department = comments[c].get("department")
        # if have "卡稱"
        if(comments[c]["withNickname"] == True):
            comment_dict["Author"] = school
            comment_dict["Author ID"] = department
        else:
            comment_dict["School"] = school
            comment_dict["Department"] = department
        comment_dict["Content"] = content.replace("\n", " ")
        # determine if have sub comments
        #sub_comments_count = comments[c]["subCommentCount"]
        #if(sub_comments_count > 0):
            #comment_id = comments[c]["id"]
            #comment_dict["SubComments"] = sub_comments_crawler(comments_url, comment_id)
        # collect into list what we'll return 
        comments_list.append(comment_dict)

    return comments_list

if __name__ == "__main__":
    # install the firefox which version is 0.32.2(equl to the version in local)
    browser = webdriver.Firefox(executable_path=GeckoDriverManager(version="v0.32.2").install())
    # test example
    print(comments_crawler("241178376"))
