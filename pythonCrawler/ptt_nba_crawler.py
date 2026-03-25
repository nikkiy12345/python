from http.client import responses

"""
requests 下載網頁
beautifulSoup 解析網頁，取得資料

"""
"""
import  requests
from bs4 import BeautifulSoup


url = "https://www.ptt.cc/bbs/nba/index.html"
#headers 反爬蟲
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
articles = soup.find_all("div", class_="r-ent")

for a in articles:
    title = a.find("div", class_="title")
    if title and title.a:  #如果有標題的話讓title 變成標題
        title = title.a.text
    else: #不符合上述條件的話，則把title設為沒有標題
        title = "沒有標題"
    print(title)

    popular = a.find("div", class_="nrec")
    if popular and popular.span:
        popular = popular.span.text
    else:
        popular = "N/A"
    print(popular)

"""
"""
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import csv

url = "https://www.ptt.cc/bbs/nba/index.html"
headers = {'User-Agent': 'Mozilla/5.0'}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

articles = soup.find_all("div", class_="r-ent")

# 開啟 CSV 檔案
with open("ptt_nba.csv", "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)

    # 寫入表頭
    writer.writerow(["人氣", "標題", "日期"])

    for a in articles:
        # 標題
        title_tag = a.select_one(".title a")
        title = title_tag.text.strip() if title_tag else "沒有標題"

        # 推文數
        nrec_tag = a.select_one(".nrec span")
        popular = nrec_tag.text if nrec_tag else "N/A"

        date_tag = a.select_one(".date")
        date = date_tag.text.strip() if date_tag else "N/A"

        writer.writerow([popular, title, date])

print("已存成 ptt_nba.csv")
"""
# print(response.text)
# if response.status_code == 200:
#    with open('output.html', 'w', encoding='utf-8') as f:
#     f.write(response.text)
#    print("寫入成功")
# else:
#    print("沒有抓到網頁")


import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import time

url = "https://www.ptt.cc/bbs/nba/index.html"
headers = {'User-Agent': 'Mozilla/5.0'}
cookies = {'over18': '1'}
# 建立 Excel
wb = Workbook()
ws = wb.active
ws.title = "PTT NBA"

# 表頭
ws.append(["人氣", "標題", "日期"])

for page in range(5):
    print(f"正在抓第 {page+1} 頁: {url}")

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = soup.find_all("div", class_="r-ent")

    for a in articles:
        title_tag = a.select_one(".title a")
        title = title_tag.text.strip() if title_tag else "沒有標題"

        nrec_tag = a.select_one(".nrec span")
        popular = nrec_tag.text if nrec_tag else "N/A"

        date_tag = a.select_one(".date")
        date = date_tag.text.strip() if date_tag else "N/A"

        ws.append([popular, title, date])

        buttons = soup.select("div.btn-group.btn-group-paging a")
        for b in buttons:
            if "上頁" in b.text:
                url = "https://www.ptt.cc" + b["href"]
                break

        time.sleep(1)  # 防擋



# 存檔
wb.save("ptt_nba_5pages.xlsx")

print(" 已抓取 5 頁並存成 Excel")
print(url)