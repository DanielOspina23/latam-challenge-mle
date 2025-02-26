from datetime import datetime

from fastapi import HTTPException
from google.cloud import bigquery


def save_metrics_to_bigquery(metrics: dict, project_id: str, dataset_id: str, table_id: str, model_id: str):
    """
    Save the model's performance metrics in BigQuery.

    Args:
        metrics (dict): A dict with model performance metrics.
        project_id (str): Project id of GCP.
        dataset_id (str): Dataset id of BigQuery.
        table_id (str): Table id of BigQuery where metrics will be saved.
        model_id (str): UUID of the model
    """

    client = bigquery.Client(project=project_id)

    row_to_insert = {
        'model_id': model_id,
        'precision_0': metrics['0']['precision'],
        'recall_0': metrics['0']['recall'],
        'f1_score_0': metrics['0']['f1-score'],
        'precision_1': metrics['1']['precision'],
        'recall_1': metrics['1']['recall'],
        'f1_score_1': metrics['1']['f1-score'],
        'accuracy': metrics['accuracy'],
        'precision_macro': metrics['macro avg']['precision'],
        'recall_macro': metrics['macro avg']['recall'],
        'f1_score_macro': metrics['macro avg']['f1-score'],
        'precision_weighted': metrics['weighted avg']['precision'],
        'recall_weighted': metrics['weighted avg']['recall'],
        'f1_score_weighted': metrics['weighted avg']['f1-score'],
        'training_date': datetime.utcnow().isoformat()
    }

    table = f'{project_id}.{dataset_id}.{table_id}'
    errors = client.insert_rows_json(table, [row_to_insert])

    if errors:
        raise HTTPException(status_code=500, detail=f'An error occurred trying to insert metrics: {errors}')
