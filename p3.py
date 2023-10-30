import requests
import openpyxl
from bs4 import BeautifulSoup

keyword = input("What are you looking for ? : ")
site = ["https://www.emag.ro/"]


def site_searcher(site, keyword):
    try:
        response = requests.get(site)
        print(response)

        if response.status_code == 200:

            soup = BeautifulSoup(response.text, 'html.parser')

            title_elements = soup.select("h2.card-v2-title-wrapper")

            print(f"Results for the keyword '{keyword}' on {site}:")

            wb = openpyxl.Workbook()
            ex_res = wb.active

            ex_res.append(["Title"])

            for titles in title_elements:
                title = titles.text.strip()
                ex_res.append([title])

            excel = "results1.xlsx"
            wb.save(excel)

            print(f"Results have been saved to {excel}")

    except requests.exceptions.RequestException as exceptions:
        print(f"Network Error: {exceptions}")


for site_url in site:
    site_searcher(site_url, keyword)
