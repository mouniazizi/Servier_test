import pandas as pd
from src.transform.clean_df import clean_dates, normalize_text_fields

def test_clean_dates():
    import pandas as pd
    major = int(pd.__version__.split(".")[0])
    if major < 2:
        import pytest
        pytest.skip("format='mixed' uniquement supporté à partir de Pandas 2.0")

    df = pd.DataFrame({
        "date": ["25/05/2020", "2020-01-01", "1 January 2020"]
    })
    cleaned = clean_dates(df, "date")
    assert cleaned["date"].notna().all()


def test_normalize_text_fields():
    df = pd.DataFrame({"title": ["  Hello! ", "World!"]})
    norm = normalize_text_fields(df, ["title"])
    assert norm["title"].tolist() == ["hello", "world"]
