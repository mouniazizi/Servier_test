
def journal_with_most_unique_drugs(data):
    """
    Find the journal that mentions the most different drugs.
    
    Returns:
    - The journal name
    - The number of unique drugs it mentions
    """
    journal_drugs = {}

    for drug in data:
        for mention in data[drug]:
            journal = mention["journal"]
            if journal not in journal_drugs:
                journal_drugs[journal] = set()
            journal_drugs[journal].add(drug)

    max_journal = None
    max_count = 0

    for journal, drugs in journal_drugs.items():
        if len(drugs) > max_count:
            max_count = len(drugs)
            max_journal = journal

    return max_journal,max_count



def get_related_drugs_from_pubmed(data, target_drug):
    """
    For a given drug, find other drugs that are mentioned
    in the same PubMed journals (not Clinical Trials).
    
    Returns:
    - A set of related drugs
    """
    target_drug = target_drug.lower()
    pubmed_journals = []

    # Find journals where the target drug is mentioned (PubMed only)
    for mention in data.get(target_drug):
        if mention["source"] == "pubmed":
            pubmed_journals.append(mention["journal"])

    related = set()

    # Search for other drugs in the same journals
    for drug in data:
        if drug == target_drug:
            continue
        for mention in data[drug]:
            if mention["source"] == "pubmed" and mention["journal"] in pubmed_journals:
                related.add(drug)
                break  # Stop after first match

    return related


if __name__=='__main__':
    
    # Load the graph result (from previous step)
    import json 
    with open("output/graph/drug_journal.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Find journal with most unique drugs
    top_journal, top_count = journal_with_most_unique_drugs(data)
    print("Journal with the most unique drugs mentioned:", top_journal, top_count)

    # 2. Find related drugs to a specific one (PubMed only)
    related = get_related_drugs_from_pubmed(data, "tetracycline")
    print("Drugs related to 'tetracycline' via shared PubMed journals:", related)