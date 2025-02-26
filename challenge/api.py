import fastapi
import uvicorn
from fastapi import HTTPException

from challenge.schemas.templates import RequestTemplate, FitRequestTemplate
from challenge.services.train_service import train_model
from challenge.settings import Settings

settings = Settings()

app = fastapi.FastAPI(
    title='Flight Delay Model',
    version=settings.APP_VERSION,
    description='API to calculate probability of flight delay'
)


@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }


@app.post("/predict", status_code=200)
async def post_predict(data: RequestTemplate) -> dict:

    return {'predict': [0]}


@app.post('/fit', status_code=200)
async def post_fit(request: FitRequestTemplate) -> dict:
    try:
        trained_model = train_model(bucket_name=request.bucket_name)
        return {"trained_model": trained_model}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during training: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, loop="asyncio")
