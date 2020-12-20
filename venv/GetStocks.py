# 股票資訊
from bs4 import BeautifulSoup
import urllib.request, re
import pandas as pd
import csv


def get_data():
    url = "https://tw.stock.yahoo.com/class"
    content = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(content)
    listed_stock = soup.find(id="LISTED_STOCK")
    # print(len(listed_stock))
    links = listed_stock.find("ul", "W(100%) Bxz(bb) P(20px) Bdrs(8px) Bgc($c-light-gray)")
    # print(len(links))
    link_list = links.find_all("a")
    # print(link_list)
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
    with open('stock_ID.csv', 'w', newline='', encoding='utf-8') as csvfile:
        _writer = csv.writer(csvfile)
        _writer.writerow(["ID", "NAME"])
        for stock_urls_i in range(0, len(stock_urls)):
            print(stock_urls_i)
            url = stock_urls[stock_urls_i]
            content = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(content)
            tables = soup.findAll("li", "List(n)")
            ##main-1-ClassQuotesTable-Proxy > div >div.Pos\(r\).Ov\(h\).ClassQuotesTable > div > div > div.table-body-wrapper > ul > li:nth-child(1) > div
            # print(tables[1])

            resource = []
            x = tables[0].findAll("tr")

            for i in range(0, len(tables)):
                # print(tables[i])
                y = tables[i].find("span", class_="Fz(14px) C(#979ba7) Ell")
                #print(y)
                p1 = y.text.split(".")
                p1 = p1[0]
                z = tables[i].find("a")
                # print(z)
                p2 = z.text
                # currency+=[p1 +" "+p2]
                resource += [[p1, p2]]
                # 寫入
                _writer.writerow([p1, p2])

        dt = pd.DataFrame(resource, columns=["ID", "NAME"])
        dt


if __name__ == '__main__':
    get_data()
