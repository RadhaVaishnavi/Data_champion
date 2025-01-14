import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Predefined dataset
data = pd.DataFrame({
    "Company Name": [
        "Nestle", "Dr. Reddy's Laboratories", "Coca", "Pfizer", "PepsiCo", 
        "Johnson & Johnson", "Danone", "Bayer", "General Mills", "GlaxoSmithKline (GSK)"
    ],
    "Website": [
        "https://www.nestle.com", "https://www.drreddys.com", "https://www.coca.com", 
        "https://www.pfizer.com", "https://www.pepsico.com", "https://www.jnj.com", 
        "https://www.danone.com", "https://www.bayer.com", "https://www.generalmills.com", 
        "https://www.gsk.com"
    ]
})

# Web scraping function
def scrape_website(url):
    try:
        response = requests.get(url, timeout=5)
        print(response)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract meta description or title
            meta_desc = soup.find("meta", attrs={"name": "description"})
            if meta_desc:
                return meta_desc["content"]
            
            title = soup.title.string if soup.title else "No title available"
            return title
        else:
            return f"Failed to access: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.title("Company Classification Tool with Web Scraping")

# Display predefined dataset
st.write("Preloaded Company Data:")
st.dataframe(data)

# Scraping and updating the dataset
st.write("Scraping websites for descriptions...")
scraped_data = []
for _, row in data.iterrows():
    website = row["Website"]
    company_name = row["Company Name"]
    description = scrape_website(website)
    scraped_data.append({"Company Name": company_name, "Website": website, "Description": description})

# Convert to DataFrame and display
scraped_df = pd.DataFrame(scraped_data)
st.write("Scraped Data:")
st.dataframe(scraped_df)

# Option to download scraped data
st.download_button(
    label="Download Scraped Data",
    data=scraped_df.to_csv(index=False),
    file_name="scraped_data.csv",
    mime="text/csv",
)
