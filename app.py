import streamlit as st
import pandas as pd

# Set the page configuration
st.set_page_config(page_title="Weekly Product Finder", layout="centered")

# Title and description
st.title("🛍️ AI-Powered Product Research Tool")
st.markdown("""
Welcome to your beginner-friendly tool that highlights the best products to sell every week on:
- Amazon
- eBay
- Etsy

This version uses sample data and is ready for future upgrades with real-time APIs or scraping.
""")

# Platform selection
platform = st.selectbox("Select Platform", ["Amazon", "eBay", "Etsy"])

# Sample static dataset (you'll replace this with real data or API integration later)
sample_data = {
    "Product": [
        "LED Strip Light", "Bluetooth Earbuds", "Reusable Notepad",
        "Vintage T-shirt", "Handmade Earrings", "Wireless Charger",
        "Wall Art Print", "Organic Lip Balm", "Custom Mug"
    ],
    "Platform": [
        "Amazon", "Amazon", "Amazon",
        "eBay", "eBay", "eBay",
        "Etsy", "Etsy", "Etsy"
    ],
    "Price": [19.99, 25.49, 14.99, 12.49, 18.75, 21.95, 15.00, 9.50, 11.99],
    "Rating": [4.5, 4.2, 4.7, 4.3, 4.8, 4.4, 4.6, 4.9, 4.7],
    "Sales": [1200, 950, 870, 780, 1050, 980, 890, 1100, 1025]
}

# Load into a DataFrame
df = pd.DataFrame(sample_data)

# Filter products for selected platform
filtered_df = df[df["Platform"] == platform]

# Sort by Sales to find top product
top_product = filtered_df.sort_values("Sales", ascending=False).head(1)

# Display top product
st.subheader(f"🔥 Top Product This Week on {platform}")
st.success(f"**{top_product['Product'].values[0]}** — ${top_product['Price'].values[0]} | ⭐ {top_product['Rating'].values[0]} | 🛒 {top_product['Sales'].values[0]} sales")

# Display full list
st.markdown("### 🗂️ All Products on This Platform")
st.dataframe(filtered_df.reset_index(drop=True))

# Footer
st.markdown("""
---
👶 Built for beginners | Future versions will use live APIs & trend prediction.
""")
