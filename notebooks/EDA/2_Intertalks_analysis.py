# %%


# OPTIONAL: Load the "autoreload" extension so that code can change
%load_ext autoreload

# OPTIONAL: always reload modules so that as you change code in src, it gets loaded
%autoreload 2

# %%
from selenium import webdriver

DRIVER_PATH = 'sl_web_driver/chromedriver.exe'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
# driver.get('https://intranet.intertops.co.ag/Lists/Posts/Post.aspx?ID=333')

# %%
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
from fake_useragent import UserAgent
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')



# %%
# save all scrapped data on a dataframe 
# article id | article body | raking
data = pd.DataFrame(columns=['id', 'body', 'ranking'])
ua = UserAgent()
a = ua.random
user_agent = ua.random
print(user_agent)
chrome_options.add_argument(f'user-agent={user_agent}')
driver = webdriver.Chrome(executable_path=DRIVER_PATH,chrome_options=chrome_options)
articles_ids = [1]
for id in articles_ids:
      website = 'https://intranet.intertops.co.ag/Lists/Posts/Post.aspx?ID=333'
      driver.get(website)
      retries = 1
      while retries <= 5:
          try:
              #print(retries)
              WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME ,'ms-belltown-authenticated')))
              break;
          except TimeoutException:
              driver.refresh()
              retries += 1
      if retries >= 5 :
        print('number of pages excited')
        break
      page_source = driver.page_source
      feature_soup = BeautifulSoup(page_source, 'lxml')
      # get article 
      text_list = feature_soup.find("div","ExternalClassA1C411029006484C9CDF974401DEA214").find_all('p')
      full_text = "\n".join([x.text for x in text_list[1:]])
      # get comments
      # get number of stars
      rank = feature_soup.find("span","ms-comm-ratingCountContainer").text
      row = [id, full_text,rank ]
      data.loc[len(data)] = row

# show data
data.head()

# %%
"""
# Analyse data
"""

# %%
all_sentences = data.body.values[0].split('\n')
all_sentences

# %%
#This splits all the sentences up which makes it easier for us to work with

all_sentences = []

for word in data.body.values:
    all_sentences.append(word)
#split data into lines 
all_sentences = data.body.values[0].split('\n')
lines = list()
for line in all_sentences:    
    words = line.split()
    for w in words: 
       lines.append(w)


print(lines)

# %%
"""
# Get all website data 
"""

# %%
# save all scrapped data on a dataframe 
# article id | article body | raking
from selenium.webdriver.common.by import By
data = pd.DataFrame(columns=['id', 'body', 'ranking'])
ua = UserAgent()
a = ua.random
user_agent = ua.random
print(user_agent)
chrome_options.add_argument(f'user-agent={user_agent}')
driver = webdriver.Chrome(executable_path=DRIVER_PATH,chrome_options=chrome_options)
website = 'https://intranet.intertops.co.ag/Lists/Posts/AllPosts.aspx' # first page containing list of all posts 
start_page_id = 0
while True:
      driver.get(website)
      retries = 1
      while retries <= 5:
          try:
              #print(retries)
              WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME ,'ms-belltown-authenticated')))
              break
          except TimeoutException:
              driver.refresh()
              retries += 1
      if retries >= 5 :
        print('number of pages excited 1')
        break
      page_source = driver.page_source
      feature_soup = BeautifulSoup(page_source, 'lxml')
      # get article 
      posts_list = feature_soup.find('table', "ms-listviewtable" ).find('tbody').find_all('tr')
      # text_list = feature_soup.find("div","ExternalClassA1C411029006484C9CDF974401DEA214").find_all('p')
      # full_text = "\n".join([x.text for x in text_list[1:]])
      rep = 1 
      test= False
      while not posts_list:
          driver.refresh()
          rep += 1 
          page_source = driver.page_source
          feature_soup = BeautifulSoup(page_source, 'lxml')
          posts_list = feature_soup.find('table', "ms-listviewtable" ).find('tbody').find_all('tr')
          if rep >5 : 
            print('number of pages excited 2')
            test = True
            break
      if test == True : 
        print("page not found")
        break
      window_before = driver.window_handles[0]
      # post_links = driver.find_elements(By.XPATH, 'ms-listlink ms-draggable')
      post_links = driver.find_element(By.CSS_SELECTOR, '.ms-vb  .ms-vb-menuPadding .itx')
      post_href = post_links.get_attribute('href')
      # post_links = driver.find_elements(By.CLASS_NAME, 'ms-listlink ms-draggable') 
      # for post_details, post_link in zip(posts_list, post_links):
      for i in range(1):
        print("yesssssssssssssssss")
        driver.execute_script('window.open(arguments[0]);', post_href)
        # ActionChains(driver).move_to_element(post_links).click().perform()
        print(driver.window_handles)
        window_after = driver.window_handles[1]
        driver.switch_to.window(window_after)
        print("Second window title = " + driver.title)
        time.sleep(random.randint(2,3))

        print('dooooooooooooone')
          
      # get comments
      # # get number of stars
      # rank = feature_soup.find("span","ms-comm-ratingCountContainer").text
      # row = [id, full_text,rank ]
      # data.loc[len(data)] = row
      try:
        print('moving to next page ...')
        start_page_id += 1 
        website = f"https://intranet.intertops.co.ag/Lists/Posts/AllPosts.aspx#InplviewHash6e752d3c-cdd4-45c5-96e8-907bfd86f62d=Paged%3DTRUE-p_PublishedDate%3D20220525%252005%253a18%253a00-p_ID%3D336-FolderCTID%3D0x012001-PageFirstRow%3D{start_page_id}"
      except Exception as ex:
        pirnt('cant move to the next page!!') 
        print(ex)
      break
        

driver.close()
# show data
data.head()

# %%
# assign URL
driver.get("https://login.yahoo.com/")
print("First window title = " + driver.title)
  
# switch to new window
driver.find_element_by_class_name("privacy").click()
print(driver.window_handles)
driver.switch_to.window(driver.window_handles[1])
print("Second window title = " + driver.title)

# %%
# example for the links og the first 3 pages 
# each page contains 30 article 
https://intranet.intertops.co.ag/Lists/Posts/AllPosts.aspx#InplviewHash6e752d3c-cdd4-45c5-96e8-907bfd86f62d=FolderCTID%3D0x012001
https://intranet.intertops.co.ag/Lists/Posts/AllPosts.aspx#InplviewHash6e752d3c-cdd4-45c5-96e8-907bfd86f62d=Paged%3DTRUE-p_PublishedDate%3D20220525%252005%253a18%253a00-p_ID%3D336-FolderCTID%3D0x012001-PageFirstRow%3D31
https://intranet.intertops.co.ag/Lists/Posts/AllPosts.aspx#InplviewHash6e752d3c-cdd4-45c5-96e8-907bfd86f62d=Paged%3DTRUE-p_PublishedDate%3D20220311%252008%253a41%253a00-p_ID%3D311-FolderCTID%3D0x012001-PageFirstRow%3D61

# %%
"""
we notice tat beside the first page all other pages can be determined by the **PageFirstRow**
"""

# %%
text_list = feature_soup.find("div","ExternalClassA1C411029006484C9CDF974401DEA214").find_all('p')
"\n".join([x.text for x in text_list[1:]])

# %%
text_article[0].find_all("p")[1].text

# %%
