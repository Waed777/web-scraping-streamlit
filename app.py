import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

st.set_page_config(page_title="Powerful Web Scraping App", layout="centered")
st.title("🕷️ Powerful Web Scraping App")
st.write("Enter any website URL with books or products to scrape:")

url = st.text_input("Website URL", "https://books.toscrape.com/")

if st.button("Start Scraping"):
    if url:
        try:
            books = []

            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url)
                html = page.content()
                browser.close()

            soup = BeautifulSoup(html, "html.parser")

            # محاولة ذكية لاكتشاف الكتب/المنتجات
            for item in soup.find_all(["article", "div"]):
                title_tag = item.find(["h3", "h2", "h1", "span", "a"])
                price_tag = item.find(["p", "span"], text=lambda x: x and "£" in x)
                availability_tag = item.find(["p", "span"], text=lambda x: x and ("In stock" in x or "available" in x))

                if title_tag:
                    books.append({
                        "Title": title_tag.get_text(strip=True) if title_tag else "N/A",
                        "Price": price_tag.get_text(strip=True) if price_tag else "N/A",
                        "Availability": availability_tag.get_text(strip=True) if availability_tag else "N/A"
                    })

            df = pd.DataFrame(books)

            if df.empty:
                st.warning("No books or products found. The website structure might be too different.")
            else:
                st.success(f"Scraped {len(df)} items successfully!")
                st.dataframe(df)

                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "Download CSV",
                    csv,
                    "scraped_data.csv",
                    "text/csv"
                )

        except Exception as e:
            st.error(f"Error scraping data: {e}")
    else:
        st.warning("Please enter a valid URL.")
