import pandas as pd
import os

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
