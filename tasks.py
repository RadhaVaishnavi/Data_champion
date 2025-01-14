
import streamlit as st
import pandas as pd

# List of companies and their websites
companies_data = [
    {"Company Name": "Pfizer", "Website": "https://www.pfizer.com"},
    {"Company Name": "Abbott", "Website": "https://www.abbott.com"},
    {"Company Name": "GSK", "Website": "https://www.gsk.com"},
    {"Company Name": "Nestle", "Website": "https://www.nestle.com"},
    {"Company Name": "CocaCola", "Website": "https://www.coca-cola.com"},
    {"Company Name": "Pepsi", "Website": "https://www.pepsi.com"},
    {"Company Name": "Vital Proteins", "Website": "https://www.vitalproteins.com"},
    {"Company Name": "Orgain", "Website": "https://www.orgain.com"},
    # Add more companies as needed
]

# Helper function to categorize companies
def categorize_company(row):
    name = row["Company Name"].lower()
    health_segments = ["gut health", "women's health", "cognitive health", "mental wellness", "sports nutrition"]
    website = row["Website"].lower()
    
    if any(keyword in website for keyword in ["drink", "milk", "cereal", "bakery"]):
        return "F&B"
    elif "manufacturer" in website or any(seg in website for seg in health_segments):
        return "Bulk"
    elif any(keyword in name for keyword in ["pfizer", "abbott", "gsk"]):
        return "Formulations"
    else:
        return "Not Relevant"

# Helper function for conditional formatting
def format_row(row):
    if row["Category"] == "Not Relevant":
        return ["background-color: red"] * len(row)
    return ["background-color: green"] * len(row)

# Streamlit App
def main():
    st.title("UBL Company Classification Tool")
    st.write("This tool classifies companies into F&B, Bulk, Formulations, or Not Relevant based on their names and websites.")
    
    # Convert the company data into a DataFrame
    df = pd.DataFrame(companies_data)
    
    # Classify companies
    df["Category"] = df.apply(categorize_company, axis=1)
    
    # Show the categorized dataframe
    st.write("### Categorized Data")
    st.dataframe(df.style.apply(format_row, axis=1))
    
    # Show a summary of the categorization
    st.write("### Category Summary")
    summary = df["Category"].value_counts().reset_index()
    summary.columns = ["Category", "Count"]
    st.bar_chart(summary.set_index("Category"))

if __name__ == "__main__":
    main()
