import fastapi
import uvicorn
from fastapi import HTTPException

from challenge.schemas.templates import RequestTemplate, FitRequestTemplate
from challenge.services.services import train_model, predict_service, update_model, predict_proba_service
from challenge.settings import Settings
from challenge.utils.logger import get_logger

settings = Settings()

app = fastapi.FastAPI(
    title='Flight Delay Model',
    version=settings.APP_VERSION,
    description='API to calculate probability of flight delay'
)

logger = get_logger()


@app.on_event('startup')
async def startup():
    update_model()


@app.get("/health", status_code=200)
async def get_health() -> dict:
    logger.info("Request received for the health endpoint")
    return {
        "status": "OK"
    }


@app.post("/predict", status_code=200)
async def post_predict(data: RequestTemplate) -> dict:
    try:
        predictions = predict_service(data=data.flights)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'An error occurred during prediction: {str(e)}')

    return {'predict': predictions}


@app.post('/fit', status_code=200)
async def post_fit(request: FitRequestTemplate) -> dict:
    logger.info("Request received for the fit endpoint")
    try:
        trained_model = train_model(bucket_name=request.bucket_name, cloud_data=request.cloud_data)
        return {"trained_model": trained_model}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during training: {str(e)}")


@app.get('/update-model', status_code=200)
async def force_update_model(model_id: str, cloud: bool) -> dict:
    if model_id.endswith('.pkl'):
        raise HTTPException(status_code=400, detail='Model id should not have extension')
    try:
        status = update_model(model_name=f'{model_id}.pkl', cloud=cloud)
        return {'updated_model': model_id, 'status': status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'An error occurred during updating model: {str(e)}')


@app.post('/predict-proba', status_code=200)
async def post_predict_proba(data: RequestTemplate) -> dict:
    try:
        predictions = predict_proba_service(data=data.flights)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'An error occurred during prediction: {str(e)}')

    return {'predict': predictions}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080, loop='asyncio')
