import pandas as pd



def build_drug_journal_graph(drugs_df: pd.DataFrame, pubmed_df: pd.DataFrame, clinical_trials_df: pd.DataFrame):
    """
    Build a relationship between drugs and journals where they are mentioned.
    It searches for each drug in the titles of PubMed and Clinical Trials articles.
    
    Returns:
    - A dictionary (JSON-style) with drug as key and list of journal mentions
    - A DataFrame with all mentions (one row per mention)
    """
    
    pubmed_df["source"] = "pubmed"
    clinical_trials_df["source"] = "clinical_trials"

    # Combine all articles into one DataFrame
    articles_df = pd.concat([pubmed_df, clinical_trials_df], ignore_index=True)

    # Get all drug names in lowercase
    drug_names = set(drugs_df["drug"].str.lower().dropna())

    json_result = {}
    rows = []

    for drug in drug_names:
        journal_entries = []
        for _, row in articles_df.iterrows():
            title = row.get("title")
            if drug in title:
                entry = {
                    "drug": drug,
                    "journal": row.get("journal", ""),
                    "title": row.get("title", ""),
                    "date": str(row.get("date", "")) if row.get("date", "") else "",                    "source": row.get("source", ""),
                    "article_id": row.get("id", "")
                }
                journal_entries.append(entry)
                rows.append(entry)  # for DataFrame

        if journal_entries:
            json_result[drug] = journal_entries

    df_result = pd.DataFrame(rows)
    return json_result, df_result
