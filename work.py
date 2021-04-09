import csv
import time
import requests
from bs4 import BeautifulSoup
URL = "https://www.majortests.com/word-lists/word-list-0{0}.html"


def generate_urls(url, start_page, end_page):                       # 產生urls
    urls = []
    for page in range(start_page, end_page): 
        urls.append(url.format(page))                               #收集每一頁的urls
    return urls


def get_resource(url):                                              #headers假裝是真人在瀏覽網頁防止被拒絕爬蟲!!
    headers = {
        "user-agent": "Mozilla/5.0 (Window NT 10.0; Win64; x64) ApplWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }
    return requests.get(url, headers=headers)


def parse_html(html_str):                                           #解析html之後變成lxml的形式
    return BeautifulSoup(html_str,"lxml")


def get_word(soup, file):
    words = []
    count = 0
    for wordlist_table in soup.find_all(class_="wordlist"):         #從網站程式碼看到 標籤為class
        count += 1
        for word_entry in wordlist_table.find_all("tr"):
            new_word = []                                           #蒐集每一個內容
            new_word.append(file)
            new_word.append(str(count))
            new_word.append(word_entry.th.text)
            new_word.append(word_entry.td.text)
            words.append(new_word)                                  #統一丟到words這個list裡
    return words

def web_scraping_bot(urls):
    eng_words = []
    for url in urls:
        file = url.split("/")[-1]                                   # -1:讓最後一個值變-1  由後往前為-1,-2,-3.....
        print("catching: ", file, "web data...")
        r = get_resource(url)
        if r.status_code == requests.codes.ok:
            soup = parse_html(r.text)
            words = get_word(soup, file)
            eng_words = eng_words + words
            print("waiting 5 seconds.....")
        else:
            print("HTTP request error!!") 
        print("sleep 5 second")                                     #讓他抓完休息5秒再抓以免被發現
    return eng_words        


def save_to_csv(words, file):                                       #存起來用csv檔寫出
    with open(file, "w+", newline = "", encoding = "utf-8") as fp:  # w+:以寫入的方式存起來 newline="":不要空格
        writer = csv.writer(fp)
        for word in words:
            writer. writerow(word)


if __name__ == "__main__":
    urlx = generate_urls(URL, 1, 3)
    eng_words = web_scraping_bot(urlx)
    for item in eng_words:
        print(item)
    save_to_csv(eng_words, "engWordlist_1.csv")    