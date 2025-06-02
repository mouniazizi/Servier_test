import pandas as pd
from src.transform.generate_graph import build_drug_journal_graph

def test_build_drug_journal_graph():
    drugs = pd.DataFrame({"drug": ["aspirin", "paracetamol"]})
    pubmed = pd.DataFrame([
        {"id": 1, "title": "aspirin for headache", "journal": "med journal", "date": "2020-01-01"}
    ])
    clinical = pd.DataFrame([
        {"id": 2, "title": "paracetamol trial", "journal": "health journal", "date": "2021-01-01"}
    ])
    json_result, df_result = build_drug_journal_graph(drugs, pubmed, clinical)
    assert "aspirin" in json_result
    assert "paracetamol" in json_result
    assert df_result.shape[0] == 2
