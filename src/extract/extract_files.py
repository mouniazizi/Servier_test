import pandas as pd
import json
from pathlib import Path


def extract_csv(file_path: str) -> pd.DataFrame:
    """
    Read a CSV file and return a DataFrame.
    """    
    return pd.read_csv(file_path)

def extract_json(file_path: str) -> pd.DataFrame:
    """
    Read a JSON file and return a DataFrame.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return pd.DataFrame(data)

def clean_json_text(raw):
    """
    Removes trailing commas to make the JSON valid.
    """
    cleaned = raw.strip()

    # Remove trailing commas
    cleaned = cleaned.replace(',\n]', '\n]')
    cleaned = cleaned.replace(',\n}', '\n}')
    cleaned = cleaned.rstrip(',]') + ']'

    return cleaned

def extract_json_with_fix(file_path):
    """
    Try to load a JSON file.
    If it fails, try to fix it and load again.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return pd.DataFrame(json.load(f))
    except json.JSONDecodeError as e:
        print(f"[JSON error] {file_path} – {e}")
        
        # Second attempt with a fix
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                raw = f.read()
            fixed = clean_json_text(raw)
            data = json.loads(fixed)
            print(f"[Fix successful] {file_path}")
            return pd.DataFrame(data)
        except Exception as e2:
            print(f"[Fix failed] {file_path} – {e2}")
            return None

def extract_csv_or_json(file_path):
    """
    Detect file format and load it with the appropriate function.
    """
    if file_path.suffix == '.csv':
        return extract_csv(file_path)
    elif file_path.suffix == '.json':
        return extract_json_with_fix(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")

def extract_all_data(base_path="data"):
    """
    Read all CSV or JSON files in each subfolder of the base path (e.g. pubmed, clinical_trials, drugs).
    Return a dictionary of lists of DataFrames, grouped by subfolder name.
    """
    base = Path(base_path)
    file_type_data = {}

    for file_type_folder in base.iterdir():  # pubmed/, clinical_trials/, drugs/, etc.
        if file_type_folder.is_dir():
            file_type_data[file_type_folder.name] = []
            for file in file_type_folder.glob("*"):
                content = extract_csv_or_json(file)
                file_type_data[file_type_folder.name].append(content)
    return file_type_data