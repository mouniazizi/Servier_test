from pathlib import Path
import json


def ensure_output_folder(path="output/cleaned"):
    """
    Create the output folder if it does not exist.
    """
    Path(path).mkdir(parents=True, exist_ok=True)

def load_dataframe(df, name, file_type,output_dir="output/cleaned"):
    """
    Save the given DataFrame as a CSV or JSON file in the output folder.
    
    Parameters:
    - df: the DataFrame to save
    - name: the file name (without extension)
    - file_type: 'csv' or 'json'
    - output_dir: folder to save the file (default: output/cleaned)
    """
    ensure_output_folder(output_dir)
    if file_type=='csv':
        output_path = Path(output_dir) / f"{name}.csv"
        df.to_csv(output_path, index=False)
    if file_type=='json':
        output_path = Path(output_dir) / f"{name}.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(df, f, indent=2, ensure_ascii=False)

    print(f"Saved: {output_path}")