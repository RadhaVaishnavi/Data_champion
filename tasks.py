import streamlit as st
import pandas as pd

# Sample list of companies with their details
companies_data = [
    {"Company Name": "Pfizer", "Website": "https://www.pfizer.com", "Dosage Forms": ["Tablet", "Capsule", "Injection"], "Health Segments": ["Cognitive Health", "Mental Wellness"]},
    {"Company Name": "Abbott", "Website": "https://www.abbott.com", "Dosage Forms": ["Sachet", "Oral Suspension", "Tablet"], "Health Segments": ["Gut Health", "Women's Health"]},
    {"Company Name": "GSK", "Website": "https://www.gsk.com", "Dosage Forms": ["Tablet", "Capsule", "Sachet"], "Health Segments": ["Cognitive Health", "Mental Wellness"]},
    {"Company Name": "Nestle", "Website": "https://www.nestle.com", "Dosage Forms": [], "Health Segments": []},
    {"Company Name": "CocaCola", "Website": "https://www.coca-cola.com", "Dosage Forms": [], "Health Segments": []},
    {"Company Name": "Pepsi", "Website": "https://www.pepsi.com", "Dosage Forms": [], "Health Segments": []},
    {"Company Name": "Vital Proteins", "Website": "https://www.vitalproteins.com", "Dosage Forms": ["Capsule", "Sachet"], "Health Segments": ["Gut Health"]},
    {"Company Name": "Orgain", "Website": "https://www.orgain.com", "Dosage Forms": ["Sachet", "Powder"], "Health Segments": ["Women's Health"]},
    # Add more companies as needed
]

# Helper function to classify the company based on input keyword
def categorize_company_by_input(keyword):
    health_segments = ["gut health", "women's health", "cognitive health", "mental wellness", "sports nutrition"]
    fnb_keywords = ["beverage", "cereal", "milk", "bakery"]
    
    relevant_companies = []
    for company in companies_data:
        # Search for the keyword in company name or associated product categories
        if keyword.lower() in company["Company Name"].lower() or any(k in company["Company Name"].lower() for k in fnb_keywords):
            # Check if the company is relevant based on dosage forms and health segments
            if "raw materials" in company["Website"].lower():
                relevance = "Not Relevant"
                category = "Not Relevant"
            else:
                # Categorize based on dosage forms and health segments
                if any(df in company["Dosage Forms"] for df in ["Oral Suspension", "Capsule", "Tablet", "Sachet"]):
                    if any(segment in company["Health Segments"] for segment in health_segments):
                        relevance = "Relevant"
                        category = "Formulations"
                    else:
                        relevance = "Relevant"
                        category = "Bulk"
                else:
                    relevance = "Not Relevant"
                    category = "Not Relevant"
                
            relevant_companies.append({
                "Company Name": company["Company Name"],
                "Website": company["Website"],
                "Dosage Forms": ", ".join(company["Dosage Forms"]) if company["Dosage Forms"] else "None",
                "Health Segments": ", ".join(company["Health Segments"]) if company["Health Segments"] else "None",
                "Relevance": relevance,
                "Category": category
            })
    
    return relevant_companies

# Streamlit App
def main():
    st.title("UBL Company Search Tool")
    st.write("Search for a company name or keyword (e.g., F&B) to get relevant company details and category classification.")
    
    # Input: Company name or keyword
    keyword = st.text_input("Enter Company Name or Keyword:", "")
    
    if keyword:
        # Get companies that match the input
        relevant_companies = categorize_company_by_input(keyword)
        
        if relevant_companies:
            # Convert to DataFrame for easy display
            df = pd.DataFrame(relevant_companies)
            
            # Display results in a table
            st.write("### Search Results")
            st.dataframe(df)
        else:
            st.write("No companies found matching the given keyword.")
    
if __name__ == "__main__":
    main()
