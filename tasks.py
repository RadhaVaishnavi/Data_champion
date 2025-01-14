import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Preloaded company data
companies_data = [
    {"Company Name": "Nestle", "Website": "https://www.nestle.com"},
    {"Company Name": "Pfizer", "Website": "https://www.pfizer.com"},
    {"Company Name": "Coca-Cola", "Website": "https://www.coca-colacompany.com"},
    {"Company Name": "PepsiCo", "Website": "https://www.pepsico.com"},
    {"Company Name": "Unilever", "Website": "https://www.unilever.com"},
]

# Convert data to DataFrame
df = pd.DataFrame(companies_data)

# Function to scrape the description from a website using Selenium
def scrape_website_description(url):
    try:
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run headlessly (no UI)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("window-size=1200x600")  # Set window size

        # Set up WebDriver with ChromeDriver Manager
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)
        time.sleep(3)  # Wait for the page to load (may need adjustment)

        # Example: Try to scrape description from <meta name="description"> or similar
        description_element = driver.find_element(By.XPATH, "//meta[@name='description']")
        description = description_element.get_attribute("content") if description_element else "No description available."
        
        driver.quit()  # Close the browser after scraping
        return description
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit app title
st.title("Company Classification Tool with Web Scraping")

# Search bar
search_query = st.text_input("Search for a company by name:", "")

# Show the data if there's a search query
if search_query:
    # Filter the DataFrame based on search query
    filtered_data = df[df["Company Name"].str.contains(search_query, case=False, na=False)]

    if not filtered_data.empty:
        for _, row in filtered_data.iterrows():
            st.write(f"**Company Name:** {row['Company Name']}")
            st.write(f"**Website:** {row['Website']}")

            # Scrape the website for description
            with st.spinner("Scraping website for description..."):
                description = scrape_website_description(row["Website"])
            st.write(f"**Description:** {description}")
    else:
        st.warning("No company found with that name.")
else:
    st.info("Enter a company name in the search bar to see its details.")

# import streamlit as st
# import pandas as pd
# import requests
# from bs4 import BeautifulSoup

# # Predefined dataset
# data = pd.DataFrame({
#     "Company Name": [
#         "Nestle", "Dr. Reddy's Laboratories", "Coca", "Pfizer", "PepsiCo", 
#         "Johnson & Johnson", "Danone", "Bayer", "General Mills", "GlaxoSmithKline (GSK)"
#     ],
#     "Website": [
#         "https://www.nestle.com", "https://www.drreddys.com", "https://www.coca.com", 
#         "https://www.pfizer.com", "https://www.pepsico.com", "https://www.jnj.com", 
#         "https://www.danone.com", "https://www.bayer.com", "https://www.generalmills.com", 
#         "https://www.gsk.com"
#     ]
# })

# # Web scraping function
# def scrape_website(url):
#     try:
#         response = requests.get(url, timeout=5)
#         print(response)
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.content, 'html.parser')
            
#             # Extract meta description or title
#             meta_desc = soup.find("meta", attrs={"name": "description"})
#             if meta_desc:
#                 return meta_desc["content"]
            
#             title = soup.title.string if soup.title else "No title available"
#             return title
#         else:
#             return f"Failed to access: {response.status_code}"
#     except Exception as e:
#         return f"Error: {str(e)}"

# # Streamlit UI
# st.title("Company Classification Tool with Web Scraping")

# # Display predefined dataset
# st.write("Preloaded Company Data:")
# st.dataframe(data)

# # Scraping and updating the dataset
# st.write("Scraping websites for descriptions...")
# scraped_data = []
# for _, row in data.iterrows():
#     website = row["Website"]
#     company_name = row["Company Name"]
#     description = scrape_website(website)
#     scraped_data.append({"Company Name": company_name, "Website": website, "Description": description})

# # Convert to DataFrame and display
# scraped_df = pd.DataFrame(scraped_data)
# st.write("Scraped Data:")
# st.dataframe(scraped_df)

# # Option to download scraped data
# st.download_button(
#     label="Download Scraped Data",
#     data=scraped_df.to_csv(index=False),
#     file_name="scraped_data.csv",
#     mime="text/csv",
# )
