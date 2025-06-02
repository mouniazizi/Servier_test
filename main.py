from src.extract.extract_pipeline import DataRepository
from src.transform.clean_df import clean_and_prepare_data
from src.load.load_df import load_dataframe
from src.transform.generate_graph import build_drug_journal_graph


def main():
    print("Extraction des données...")
    repo = DataRepository()
    raw_data = {
        "drugs": repo.get_drugs(),
        "pubmed": repo.get_pubmed(),
        "clinical_trials": repo.get_clinical_trials()
    }

    print("Nettoyage des données...")
    cleaned_data = clean_and_prepare_data(raw_data)


    print("Aperçu des données nettoyées :")
    for domain, df in cleaned_data.items():
        print(domain.upper(),df.head())
        load_dataframe(df,domain,'csv',output_dir='output/cleaned_data')

    graph_dict,graph_df = build_drug_journal_graph(cleaned_data['drugs'], cleaned_data['pubmed'], cleaned_data['clinical_trials'])
    load_dataframe(graph_df,'drug_journal','csv','output/graph')

    load_dataframe(graph_dict,'drug_journal','json','output/graph')

if __name__ == "__main__":
    main()
