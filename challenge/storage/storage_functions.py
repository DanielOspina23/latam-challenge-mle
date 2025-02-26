import pickle
import uuid

from fastapi import HTTPException

from google.cloud import storage


def get_last_file(bucket_name):
    client = storage.Client()

    try:
        bucket = client.get_bucket(bucket_name)
        blobs = list(bucket.list_blobs())

        if not blobs:
            raise HTTPException(status_code=500, detail='There are no blobs in the bucket.')

        blobs.sort(key=lambda blob: blob.time_created, reverse=True)
        return blobs[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


def get_training_data(bucket_name):
    latest_blob = get_last_file(bucket_name=bucket_name)
    return latest_blob.download_as_text()


def get_trained_model(bucket_name):
    latest_blob = get_last_file(bucket_name=bucket_name)
    return latest_blob.download_as_string()
    
    
def save_model_in_storage(model, bucket_name) -> str:
    """
        Save a serialized model in Google Cloud Storage with a unique name based on UUID.

        Args:
            model: trained model.
            bucket_name: Bucket where model will be saved.

        Returns:
            str: File name saved in bucket.
    """

    model_pickle = pickle.dumps(model)
    file_name = f'{uuid.uuid4()}.pkl'

    client = storage.Client()
    bucket = client.bucket(bucket_name=bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_string(model_pickle, content_type='application/octet-stream')

    return file_name


def get_file(file_name, bucket_name):
    client = storage.Client()

    try:
        bucket = client.get_bucket(bucket_name)
        blobs = bucket.list_blobs()

        if not blobs:
            return None

        for blob in blobs:
            if blob.name == file_name:
                return blob.download_as_string()

        return None

    except Exception as e:
        print(e)
