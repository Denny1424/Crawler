# 該程式在抓取PTT中C_chat版的網頁，並判斷是否抓取成功
# 若成功則建立html檔，將資料傳輸進去並print出「寫入成功」
# 若失敗則只打印出「沒有抓到網頁」

#pip install requests
import requests #該模組用於爬蟲

url = "https://www.ptt.cc/bbs/C_Chat/index.html" # ptt C_chat版網址
my_headers = {'cookie': 'over18=l'} 

response = requests.get(url, headers = my_headers) 

if response.status_code == 200: # 檢查狀態，避免網址錯誤
    with open ('C_Cha.html','w',encoding = 'utf-8') as f: # 通常會寫入一個html檔檢視
        f.write(response.text) #response是一個物件，要印出來要看他的屬性「text」
    print('寫入成功')
else:# status_code == 404 
    print("沒有抓到網頁")

