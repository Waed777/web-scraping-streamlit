import streamlit as st
import pandas as pd
from scraper import scrape_books

st.set_page_config(page_title="Web Scraping App", layout="centered")
st.title("🕷️ Web Scraping Dynamic Scraper App")
st.write("Enter the URL of the website you want to scrape:")

url = st.text_input("Website URL", "https://example.com/books")

if st.button("Start Scraping"):
    if url:
        try:
            with st.spinner("Scraping data... ⏳"):
                data = scrape_books(url)
            
            if not data:
                st.warning("No data found at the provided URL.")
            else:
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
        except Exception as e:
            st.error("Error scraping data.")
            st.text(str(e))
    else:
        st.warning("Please enter a valid URL.")
