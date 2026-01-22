# في scraper.py
import requests
from bs4 import BeautifulSoup

def scrape_books(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    books = []
    for item in soup.find_all("article", class_="product_pod"):
        title = item.h3.a.attrs.get("title")
        price = item.select_one("p.price_color").text
        availability = item.select_one("p.availability").text.strip()
        books.append({
            "Title": title,
            "Price": price,
            "Availability": availability
        })
    return books

