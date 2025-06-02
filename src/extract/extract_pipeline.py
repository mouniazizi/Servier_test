from src.extract.extract_files import extract_all_data


class DataRepository:
    """
    This class loads and gives access to the different input data sources.
    It reads all files from the data folder (pubmed, clinical_trials, drugs).
    """
    def __init__(self, base_path="data"):
        self.data = extract_all_data(base_path)

    def get_pubmed(self):
        return self.data.get("pubmed_files", [])

    def get_clinical_trials(self):
        return self.data.get("clinical_trials_files", [])

    def get_drugs(self):
        return self.data.get("drugs_files", [])
