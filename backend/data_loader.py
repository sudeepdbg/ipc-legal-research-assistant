import pandas as pd
import os

# ------------------------------------------------------------
# 1. Load IPC sections from ipc_sections.csv
# ------------------------------------------------------------
def load_ipc_sections(csv_path="data/ipc_sections.csv"):
    """
    Reads IPC sections CSV.
    Expected columns: Description, Offense, Punishment, Section
    """
    df = pd.read_csv(csv_path)
    chunks = []
    metadatas = []
    for _, row in df.iterrows():
        text = f"Section: {row['Section']}\nOffense: {row['Offense']}\nDescription: {row['Description']}\nPunishment: {row['Punishment']}"
        chunks.append(text)
        metadatas.append({
            "section": row['Section'],
            "offense": row['Offense'],
            "source": "IPC"
        })
    return chunks, metadatas

# ------------------------------------------------------------
# 2. Load NCRB statistics from ncrb_data.csv
# ------------------------------------------------------------
def load_ncrb_data(csv_path="data/ncrb_data.csv"):
    """
    Reads NCRB conviction/pendency CSV.
    Column names are taken exactly from the provided file.
    """
    df = pd.read_csv(csv_path)
    chunks = []
    metadatas = []
    for _, row in df.iterrows():
        state = row['State/UT']
        # Skip summary rows like "Total State (S)" and "Total All India"
        if state in ['Total State (S)', 'Total UT (S)', 'Total All India']:
            continue

        text = f"State/UT: {state}\n"
        text += f"Cases pending trial from previous year: {row['Cases Pending Trial from the Previous Year - ( Col. 3)']}\n"
        text += f"Cases sent for trial during the year: {row['Cases Sent for Trial during the year - ( Col. 4)']}\n"
        text += f"Total cases for trial: {row['Total Cases for Trial (Col.3+Col.4) - ( Col. 5)']}\n"
        text += f"Cases abated: {row['Cases Abated by Court - ( Col. 6)']}\n"
        text += f"Cases withdrawn: {row['Cases Withdrawn from Prosecution - ( Col. 7)']}\n"
        text += f"Cases compounded or compromised: {row['Cases Compounded or Compromised - ( Col. 8)']}\n"
        text += f"Cases disposed by plea bargaining: {row['Cases Disposed off by Plea Bargaining - ( Col. 9)']}\n"
        text += f"Cases quashed: {row['Cases Quashed - ( Col. 10)']}\n"
        text += f"Cases disposed without trial: {row['Cases Disposed off without trial (Col.6+Col.7+Col.8+Col.9+Col.10) - ( Col. 11)']}\n"
        text += f"Cases stayed or sent to record room: {row['Cases Stayed or Sent to Record Room - ( Col. 12)']}\n"
        text += f"Cases convicted from previous year: {row['Cases Convicted Out of Cases from Previous Year - ( Col. 13)']}\n"
        text += f"Cases convicted from cases during year: {row['Cases Convicted Out of Cases during the Year - ( Col. 14)']}\n"
        text += f"Total convicted: {row['Cases Convicted (Col.13+Col.14) - ( Col. 15)']}\n"
        text += f"Cases discharged: {row['Cases Discharged - ( Col. 16)']}\n"
        text += f"Cases acquitted: {row['Cases Acquitted - ( Col. 17)']}\n"
        text += f"Trials completed: {row['Cases in which Trials were Completed (Col.15+Col.16+ Col.17) - ( Col. 18)']}\n"
        text += f"Conviction rate: {row['Conviction Rate (Col.15/Col.18) *100 - ( Col. 21)']}%\n"
        text += f"Pendency percentage: {row['Pendency Percentage (Col.20/Col.5)*100 - ( Col. 22)']}%\n"

        chunks.append(text)
        metadatas.append({
            "state": state,
            "source": "NCRB"
        })
    return chunks, metadatas

# ------------------------------------------------------------
# 3. Load judgments from judgments.csv (bail case data)
# ------------------------------------------------------------
def load_judgments_csv(csv_path="data/judgments.csv"):
    """
    Reads the bail judgments CSV.
    Expected columns based on earlier conversations:
        case_id, case_title, court, date, judge, ipc_sections, bail_type,
        bail_cancellation_case, landmark_case, accused_name, accused_gender,
        prior_cases, bail_outcome, bail_outcome_label_detailed, crime_type,
        facts, legal_issues, judgment_reason, summary, bias_flag,
        parity_argument_used, legal_principles_discussed, region,
        source_filename, special_laws
    If some columns are missing, they are skipped.
    """
    df = pd.read_csv(csv_path)
    chunks = []
    metadatas = []
    for _, row in df.iterrows():
        # Build a rich text block from all available columns
        text_parts = []
        for col in df.columns:
            val = row[col]
            if pd.notna(val) and str(val).strip() != '':
                text_parts.append(f"{col}: {val}")
        text = "\n".join(text_parts)

        chunks.append(text)

        # Metadata for filtering
        meta = {
            "source": "bail_judgment",
            "case_id": row.get('case_id', ''),
            "court": row.get('court', ''),
            "year": str(row.get('date', ''))[:4] if pd.notna(row.get('date')) else '',
            "crime_type": row.get('crime_type', ''),
            "bail_outcome": row.get('bail_outcome', '')
        }
        metadatas.append(meta)
    return chunks, metadatas
