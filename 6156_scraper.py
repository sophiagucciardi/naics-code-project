from selenium import webdriver
from bs4 import BeautifulSoup
import time

# 
# soups:
# {
#  "url1": soup1,
#  "url2": soup2
# }
# 

urls = ["https://bsmlawfirm.com/practice-areas", "https://www.pinnacletravelstaffing.com/"]
soups = {}

for url in urls:
    
    driver = webdriver.Firefox()
    driver.get(url)
    time.sleep(2)

    html = driver.page_source

    soup = BeautifulSoup(html)
    soups[url] = soup

    print(soup.text)
    driver.close()

