import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

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

# Function to scrape the description from a website
def scrape_website_description(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Example: Extract meta description or a specific tag content
        description = soup.find("meta", attrs={"name": "description"})
        if description and description.get("content"):
            return description["content"]
        return "No description available."
    except requests.exceptions.HTTPError as e:
        return f"Error: HTTP Error {e.response.status_code} for URL {url}"
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
