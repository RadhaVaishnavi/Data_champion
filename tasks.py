import requests
from bs4 import BeautifulSoup

# Function to fetch company information by searching for it on Google
def get_company_info(company_name):
    # Google search URL to find the company
    search_url = f"https://www.google.com/search?q={company_name}"
    
    # Custom headers to mimic a browser request (this avoids being blocked by websites)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # Make a GET request to Google search
    response = requests.get(search_url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the first search result that seems like the official website
        link = soup.find('a', href=True)
        
        if link:
            # The href attribute contains the website URL
            company_url = link['href']
            company_name = company_name.capitalize()
            
            # Make a GET request to the company URL to get more details
            company_page = requests.get(company_url, headers=headers)
            
            if company_page.status_code == 200:
                company_soup = BeautifulSoup(company_page.text, 'html.parser')
                
                # Try to find the description from meta tag (common method)
                meta_description = company_soup.find("meta", attrs={"name": "description"})
                
                if meta_description:
                    description = meta_description.get("content", "No description available.")
                else:
                    description = "No description available."
                
                # Return the information in a dictionary format
                return {
                    'company_name': company_name,
                    'company_url': company_url,
                    'description': description
                }
            else:
                return {
                    'error': f"Failed to retrieve the company page, status code: {company_page.status_code}"
                }
        else:
            return {
                'error': "No link found for the company."
            }
    else:
        return {
            'error': f"Failed to retrieve search results, status code: {response.status_code}"
        }

# Function to display the fetched company info
def display_company_info(company_name):
    company_info = get_company_info(company_name)
    
    if 'error' in company_info:
        print(f"Error: {company_info['error']}")
    else:
        print(f"Company Name: {company_info['company_name']}")
        print(f"Website: {company_info['company_url']}")
        print(f"Description: {company_info['description']}")

# Main function to run the search and display result
if __name__ == "__main__":
    # Input company name to search
    company_name = input("Enter the company name to search: ")
    display_company_info(company_name)


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
