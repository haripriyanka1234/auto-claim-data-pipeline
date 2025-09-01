import re

import pandas as pd

import streamlit as st

from PyPDF2 import PdfReader

from io import BytesIO
 
st.title("📑 Insurance Claim Form Extractor")
 
uploaded_file = st.file_uploader("Upload PDF", type="pdf")
 
if uploaded_file is not None:

    reader = PdfReader(uploaded_file)

    all_text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
 
    forms = all_text.split("Insurance Claim Form")

    data = []
 
    patterns = {

        "Claim ID": r"Claim ID\s+([A-Z0-9]+)",

        "Policy Number": r"Policy Number\s+([A-Z0-9]+)",

        "Claimant Name": r"Claimant Name\s+([\w\s]+)",

        "Date of Birth": r"Date of Birth\s+([\d/]+)",

        "Contact Number": r"Contact Number\s+([+\d-]+)",

        "Email": r"Email\s+(\S+@\S+)",

        "Address": r"Address\s+(.+)",

        "Date of Incident": r"Date of Incident\s+([\d/]+)",

        "Type of Claim": r"Type of Claim\s+(\w+)",

        "Claim Amount (INR)": r"Claim Amount \(INR\)\s+(\d+)",

        "Hospital/Repair Shop": r"Hospital/Repair Shop\s+([\w\s]+)",

        "Incident Description": r"Incident Description\s+(.+)",

        "Bank Name": r"Bank Name\s+([\w\s]+)",

        "Account Holder Name": r"Account Holder Name\s+([\w\s]+)",

        "Account Number": r"Account Number\s+(\d+)",

        "IFSC Code": r"IFSC Code\s+([A-Z0-9]+)"

    }
 
    for form in forms:

        form_data = {}

        for field, pattern in patterns.items():

            match = re.search(pattern, form)

            form_data[field] = match.group(1).strip() if match else None

        if form_data.get("Claim ID"):

            data.append(form_data)
 
    df = pd.DataFrame(data)

    st.dataframe(df)
 
    # Write to Excel in memory

    buffer = BytesIO()

    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:

        df.to_excel(writer, index=False)

    buffer.seek(0)
 
    st.download_button("Download as Excel",

                       data=buffer,

                       file_name="insurance_claims.xlsx",

                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

 