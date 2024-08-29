from janome.tokenizer import Tokenizer
from janome.tokenfilter import CompoundNounFilter
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from collections import Counter
import time
import pandas as pd
import csv
import re
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)



driver = webdriver.Chrome()
driver.get("https://google.com")
time.sleep(5)
search_box = driver.find_element(By.XPATH, '//*[@id="APjFqb"]')
search_box.click()
search_word = "就活　26卒"
search_box.send_keys(search_word)
search_box.click()
search_box.send_keys(Keys.RETURN)
time.sleep(5)
count = 10
results = []

while len(results) < count:
    current_results = [
        {
            'title': title.text,
            'link': title.find_element(By.XPATH, '..').get_attribute('href')
        }
        for title in driver.find_elements(By.CSS_SELECTOR, "h3")
        if title.text.strip()
    ]
    results.extend(current_results)
    if len(results) >= count:
        break    
    if len(results) < count:
        try:
            next_button = driver.find_element(By.ID, "pnnext")  
            next_button.click()
            time.sleep(2)  
        except Exception as e:
            break

time.sleep(5)
results = results[:count]
all_titles = []
all_headings = []
site_lengths = []

for index, result in enumerate(results):
    driver.get(result['link'])
    time.sleep(2)
    body_text = driver.find_element(By.TAG_NAME, "body").text
    text_length = len(body_text)
    site_lengths.append(text_length)
    headings = [heading.text for heading in driver.find_elements(By.TAG_NAME, "h2") if heading.text.strip()]
    all_headings.extend(headings)   
    all_titles.append(result['title'])
    print(f"{index + 1}: {result['title']}")
    for i, heading in enumerate(headings):
        print(f"  {i + 1}. {heading}")
    print(f"  記事全体の文字数: {text_length}")
    print("-" * 50)
    time.sleep(2)

tokenizer = Tokenizer()
token_filters = [CompoundNounFilter()]
words = []
title_words = []

for title in all_titles:
    tokens = tokenizer.tokenize(title)
    for token in tokens:
        if token.part_of_speech.split(',')[0] == "名詞" and len(token.surface) > 1:
            title_words.append(token.surface)

title_word_counts = Counter(title_words)
common_title_words = title_word_counts.most_common()

print("\nタイトルの共通単語:")
for word, freq in common_title_words:
    print(f"{word}: {freq}")

for heading in all_headings:
    tokens = tokenizer.tokenize(heading)
    previous_token = None
    for token in tokens:
        if token.part_of_speech.split(',')[0] == "名詞":
            if previous_token and previous_token.part_of_speech.split(',')[0] == "名詞":
                combined_word = words[-1] + token.surface
                words[-1] = combined_word if len(combined_word) > 1 else '' 
            else:
                words.append(token.surface if len(token.surface) > 1 else '')
        elif token.part_of_speech.split(',')[0] != "助詞" and len(token.surface) > 1:
            words.append(token.surface)
        previous_token = token

words = [word for word in words if word]
time.sleep(2)
word_counts = Counter(words)
time.sleep(2)
common_words = word_counts.most_common()
time.sleep(2)
for word, freq in common_words:
    print(f"{word}: {freq}")

average_length = sum(site_lengths) / len(site_lengths) if site_lengths else 0
print(f"各サイトの平均文字数: {average_length}")


# csv出力

csv_file_path = 'D:/python/output.csv'
with open(csv_file_path, 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Link', 'Text_Length'])
    for result, length in zip(results, site_lengths):
        writer.writerow({'Title': result['title'], 'Link': result['link'], 'Text_Length': length})
    writer.writerow([])
    writer.writerow(['見出し'])
    for heading in all_headings:
        writer.writerow([heading])
    writer.writerow([])
    writer.writerow(['単語', '出現回数'])
    for word, freq in common_words:
        writer.writerow([word, freq])
    writer.writerow([])
    writer.writerow(['単語', '出現回数'])
    for word, freq in common_title_words:
        writer.writerow([word, freq])


csv_file_path = 'D:/python/output.csv'

with open(csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
    fieldnames = ['Title', 'Link', 'Text_Length', 'Headings']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    
    for result, length in zip(results, site_lengths):
        headings_str = ' | '.join(
            heading for heading in all_headings if heading in result['title']
        )
        
        writer.writerow({
            'Title': result['title'],
            'Link': result['link'],
            'Text_Length': length,
            'Headings': headings_str
        })

all_headings_combined = []
for headings in all_headings:
    combined_headings = ' | '.join(headings)
    all_headings_combined.append(combined_headings)


for index, heading in enumerate(all_headings):
    print(f"Heading {index + 1}:")
    print(f"  {heading}")
    print("-" * 50)


with open(csv_file_path, 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    
    writer.writerow(['Title', 'Headings', 'Text_Length'])
    for index, result in enumerate(results):
        title = result['title']
        text_length = site_lengths[index]
        headings = [heading for heading in all_headings if heading.startswith(title)]
        headings_str = '\n'.join(headings) 
        
        writer.writerow([title, headings_str, text_length])

with open(csv_file_path, 'w', newline='', encoding='utf-8-sig') as file:
    fieldnames = ['Title', 'Link', 'Text_Length']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for result, length in zip(results, site_lengths):
        writer.writerow({'Title': result['title'], 'Link': result['link'], 'Text_Length': length})