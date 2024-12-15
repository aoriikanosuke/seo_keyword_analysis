from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
import urllib.parse

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    search_results = get_search_results(keyword)
    return render_template('results.html', keyword=keyword, results=search_results)

def get_search_results(keyword):
    # Google検索結果からリンクを取得
    search_url = f"https://www.google.com/search?q={keyword}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    search_results = []
    links = []

    # 検索結果のリンクを抽出
    for a_tag in soup.select('a[href^="/url?q="]')[:11]:
        link = a_tag['href'].split('/url?q=')[1].split('&')[0]
        link = urllib.parse.unquote(link) 
        if link not in links:  # 重複を排除
            links.append(link)

    # 各リンク先のページを解析
    for link in links:
        try:
            page_response = requests.get(link, headers=headers, timeout=5)
            page_soup = BeautifulSoup(page_response.text, 'html.parser')

            title = page_soup.title.string if page_soup.title else "No Title"
            h2_tags = [h2.get_text(strip=True) for h2 in page_soup.find_all('h2')]
            text_length = len(page_soup.get_text())

            search_results.append({
                'link': link,
                'title': title,
                'h2_tags': h2_tags,
                'text_length': text_length
            })
        except Exception as e:
            print(f"Error fetching {link}: {e}")
            continue

    return search_results

if __name__ == '__main__':
    app.run(debug=True)
