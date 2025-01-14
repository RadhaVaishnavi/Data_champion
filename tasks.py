import streamlit as st
import pandas as pd

# Predefined dataset
data = pd.DataFrame({
    "Company Name": [
        "Nestle", "Dr. Reddy's Laboratories", "Coca", "Pfizer", "PepsiCo", 
        "Johnson & Johnson", "Danone", "Bayer", "General Mills", "GlaxoSmithKline (GSK)", 
        "Kellogg’s", "Merck & Co.", "Unilever", "Roche", "Nestle Waters", 
        "Sanofi", "Mondelez International", "Novartis", "Kraft Heinz", "Eli Lilly and Company", 
        "Tyson Foods", "Teva Pharmaceuticals", "Mars, Incorporated", "AbbVie", "Campbell Soup Company", 
        "Amgen", "Conagra Brands", "AstraZeneca", "Molson Coors", "Boehringer Ingelheim", 
        "AB InBev", "BASF", "Diageo", "Procter & Gamble (P&G)", "Heineken", 
        "Medtronic", "McKesson", "AmerisourceBergen", "Cardinal Health", "Medline Industries"
    ],
    "Website": [
        "www.nestle.com", "www.drreddys.com", "colacompany.com", "www.pfizer.com", "www.pepsico.com",
        "www.jnj.com", "www.danone.com", "www.bayer.com", "www.generalmills.com", "www.gsk.com",
        "www.kelloggs.com", "www.merck.com", "www.unilever.com", "www.roche.com", "www.nestlewaters.com",
        "www.sanofi.com", "www.mondelezinternational.com", "www.novartis.com", "www.kraftheinzcompany.com", "www.lilly.com",
        "www.tysonfoods.com", "www.tevapharm.com", "www.mars.com", "www.abbvie.com", "www.campbellsoupcompany.com",
        "www.amgen.com", "www.conagrabrands.com", "www.astrazeneca.com", "www.molsoncoors.com", "www.boehringeringelheim.com",
        "www.abinbev.com", "www.basf.com", "www.diageo.com", "www.pg.com", "www.theheinekencompany.com",
        "www.medtronic.com", "www.mckesson.com", "www.amerisourcebergen.com", "www.cardinalhealth.com", "www.medline.com"
    ]
})

# Add empty columns for processing
data["Relevant"] = "Unknown"
data["Category"] = "Unknown"
data["F&B"] = "No"
data["Manufacturer"] = "No"
data["Distributor"] = "No"
data["Gut Health"] = "No"
data["Women’s Health"] = "No"
data["Cognitive Health"] = "No"

# Function to classify companies based on sample rules
def classify_company(data):
    for index, row in data.iterrows():
        # Determine category
        if "food" in row["Company Name"].lower() or "beverage" in row["Company Name"].lower():
            row["Category"] = "F&B"
        elif "pharma" in row["Company Name"].lower() or "lab" in row["Company Name"].lower():
            row["Category"] = "Bulk (Manufacturer)"
        elif "distribution" in row["Company Name"].lower() or "brands" in row["Company Name"].lower():
            row["Category"] = "Bulk (Distributor)"
        else:
            row["Category"] = "Not Relevant"
        
        # Set relevance (example logic, can be extended)
        if "health" in row["Company Name"].lower():
            row["Relevant"] = "Yes"
        else:
            row["Relevant"] = "No"
    return data

# Streamlit UI
st.title("Company Classification Tool for Unique BioTech")

# Display predefined dataset
st.write("Preloaded Company Data:")
st.dataframe(data)

# Process and classify data
st.write("Classifying companies...")
processed_data = classify_company(data)
st.write("Classified Data:")
st.dataframe(processed_data)

# Option to download processed data
st.download_button(
    label="Download Classified Data",
    data=processed_data.to_csv(index=False),
    file_name="classified_data.csv",
    mime="text/csv",
)

# Manual entry form
st.header("Add a Company Manually")
with st.form("manual_entry"):
    company_name = st.text_input("Company Name")
    website = st.text_input("Website")
    f_and_b = st.radio("F&B?", ["Yes", "No"])
    manufacturer = st.radio("Manufacturer?", ["Yes", "No"])
    distributor = st.radio("Distributor?", ["Yes", "No"])
    gut_health = st.radio("Gut Health?", ["Yes", "No"])
    womens_health = st.radio("Women’s Health?", ["Yes", "No"])
    cognitive_health = st.radio("Cognitive Health?", ["Yes", "No"])
    submitted = st.form_submit_button("Add Company")

    if submitted:
        new_data = pd.DataFrame(
            [[company_name, website, "No", "", manufacturer, distributor, f_and_b, "No", "No", gut_health, womens_health, cognitive_health]],
            columns=["Company Name", "Website", "Relevant", "Category", "Manufacturer", "Distributor", "F&B", "Probiotics", "Fortification", "Gut Health", "Women’s Health", "Cognitive Health"]
        )
        st.write("New Company Data:")
        st.dataframe(new_data)

        processed_data = pd.concat([processed_data, new_data], ignore_index=True)
        st.write("Updated Data:")
        st.dataframe(processed_data)
