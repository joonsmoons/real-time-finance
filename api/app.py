from fastapi import FastAPI
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware

sentiment_pipeline = pipeline(
    model="mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"
)


app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/api/v1/health")
async def check_health():
    return {"status": "healthy"}


@app.get("/api/v1/get_sentiment/{text}")
async def get_sentiment(text: str):
    return sentiment_pipeline(text)[0]
