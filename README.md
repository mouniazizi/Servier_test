
# Drug Mention Data Pipeline

This project builds a data pipeline that links drugs to journals that mention them.  
It uses publication data from **PubMed** and **Clinical Trials**, and produces a final output showing which drug is mentioned by which journal, along with extra details (date, source, article ID, etc.).

---

## Project Structure

```
.
├── data/                      # Input folders:
│   ├── drugs/                 # Drug names (CSV)
│   ├── pubmed/                # PubMed publications (CSV or JSON)
│   └── clinical_trials/       # Clinical Trials publications (CSV or JSON)
│
├── SQL/ # SQL answers to questions
│ ├── Q1.sql
│ └── Q2.sql
│
├── output/                    
│   ├── cleaned_data           # Cleaned CSVs  
│   │   ├── drugs.csv   
│   │   ├── pubmed.csv   
│   │   └── clinical_trials.csv
│   └── graph.json             # Final output files
│       ├── drug_journal.csv   # Flat file: one row per mention
│       └── drug_journal.json  # Nested file: grouped by drug
├── src/                       # Source code
│   ├── extract/
│   │   ├── extract_files.py   # Load CSV/JSON files
│   │   └── extract_pipeline.py
│   ├── transform/
│   │   └── clean_df.py        # Text/date cleaning logic
│   ├── graph/
│   │   └── generate_graph.py  # Build relationships between drugs and journals
│   └── load/
│       └── load_df.py         # Save outputs
│
├── tests/                     # Unit tests
│   └── test_clean.py, ...
│
├── main.py                    # Pipeline entry point
│
└── ad_hoc.py # Bonus: answer questions
```

---

## Assumptions on the Data

- We detect drug mentions by checking if the **drug name appears in the `title`** of an article.
- Journal names are in the `journal` field of each publication.
- Drug names are compared in **lowercase**, without punctuation (simple match, no fuzzy logic, no NLP).
- A journal is linked to a drug if it published a **PubMed** or **Clinical Trial** article that mentions the drug.
- Dates may have multiple formats (e.g. `25/05/2020`, `2020-01-01`, `1 January 2020`), so we clean them carefully.
- Files are provided in CSV or JSON format.

---

## Data Pipeline Steps

### 1. Extract
- Load all input files (drugs, pubmed, clinical trials).
- Support both `.csv` and `.json` formats.
- Fix malformed JSON files if needed.

### 2. Transform
- Normalize text (lowercase, remove extra spaces).
- Clean date columns using dual parsing.
- Build relationships between:
  - Drug
  - Journal
  - Date
  - Source (PubMed or Clinical Trials)
  - Title
  - Article ID

### 3. Load
- Save results as:
  - `drug_journal.csv` → simple table
  - `drug_journal.json` → structured by drug, with a list of journal mentions

---

## Ad Hoc Analysis (Bonus)

Two extra functions were implemented:

### 1- Journal with Most Drugs
Find the journal that **mentions the most different drugs**.

### 2- Related Drugs (PubMed Only)
For a given drug, find other drugs **mentioned in the same journals**,  
**only from PubMed**, not Clinical Trials.

---

## Testing

- Simple unit tests for data loading, cleaning, and transformation.
- Run tests using:

```bash
pytest tests/
```

---
## Project Setup

### Requirements

Make sure you have:

- Python 3.9 or newer installed
- Poetry installed
- Git (for cloning the project)

### Install the project

Clone the project and install dependencies:

```bash
git clone 
```

### Run the pipeline

You can run the main pipeline with:

```bash
poetry run python main.py
```

### Run tests

You can run the unit test with:

```bash
pytest tests/
```

The output files will be saved in the `output/` folder:
- `drug_journal.csv`
- `drug_journal.json`

---

## Docker and Automation

This project can be put in a Docker image.  
It helps run the pipeline the same way everywhere (locally or in the cloud).

We can also use CI/CD to:

- Test the code automatically
- Build and push the Docker image to Artifact Registry
- Use this image in Cloud Composer to run the pipeline on a schedule

This makes the project easier to run, update, and deploy.

---


## Going Further

###  What to consider for big data?

If the data is very large (many files or terabytes), we should:

- Read data in parts (not all at once).
- Use chunked reading (`chunksize`) or streaming.
- Store data in the cloud (GCP, AWS...).
- Use engines like BigQuery or Spark instead of pandas.

###  What to change in this code?

To make this project handle big data:

- Replace pandas with BigQuery queries.
- Use DBT for transformation logic and dependencies.
- Use Airflow to automate the runs.

---

## Conclusion

This project shows how to build a clean data pipeline to link drugs with journals based on publications.  
The solution is modular, testable, and easy to extend.  
Bonus functions help analyze the results further.  
It can scale with small changes if needed for cloud or big data use.

---