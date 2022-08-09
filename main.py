from datetime import datetime
import csv
from typing import Generator, List

import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet


URL = "https://ru.wikipedia.org/wiki/Города_Киргизии"
WIKIPEDIA = 'https://ru.wikipedia.org/'

def get_response(url: str) -> requests:
    return requests.get(url)


def get_html(response: requests) -> requests:
    return response.text


def get_table(html: requests) -> ResultSet:
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all("table", {'class': 'wikitable sortable'})


def get_headers(table: ResultSet) -> List[str]:
    headers = []
    for row in table:
        if row.find_all("th"):
            table_headings = row.find_all("th")
            for th in table_headings:
                headers.append(th.text.strip())
            headers.append('Link')
    return headers


def get_tr(tables: ResultSet) -> Generator:
    for table in tables:
        table_rows = table.find_all("tr")
        for row in table_rows:
            if row.find_all("td"):
                yield row.find_all("td")


def get_td(table_data: Generator) -> Generator:
    for rows in table_data:
        row_data = []
        link_data = []
        count = 0
        for td in rows:
            if count % 18 == 2:
                try:
                    row_data.append(WIKIPEDIA + td.find('a')['href'])
                    continue
                except TypeError:
                    pass
            if count % 18 == 0:
                link_data.append(td.find('a')['href'])
            row_data.append(td.text.strip())
            count += 1
        for link in link_data:
            row_data.append(WIKIPEDIA + link)
        if row_data:
            yield row_data


def write_csv(headers: List[str], data: Generator):
    with open(f"{datetime.now().date()}_cities.csv", "w+", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for row in data:
            writer.writerow(row)


def main(url: str):
    response = get_response(url)
    html = get_html(response)
    table = get_table(html)
    headers = get_headers(table)
    trs = get_tr(table)
    tds = get_td(trs)
    write_csv(headers, tds)


if __name__ == "__main__":
    main(URL)
