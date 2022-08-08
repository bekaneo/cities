from datetime import datetime

import requests
from bs4 import BeautifulSoup
import csv

url = "https://ru.wikipedia.org/wiki/Города_Киргизии"

response = requests.get(url)
html_page = response.text

soup = BeautifulSoup(html_page, 'html.parser')
tables = soup.find_all("table", {'class': 'wikitable sortable'})
for index, table in enumerate(tables):

    table_rows = table.find_all("tr")

    with open(f"{datetime.now().date()}_cities.csv", "w+", newline="") as file:
        writer = csv.writer(file)
        for row in table_rows:
            row_data = []
            if row.find_all("th"):
                table_headings = row.find_all("th")
                for th in table_headings:
                    row_data.append(th.text.strip())
                row_data.append('Link')
            else:
                link_data = []
                table_data = row.find_all("td")
                count = 0
                for td in table_data:
                    if count % 18 == 2:
                        try:
                            row_data.append('https://ru.wikipedia.org/' + td.find('a')['href'])
                            continue
                        except TypeError:
                            pass
                    if count % 18 == 0:
                        link_data.append(td.find('a')['href'])
                    row_data.append(td.text.strip())
                    count += 1
                for link in link_data:
                    row_data.append('https://ru.wikipedia.org/' + link)
            writer.writerow(row_data)
