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

# ドライバーのセットアップ処理
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=chrome_options)

# 開きたいドライバーのURLを持ってくる
def perform_search(driver, search_word): 
    driver.get("https://google.com") 
    time.sleep(2)
    search_box = driver.find_element(By.XPATH, '//*[@id="APjFqb"]')
    search_box.click()
    search_box.send_keys(search_word)
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)

# 取得したデータの格納先
def collect_search_results(driver, count):
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
        try:
            next_button = driver.find_element(By.ID, "pnnext")
            next_button.click()
            time.sleep(2)
        except Exception:
            break
    return results[:count]

# 取得したデータの出力処理
def extract_content_from_pages(driver, results):
    all_titles, all_headings, site_lengths = [], [], []
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
    return all_titles, all_headings, site_lengths

def main():
    driver = setup_driver() # ドライバーの取得
    search_word = "it業界　志望動機" # 検索KWを入力
    perform_search(driver, search_word)
    results = collect_search_results(driver, count=5) #countは調べたいURLの個数,デフォルト10個
    all_titles, all_headings, site_lengths = extract_content_from_pages(driver, results)
    driver.quit()

if __name__ == "__main__":
    main()
