import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import time

#想把資料給別人可以用JSON格式

url = "https://www.youtube.com/watch?v=lcJMuMZWqps"
headers = {'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15'}
cookies = {'over18': '1'}
# 建立 Excel
wb = Workbook()
ws = wb.active
ws.title = "Youtobe Andy 收到的贊助金額"

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