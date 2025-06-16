from src.extract.extract_pipeline import DataRepository
from src.transform.clean_df import clean_and_prepare_data
from src.load.load_df import load_dataframe
from src.transform.generate_graph import build_drug_journal_graph


def main():
    print("Extracting data...")
    repo = DataRepository()
    raw_data = {
        "drugs": repo.get_drugs(),
        "pubmed": repo.get_pubmed(),
        "clinical_trials": repo.get_clinical_trials()
    }

    print("Cleaning data...")
    cleaned_data = clean_and_prepare_data(raw_data)

    print("Preview of cleaned data:")
    for source, df in cleaned_data.items():
        print(source.upper(), df.head())
        load_dataframe(df, source, 'csv', output_dir='output/cleaned_data')

    # Build the drug-journal relationships
    graph_dict, graph_df = build_drug_journal_graph(
        cleaned_data['drugs'], cleaned_data['pubmed'], cleaned_data['clinical_trials']
    )

    # Save outputs
    load_dataframe(graph_df, 'drug_journal', 'csv', 'output/graph')
    load_dataframe(graph_dict, 'drug_journal', 'json', 'output/graph')


if __name__ == "__main__":
    main()
