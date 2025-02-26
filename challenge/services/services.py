import pickle

import pandas as pd
from fastapi import HTTPException

from challenge.db.db_functions import save_metrics_to_bigquery
from challenge.model import DelayModel
from challenge.settings import Settings
from challenge.storage.storage_functions import save_model_in_storage, get_file, get_training_data, get_trained_model
from challenge.utils.utils import load_data_from_csv

settings = Settings()
model = DelayModel()


def train_model(bucket_name: str) -> str:
    last_file_data = get_training_data(bucket_name=bucket_name)

    data = load_data_from_csv(csv_data=last_file_data)

    features, target = model.preprocess(data=data, target_column="delay")
    metrics, training_model = model.fit(features=features, target=target)

    file_name = save_model_in_storage(model=training_model, bucket_name=settings.MODELS_BUCKET_NAME)

    save_metrics_to_bigquery(metrics=metrics, project_id=settings.project_id, dataset_id=settings.dataset_id,
                             table_id=settings.table_id, model_id=file_name)

    return file_name


def predict_service(data: list) -> list:

    data = [flight.__dict__ for flight in data]
    features = pd.DataFrame(data)
    features = model.preprocess(data=features)

    return model.predict(features=features)


def update_model(model_name: str = None):
    if model_name:
        trained_model = get_file(file_name=model_name, bucket_name=settings.MODELS_BUCKET_NAME)

        if trained_model:
            model_trained = pickle.loads(trained_model)
            model.load_model(model=model_trained)
        else:
            raise HTTPException(status_code=404, detail=f"Model {model_name} does not exist in the bucket.")

    last_model = get_trained_model(bucket_name=settings.MODELS_BUCKET_NAME)
    if last_model:
        model_trained = pickle.loads(last_model)
        model.load_model(model=model_trained)
    else:
        raise HTTPException(status_code=404, detail=f"There are no models in the bucket.")
