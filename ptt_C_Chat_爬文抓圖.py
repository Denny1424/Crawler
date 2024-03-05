import requests
import os
from bs4 import BeautifulSoup
import urllib.parse as urlpar
import re
from tqdm import tqdm

# 下載圖片
def download(url, title, cookie, user_agent):
    # 基礎設定
    my_headers = Headers_add()
    my_headers.cookie_add(cookie)
    my_headers.user_agent_add(user_agent)
    allow = ['jpg', 'png','jpeg','gif'] #規定可下載檔案

    # 取得文章中所有連結的list
    response_article = requests.get(url,headers=my_headers()) #抓目前文章網址的HTML
    # print(response_article.status_code) # 檢查是否正確抓取該網頁
    article_soup = BeautifulSoup(response_article.text, 'html.parser')
    article_body = article_soup.find('div', id='main-content') #找出該網頁的主體
    article_a = article_body.select('a:not(.f2 a)') 
    # 選取所有不被class=f2包住的a，回傳list
    # 要這樣做是因為class=f2的節點，在ptt都被設定為是系統文字(如於...時間修改文章)

    # print (len(article_a)) # 確認該文章共有多少網址

    #圖片下載
    if len(article_a) == 0: return # 若該文章沒有任何網址則回到主程式的迴圈，進入下一篇文章
    for i in tqdm(article_a, ncols = 80): # 進度條
        href = i.get("href")
        link_split = href.split('.')
        fromat1 = link_split[-1]
        if fromat1 in allow:
            response = requests.get(href, headers = {'User-Agent':user_agent})
            if not os.path.exists(f'文章圖片/{title}'): os.makedirs(f'文章圖片/{title}')
            # 若路徑不存在則建立該路徑上的所有文建夾
            # print(response.status_code)
            with open (f'文章圖片/{title}/{href.split("/")[-1]}', "wb") as f:
                f.write(response.content)
            # 該圖片沒有內建image的content，將其直接content下來，並以二進位儲存(確保顯示圖片)

# Headers 的建構類別            
class Headers_add:
    def __init__(self,dict = {}):
        self.dict = dict
    def __call__(self):
        return self.dict
    def cookie_add(self, cookie):
        self.dict['Cookie'] = cookie
    def user_agent_add(self,user_agent):
        self.dict['User-Agent'] = user_agent

# 主程式
def main():

    # 基礎設定
    url = "https://www.ptt.cc/bbs/C_Chat/index.html"
    url_base = "https://www.ptt.cc"
    cookie = "over18=1"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
    my_headers = Headers_add() 
    my_headers.cookie_add(cookie)
    my_headers.user_agent_add(user_agent)
    
    # 取得文章List
    response = requests.get(url, headers=my_headers())
    soup = BeautifulSoup(response.text,'html.parser')
    articles = soup.find_all("div", class_ = 'r-ent')

    # 取得單筆文章的title、href
    for a in articles:
        if a.find('div', class_ = 'mark').text == 'M':
            continue
        title = a.find("div", class_ = "title")
        if title and title.a:
            title_text = title.a.text
            title_text = re.sub(r'[\\/:*?"<>|.\s]', '',title_text)
            # 後續title將作為文件檔檔名，因此需排除上面的特殊符號
            href = title.a.get("href") # 取得網址
            href = urlpar.urljoin(url_base,href) 
            # C_Chat版的文章網址是用相對路徑，因此要將其與base網址連結
            print(href)
        download(href,title_text,cookie,user_agent)

# 如果運行此py檔，則優先跑main()
if __name__ == "__main__":
    main()