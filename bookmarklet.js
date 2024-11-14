javascript:(function(){
    const searchWord = prompt("検索キーワードを入力してください:", "it業界 志望動機");
    if (!searchWord) return;

    // Google検索にリダイレクト
    window.open(`https://www.google.com/search?q=${encodeURIComponent(searchWord)}`, "_self");

    // 結果の収集
    setTimeout(function collectResults(){
        const results = [];
        document.querySelectorAll("h3").forEach((titleElement) => {
            const title = titleElement.innerText;
            const linkElement = titleElement.closest("a");
            if (linkElement && title) {
                results.push({ title, link: linkElement.href });
            }
        });

        console.clear();
        console.log(`検索キーワード: ${searchWord}`);
        results.slice(0, 10).forEach((result, index) => {
            console.log(`${index + 1}: ${result.title}\n  リンク: ${result.link}`);
        });
        if (results.length === 0) {
            console.log("検索結果が見つかりませんでした。");
        }
    }, 3000); // ページロードのため3秒待機

})();
