import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Web Scraping App", layout="centered")
st.title("🕷️ Web Scraping Dynamic App")
st.write("Enter the URL of the website you want to scrape books from:")

# إدخال الرابط
url = st.text_input("Website URL", "https://books.toscrape.com/")

# زر البداية
if st.button("Start Scraping"):
    if url:
        try:
            # إرسال طلب للموقع
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # استخراج بيانات الكتب - مثال على موقع books.toscrape.com
            books = []
            for book in soup.select("article.product_pod"):
                title = book.h3.a.attrs["title"]
                price = book.select_one("p.price_color").text
                availability = book.select_one("p.availability").text.strip()
                books.append({
                    "Title": title,
                    "Price": price,
                    "Availability": availability
                })

            # تحويل البيانات إلى DataFrame
            df = pd.DataFrame(books)

            st.success("Data scraped successfully!")
            st.dataframe(df)

            # تحميل CSV
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download CSV",
                csv,
                "books_data.csv",
                "text/csv"
            )

        except Exception as e:
            st.error(f"Error scraping data: {e}")
    else:
        st.warning("Please enter a valid URL.")
