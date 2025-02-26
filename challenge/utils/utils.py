from io import StringIO

import pandas as pd


def load_data_from_csv(csv_data: str) -> pd.DataFrame:
    return pd.read_csv(StringIO(csv_data))
