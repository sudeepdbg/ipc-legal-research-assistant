# ipc-legal-research-assistant
legal-research-assistant/
├── backend/
│   ├── main.py
│   ├── data_loader.py
│   ├── embeddings.py (optional, merged into retriever)
│   ├── retriever.py
│   ├── prompts.py
│   ├── config.py
│   └── requirements.txt
├── frontend/
│   └── app.py
├── data/
│   ├── ipc_sections.csv
│   ├── ncrb_data.csv
│   └── judgments/ (empty, but add a README explaining format)
├── scripts/
│   └── init_db.py
├── chroma_db/ (ignored in .gitignore)
├── .gitignore
└── README.md
