import requests
import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup
from datetime import datetime

TRENDING_URL = 'https://www.etsy.com/c/trending-items'

def fetch_trending_products():
    try:
        response = requests.get(TRENDING_URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, 'html.parser')
    product_list = []

    for item in soup.select('li.wt-list-unstyled.wt-grid__item-xs-6'):
        try:
            title_tag = item.select_one('h3')
            url_tag = item.select_one('a')
            price_tag = item.select_one('span.currency-value')
            image_tag = item.select_one('img')

            if not title_tag or not url_tag or not image_tag:
                continue

            title = title_tag.get_text(strip=True)
            url = url_tag['href']
            price = float(price_tag.text.strip()) if price_tag else None
            image = image_tag.get('src', '')

            product_list.append({
                'Title': title,
                'URL': url,
                'Price (USD)': price,
                'Image': image,
                'Scrape Time': datetime.utcnow()
            })
        except Exception:
            continue

    return pd.DataFrame(product_list)

st.set_page_config(page_title="Etsy Product Trend Finder", layout="wide")
st.title("🧵 Etsy Weekly Product Trend Finder")

st.markdown("""
This tool highlights trending products on **Etsy** to help you discover what to sell. Updated weekly.

Browse the list below or download for offline use.
""")

if st.button("🔄 Refresh Trending List"):
    df = fetch_trending_products()
    st.session_state['df'] = df
    st.success("Data refreshed!")

if 'df' not in st.session_state:
    st.session_state['df'] = fetch_trending_products()

df = st.session_state['df']
if not df.empty:
    for _, row in df.iterrows():
        with st.container():
            st.markdown(f"### [{row['Title']}]({row['URL']})")
            cols = st.columns([2, 1])
            if row['Image']:
                cols[0].image(row['Image'], use_column_width=True)
            if row['Price (USD)'] is not None:
                cols[1].write(f"**Price:** ${row['Price (USD)']:.2f}")
            cols[1].write(f"[View on Etsy]({row['URL']})")
else:
    st.warning("No data found. Please refresh.")

st.download_button(
    label="📥 Download Product List as CSV",
    data=df.to_csv(index=False),
    file_name="etsy_trending_products.csv",
    mime="text/csv"
)

st.caption("Last updated: " + datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"))
