#This will not run on online IDE 
import requests 
from bs4 import BeautifulSoup 
import getpass
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
from main import Predict_tweet
# Initialize WebDriver
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options

def scraping_comments_insta_post(link_post):





    chrome_options = Options()
    # chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--no-sandbox") # linux only
    chrome_options.add_argument("--headless=new") # for Chrome >= 109
    # chrome_options.add_argument("--headless")
    # chrome_options.headless = True # also works
    #driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Edge()


    # Open the URL of the webpage
# Open the URL of the webpage
    url = "https://www.instagram.com"
    driver.get(url)
    time.sleep(2)

    username = ""
    #password = getpass.getpass(prompt='Your favorite flower? ')
    password = ""
    driver.find_elements(By.TAG_NAME , "input")[0].send_keys(username)
    driver.find_elements(By.TAG_NAME , "input")[1].send_keys(password)

    driver.find_elements(By.TAG_NAME,"button")[1].click()

    time.sleep(15)
    # driver.get("https://www.instagram.com/p/C5KvO7lNjHP/?hl=en")

    driver.get(link_post)
    time.sleep(3)



    for i in range(25):
        driver.execute_script('document.querySelector(\'[class="x5yr21d xw2csxc x1odjw0f x1n2onr6"]\').scrollBy(0,50000)')
        time.sleep(0.6)

    
    time.sleep(3)


    list_of_name_links = []

    profile_links = driver.find_elements(By.XPATH, "//a[@class='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz notranslate _a6hd']")
    for links in profile_links:

        list_of_name_links.append([links.text,links.get_attribute("href")])

    df_of_name_links = pd.DataFrame(list_of_name_links[1:],columns = ["User_Name","Profile_Link"]).drop_duplicates()
    UserProfile_UserComment = driver.find_elements(By.XPATH, "//span[@class='x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp xo1l8bm x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj']")
    list_UserProfile_UserComment = [ele.text for ele in UserProfile_UserComment]


    df_of_name_comment = pd.DataFrame(np.array(list_UserProfile_UserComment[1:-1]).reshape(-1,2), columns=["User_Name","User_Comment"])



    df_user_link_comment = pd.merge(df_of_name_links , df_of_name_comment, on="User_Name")

    comment_datetime = driver.find_elements(By.XPATH, "//time[@class='x1ejq31n xd10rxx x1sy0etr x17r0tee x1roi4f4 xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6']")
    list_comment_datetime = [ele.get_attribute("datetime") for ele in comment_datetime]
    df_user_link_comment["datetime"] = list_comment_datetime



    df_user_link_comment["Predict"] = Predict_tweet(df_user_link_comment["User_Comment"])
    df_user_link_comment["post_link"] = [link_post] * len(df_user_link_comment)
    df_user_link_comment["predict_cat"] = df_user_link_comment["Predict"].apply(lambda x : "Negative" if x == 0.0 else "Positive")


    df_user_link_comment.to_csv("test_insta.csv")


    driver.set_window_size(500, 1000)
    post_date = driver.find_elements(By.XPATH, "//time[@class='x1p4m5qa']")
    post_owner = driver.find_elements(By.XPATH, "//a[@class='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz notranslate _a6hd']")
    num_likes_comment = driver.find_elements(By.XPATH, "//span[@class='html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs']")
    list_post_info = [[link_post,post_owner[0].text,post_owner[0].get_attribute("href"),int(num_likes_comment[0].text.replace(',', '')),int(num_likes_comment[1].text.replace(',', '')),post_date[0].get_attribute("datetime")]]

    

    return df_user_link_comment,list_post_info