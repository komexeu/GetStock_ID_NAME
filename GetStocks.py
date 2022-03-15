# coding=utf-8
# 股票資訊
from bs4 import BeautifulSoup
import urllib.request
import re
import pandas as pd
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


def get_data():
    url = "https://tw.stock.yahoo.com/class"

    content = urllib.request.urlopen(url)
    content_utf8 = content.read().decode('utf-8')
    soup = BeautifulSoup(content_utf8)
    listed_stock = soup.find(id="LISTED_STOCK")
    # print(len(listed_stock))
    links = listed_stock.find_all("ul")
    # print("count=====>", links)
    link_list = links[0].find_all("a")
    # print("count=====>", len(link_list))
    # 取得所有分類的URL
    stock_urls = []
    for k in range(0, len(link_list)):
        # print(k)
        # print(link_list[k])
        get_link = link_list[k].get('href')
        tmp_url = 'https://tw.stock.yahoo.com' + get_link
        stock_urls += [tmp_url]
        # print(get_link)
    # print(stock_urls)
    # ------------------------
    with open('stock_ID.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
        _writer = csv.writer(csvfile)
        _writer.writerow(["ID", "NAME"])
        for stock_urls_i in range(0, len(stock_urls)):
            print(stock_urls_i)
            url = stock_urls[stock_urls_i]
            soup = BeautifulSoup(content_utf8)
            # ---------------------
            options = Options()
            options.add_argument('--headless')
            options.add_argument("--disable-notifications")
            # https://sites.google.com/chromium.org/driver/
            chrome = webdriver.Chrome('./chromedriver', chrome_options=options)
            chrome.get(url)
            for x in range(1, 4):
                chrome.execute_script(
                    "window.scrollTo(0,document.body.scrollHeight)")
                time.sleep(2)
            soup = BeautifulSoup(chrome.page_source, 'html.parser')
            tables = soup.findAll("li", "List(n)")
            # ---------------------
            # main-1-ClassQuotesTable-Proxy > div >div.Pos\(r\).Ov\(h\).ClassQuotesTable > div > div > div.table-body-wrapper > ul > li:nth-child(1) > div
            # print(tables[1])

            resource = []
            print(len(tables))
            for i in range(0, len(tables)):
                # print(tables[i])
                # 股號
                y = tables[i].find("span", class_="Fz(14px) C(#979ba7) Ell")
                # print(y)
                p1 = y.text.split(".")
                p1 = p1[0]
                # 股名
                z = tables[i].find(
                    "div", class_="Lh(20px) Fw(600) Fz(16px) Ell")
                print(z)
                p2 = z.text
                # currency+=[p1 +" "+p2]
                resource += [[p1, p2]]
                # 寫入
                _writer.writerow([p1, p2])

        dt = pd.DataFrame(resource, columns=["ID", "NAME"])
        dt


if __name__ == '__main__':
    get_data()
    print("FINISH.")
