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

def load_judgments(judgments_dir="data/judgments/"):
    chunks = []
    metadatas = []
    for filename in os.listdir(judgments_dir):
        if filename.endswith(".txt"):
            with open(os.path.join(judgments_dir, filename), 'r', encoding='utf-8') as f:
                text = f.read()
            # Simple chunking by paragraphs (adjust as needed)
            paragraphs = text.split('\n\n')
            for i, para in enumerate(paragraphs):
                if len(para.strip()) < 50:  # skip very short paragraphs
                    continue
                chunks.append(para)
                metadatas.append({
                    "case": filename.replace('.txt', ''),
                    "chunk_id": i,
                    "source": "judgment"
                })
    return chunks, metadatas
