import pickle
import uuid

from fastapi import HTTPException

from google.cloud import storage


def get_last_training_file(bucket_name):
    client = storage.Client()

    try:
        bucket = client.get_bucket(bucket_name)
        blobs = list(bucket.list_blobs())

        if not blobs:
            raise HTTPException(status_code=500, detail='There are no blobs in the bucket.')

        blobs.sort(key=lambda blob: blob.time_created, reverse=True)
        latest_blob = blobs[0]

        return latest_blob.download_as_text()
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
    
    
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
    file_name = f"{uuid.uuid4()}.pkl"

    client = storage.Client()
    bucket = client.bucket(bucket_name=bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_string(model_pickle, content_type='application/octet-stream')

    return file_name
