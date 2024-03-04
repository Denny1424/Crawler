#該程式在抓取文章列表，包含人氣、標題、時間等
#並將列表儲存為json格式，方便後續使用

#pip install beautifulsoup4
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd


url = "https://www.ptt.cc/bbs/C_Chat/index.html" # ptt C_chat版網址
my_headers = {'cookie': 'over18=l'} 
response = requests.get(url, headers = my_headers) 
soup = BeautifulSoup(response.text, "html.parser") # 先建立一個beautifulSoup物件
    # 分析response.text, 並使用html的解析器
articles = soup.find_all("div", class_ = "r-ent") 
    # find_all() 可找到所有符合條件的元素，且會回傳列表
    # 找出所有div節點，再從其中找出class名稱為"r-ent"的項，並加入列表內
    # 此步驟需通過F12確認所需資料的節點及class的名稱

#print(articles)
#print(articles[0])
# print (type(articles)

data_list = []
for item in articles:
    # 遍歷每一個文章

    data = {}

    title = item.find("div", class_="title") # 搜索該文章div中class名為"title"的節點
    if title and title.a: # 判斷是否有title且title要有連結(a)，避免報錯
        title = title.a.text # 取出該title節點中，超連結的文字(a.text)
    else:
        title = "沒有標題"
    data["標題"] = title

    popular = item.find("div", class_="nrec") # 人氣
    if popular and popular.span:
        popular = popular.span.text
    else:
        popular = "N/A"
    data["人氣"] = popular
    #popular = item.find_all('div', class_="nrec")[0].span.text
    #這樣會出問題，該網頁設計是如果文章還沒有人推、虛的話會直接沒span出東西
    
    date = item.find_all('div', class_="date")[0].text
    data["日期"] = date 
    # 回傳的是個列表，因此不能直接.text，若確定只有一項，再加個[0]取出就好
    # 該方法較不穩定，若文章被刪除之類的可能會直接報錯

    data_list.append(data)

    #print (f'{popular} {title} {date}')

#儲存為json檔
with open ("ptt_C_chat.json","w", encoding="utf-8") as file:
    json.dump(data_list, file, ensure_ascii=False, indent = 4)
    #將資料寫成json檔，將data_list的資料寫入file,不將非ASCII字符轉義(如中文)，使用四個空格作為縮排
print("已成功將資料匯入json檔案")

#儲存為excel檔
df = pd.DataFrame(data_list) # 先將其轉為pd內的DataFrame格式
df.to_excel("ptt_C_chat.xlsx", index = False, engine = "openpyxl") # to_後有很多儲存的格式可以選
    # 將該DataFrame儲存為excel的格式，關閉索引標籤、寫入Excel檔案的引擎為"openpyxl"
print("已成功將資料匯入excel")
