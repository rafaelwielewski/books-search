import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import uuid

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
IMAGE_PREFIX = "https://books.toscrape.com/"
OUTPUT_FILE = "data/books.csv"

def rating_to_int(rating_str):
    mapping = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    return mapping.get(rating_str, 0)

def extract_book_data(article, category="Unknown"):
    title = article.h3.a["title"]
    price = float(article.select_one(".price_color").text[2:])
    rating = rating_to_int(article.p["class"][1])
    availability = article.select_one(".availability").text.strip()
    img_url = IMAGE_PREFIX + article.img["src"].replace("../", "")
    return {
        "id": str(uuid.uuid4()),
        "title": title,
        "price": price,
        "rating": rating,
        "availability": availability,
        "category": category,
        "image": img_url
    }

def get_categories():
    url = "https://books.toscrape.com/index.html"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    category_links = soup.select(".side_categories ul li ul li a")
    categories = {link["href"]: link.text.strip() for link in category_links}
    return categories

def scrape() -> str:
    books = []
    categories = get_categories()

    for rel_url, category_name in categories.items():
        page = 1
        while True:
            if page == 1:
                page_url = IMAGE_PREFIX + rel_url
            else:
                page_url = IMAGE_PREFIX + rel_url.replace("index.html", f"page-{page}.html")

            res = requests.get(page_url)
            if res.status_code != 200:
                break

            soup = BeautifulSoup(res.text, "html.parser")
            articles = soup.select("article.product_pod")
            if not articles:
                break

            for article in articles:
                book = extract_book_data(article, category=category_name)
                books.append(book)

            page += 1
            time.sleep(0.2)

    df = pd.DataFrame(books)
    os.makedirs("data", exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ {len(df)} livros salvos em {OUTPUT_FILE}")
    return "Scraping concluído com sucesso!"

if __name__ == "__main__":
    scrape()