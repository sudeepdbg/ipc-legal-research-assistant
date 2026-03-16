import pandas as pd
import os

# ------------------------------------------------------------
# 1. Load IPC sections from ipc_sections.csv
# ------------------------------------------------------------
def load_ipc_sections(csv_path="data/ipc_sections.csv"):
    df = pd.read_csv(csv_path)
    chunks = []
    metadatas = []
    for _, row in df.iterrows():
        # Combine fields into a single text block
        text = f"Section: {row['Section']}\nOffense: {row['Offense']}\nDescription: {row['Description']}\nPunishment: {row['Punishment']}"
        chunks.append(text)
        metadatas.append({
            "section": row['Section'],
            "offense": row['Offense'],
            "source": "IPC"
        })
    return chunks, metadatas

# ------------------------------------------------------------
# 2. Load judgments from judgments.csv (bail case data)
# ------------------------------------------------------------
def load_judgments_csv(csv_path="data/judgments.csv"):
    """
    Reads the bail judgments CSV and creates one text chunk per judgment.
    Adjust the column names if your CSV differs.
    """
    df = pd.read_csv(csv_path)
    chunks = []
    metadatas = []
    for _, row in df.iterrows():
        # Build a rich text block from key columns
        text = f"Case Title: {row['case_title']}\n"
        text += f"Court: {row['court']}\n"
        text += f"Date: {row['date']}\n"
        text += f"Judge(s): {row['judge']}\n"
        text += f"IPC Sections: {row['ipc_sections']}\n"
        text += f"Bail Type: {row['bail_type']}\n"
        text += f"Bail Outcome: {row['bail_outcome']}\n"
        text += f"Crime Type: {row['crime_type']}\n"
        text += f"Facts: {row['facts']}\n"
        text += f"Legal Issues: {row['legal_issues']}\n"
        text += f"Judgment Reason: {row['judgment_reason']}\n"
        text += f"Summary: {row['summary']}\n"
        text += f"Legal Principles Discussed: {row['legal_principles_discussed']}\n"
        text += f"Special Laws: {row['special_laws']}\n"

        chunks.append(text)

        # Metadata for filtering
        metadatas.append({
            "source": "bail_judgment",
            "case_id": row['case_id'],
            "court": row['court'],
            "year": str(row['date'])[:4] if pd.notna(row['date']) else "",
            "crime_type": row['crime_type'],
            "bail_outcome": row['bail_outcome']
        })
    return chunks, metadatas

# ------------------------------------------------------------
# 3. Load NCRB statistics from ncrb_data.csv
# ------------------------------------------------------------
def load_ncrb_data(csv_path="data/ncrb_data.csv"):
    """
    Reads the NCRB conviction/pendency CSV and creates one text chunk per state/UT.
    """
    df = pd.read_csv(csv_path)
    chunks = []
    metadatas = []
    for _, row in df.iterrows():
        state = row['State/UT']
        # Skip summary rows like "Total State (S)", "Total All India"
        if state in ['Total State (S)', 'Total UT (S)', 'Total All India']:
            continue

        text = f"State/UT: {state}\n"
        text += f"Cases pending trial from previous year: {row['Cases Pending Trial from the Previous Year - ( Col. 3)']}\n"
        text += f"Cases sent for trial during the year: {row['Cases Sent for Trial during the year - ( Col. 4)']}\n"
        text += f"Conviction rate: {row['Conviction Rate (Col.21)']}%\n"
        text += f"Pendency percentage: {row['Pendency Percentage (Col.22)']}%\n"
        # You can add more columns if needed

        chunks.append(text)
        metadatas.append({
            "state": state,
            "source": "NCRB"
        })
    return chunks, metadatas
