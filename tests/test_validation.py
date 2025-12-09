import pandas as pd

from src.validation import validate_schema


def test_validate_schema_missing_columns():
    df = pd.DataFrame({"date": ["2024-01-01"], "Close": [10]})
    errors = validate_schema(df)
    assert any("Volume" in err for err in errors)


def test_validate_schema_passes():
    df = pd.DataFrame(
        {
            "date": ["2024-01-01", "2024-01-02"],
            "Close": [10, 11],
            "Volume": [100, 200],
        }
    )
    errors = validate_schema(df)
    assert errors == []
