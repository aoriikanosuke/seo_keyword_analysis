from flask import Flask, request, render_htmls
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return render_htmls('index.html')

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    search_results = get_search_results(keyword)
    return render_htmls('results.html', keyword=keyword, results=search_results)

def get_search_results(keyword):
    # 検索結果を取得する例（Google検索の場合、適切なAPIを使うべき）
    url = f"https://www.google.com/search?q={keyword}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    titles = []
    for g in soup.find_all('h2')[:10]:  # 検索結果上位10件
        titles.append(g.text)
    return titles

if __name__ == '__main__':
    app.run(debug=True)
