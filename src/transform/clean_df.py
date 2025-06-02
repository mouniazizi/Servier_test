import pandas as pd
import re

def merge_data(data: list[pd.DataFrame]) -> pd.DataFrame:
    """
    Merge a list of DataFrames into one DataFrame.
    If the list is empty, return an empty DataFrame.
    """

    if not data:
        return pd.DataFrame()
    return pd.concat(data, ignore_index=True)

def clean_dates(df: pd.DataFrame, date_column: str) -> pd.DataFrame:
    """
    Clean and convert the date column into a standard date format.
    Handles multiple formats using dayfirst and mixed mode.
    """
    df[date_column] = (
        df[date_column]
        .astype(str)
        .str.strip()
    )
    df[date_column] = pd.to_datetime(df[date_column], errors='coerce',dayfirst=True,format="mixed").dt.date
    return df

def normalize_text_fields(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """
    Normalize text columns by:
    - Converting to lowercase
    - Removing extra spaces
    - Removing special characters
    """
    for col in columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.lower()
            # clean special characters
            df[col] = df[col].astype(str).apply(lambda x: re.sub(r"[^\w\s]", "", x))
    return df

def rename_column(df: pd.DataFrame, old_name: str, new_name: str) -> pd.DataFrame:
    """
    Rename a column if it exists in the DataFrame.
    """
    if old_name in df.columns:
        return df.rename(columns={old_name: new_name})
    return df

def clean_and_prepare_data(file_groups: dict[str, list[pd.DataFrame]]) -> dict[str, pd.DataFrame]:
    """
    Clean and prepare the merged DataFrames by file_type.
    - For pubmed and clinical_trials: clean dates, normalize text, and rename title column
    - For drugs: normalize drug names
    """
    cleaned = {}
    for file_type, dfs in file_groups.items():
        merged = merge_data(dfs)
        if file_type != "drugs":
            merged = clean_dates(merged, "date")
            merged = normalize_text_fields(merged, ["title", "journal","scientific_title"])
            merged = rename_column(merged,"scientific_title","title")
        else:
            merged = normalize_text_fields(merged, ["drug"])
        cleaned[file_type] = merged
    return cleaned
