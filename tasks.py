import streamlit as st
import pandas as pd

# List of companies and their websites
companies_data = [
    {"Company Name": "Pfizer", "Website": "https://www.pfizer.com", "Dosage Forms": ["Tablet", "Capsule"], "Health Segments": ["Cognitive Health", "Women's Health"]},
    {"Company Name": "Abbott", "Website": "https://www.abbott.com", "Dosage Forms": ["Oral Suspension", "Capsule"], "Health Segments": ["Gut Health", "Mental Wellness"]},
    {"Company Name": "GSK", "Website": "https://www.gsk.com", "Dosage Forms": ["Tablet", "Sachet"], "Health Segments": ["Cognitive Health", "Gut Health"]},
    {"Company Name": "Nestle", "Website": "https://www.nestle.com", "Dosage Forms": ["Powder", "Liquid"], "Health Segments": ["Women's Health", "Sports Nutrition"]},
    {"Company Name": "CocaCola", "Website": "https://www.coca-cola.com", "Dosage Forms": ["Beverage"], "Health Segments": []},
    {"Company Name": "Pepsi", "Website": "https://www.pepsi.com", "Dosage Forms": ["Beverage"], "Health Segments": []},
    {"Company Name": "Vital Proteins", "Website": "https://www.vitalproteins.com", "Dosage Forms": ["Powder", "Sachet"], "Health Segments": ["Gut Health", "Sports Nutrition"]},
    {"Company Name": "Orgain", "Website": "https://www.orgain.com", "Dosage Forms": ["Powder", "Sachet"], "Health Segments": ["Gut Health", "Women's Health"]},
    # Add more companies as needed
]

# Function to categorize the company based on user input
def categorize_company_by_input(company_name, keywords, dosage_form, health_segments, raw_material_check):
    # Convert inputs to lowercase
    keywords = keywords.lower()
    dosage_form = dosage_form.lower()
    health_segments = health_segments.lower()
    
    # Find the company that matches the company name
    for company in companies_data:
        if company_name.lower() in company["Company Name"].lower():
            website = company["Website"]
            
            # Check relevance based on the keywords and health segments
            relevance = "Relevant"
            category = "Not Relevant"
            
            # Check for F&B-related keywords
            if "fnb" in keywords:
                if any(x in company["Dosage Forms"] for x in ["beverage", "milk", "cereal"]):
                    category = "F&B"
            
            # Check for dosage form keywords
            elif dosage_form in company["Dosage Forms"]:
                category = "Formulations"
            
            # Check for health segment keywords
            elif health_segments in [segment.lower() for segment in company["Health Segments"]]:
                category = "Formulations"
            
            # Check for raw material distributors
            elif raw_material_check:
                relevance = "Not Relevant"
                category = "Not Relevant"
            
            return {
                "Company Name": company["Company Name"],
                "Website": website,
                "Relevance": relevance,
                "Category": category
            }
    
    # If no matching company is found
    return {"Company Name": "Not Found", "Website": "", "Relevance": "Not Found", "Category": "Not Found"}

# Streamlit App
def main():
    st.title("UBL Company Classification Tool")
    st.write("Input the company name or keyword to check relevance and categorization.")

    # Input fields for the user to provide data
    company_name = st.text_input("Enter Company Name or Keywords (e.g., F&B, Dosage Forms, Health Segments)", "")
    keywords = st.text_input("Enter Keywords (e.g., fnb, raw materials, etc.)", "")
    dosage_form = st.text_input("Enter Dosage Form (e.g., Tablet, Capsule, Sachet, Oral Suspension)", "")
    health_segments = st.text_input("Enter Health Segments (e.g., Women's Health, Gut Health, Cognitive Health)", "")
    raw_material_check = st.checkbox("Check if the company is into raw materials (for Not Relevant category)")

    # If the user submits the input
    if company_name:
        result = categorize_company_by_input(company_name, keywords, dosage_form, health_segments, raw_material_check)
        
        # Display the result
        st.write(f"### Results for {company_name}:")
        st.write(f"**Website**: {result['Website']}")
        st.write(f"**Relevance**: {result['Relevance']}")
        st.write(f"**Category**: {result['Category']}")

if __name__ == "__main__":
    main()
