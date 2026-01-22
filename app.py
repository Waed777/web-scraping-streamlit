import streamlit as st
import pandas as pd
from scraper import scrape_books

st.set_page_config(page_title="Web Scraping App", layout="centered")

st.title("🕷️ Web Scraping Demo App")

st.write("Click the button below to scrape book data.")

if st.button("Start Scraping"):
    data = scrape_books()
    df = pd.DataFrame(data)

    st.success("Data scraped successfully!")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download CSV",
        csv,
        "books_data.csv",
        "text/csv"
    )
