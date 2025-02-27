from io import StringIO

import pandas as pd


def load_data_from_csv(csv_data: str, cloud_data: bool) -> pd.DataFrame:
    if cloud_data:
        return pd.read_csv(StringIO(csv_data))
    return pd.read_csv(csv_data)
