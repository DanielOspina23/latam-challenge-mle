from challenge.db.db_functions import save_metrics_to_bigquery
from challenge.model import DelayModel
from challenge.settings import Settings
from challenge.storage.storage_functions import get_last_training_file, save_model_in_storage
from challenge.utils.utils import load_data_from_csv

settings = Settings()


def train_model(bucket_name: str) -> str:
    last_file_data = get_last_training_file(bucket_name=bucket_name)
    data = load_data_from_csv(csv_data=last_file_data)
    model = DelayModel()
    features, target = model.preprocess(data=data, target_column='delay')
    metrics, training_model = model.fit(features=features, target=target)

    file_name = save_model_in_storage(model=training_model, bucket_name=settings.MODELS_BUCKET_NAME)

    save_metrics_to_bigquery(metrics=metrics, project_id=settings.project_id, dataset_id=settings.dataset_id,
                             table_id=settings.table_id, model_id=file_name)

    return file_name
