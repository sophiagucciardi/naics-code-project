#imports
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from selenium import webdriver
from bs4 import BeautifulSoup
import time

#url input
print("Please paste the URL for the company's 'About' page, or another page that outlines what the company does:")
url = input()

#list and dict for scraped text
soups = []
soups_dict = {}

#--scraper---------------------------------------------
driver = webdriver.Firefox()
driver.get(url)
time.sleep(2)

html = driver.page_source
raw_soup = BeautifulSoup(html)
#remove white space
processed_soup = raw_soup.get_text(" ", strip=True)

driver.close()
#------------------------------------------------------

soups.append(str(processed_soup))
print(soups)

#--summarizer------------------------------------------
model_name = "allenai/led-large-16384-arxiv"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer, device=0)

long_text = processed_soup
summary = pipe(
    long_text,
    truncation=True, 
    max_length=300, 
    no_repeat_ngram_size=5, 
    num_beams=3, 
    early_stopping=True
    )

print(summary)
#-----------------------------------------------------