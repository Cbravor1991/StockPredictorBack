from fastapi import APIRouter, Request
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data.data_manipultaio import obtain_rows
from machineLearningModels.predictors.stockPricePredictor import StockPricePredictor
from downloader.stockDataProcessor import download_and_load_data
from datetime import datetime


prediction = APIRouter()

@prediction.post("/historicalData")
async def receive_prediction(request: Request):
    data = await request.json()
    start_date = datetime(2023, 1, 1)
    end_date = datetime.now()
    ticker = {data.get('stockName')}
    output_file = "stock_data.csv"

    data = download_and_load_data(ticker, start_date, end_date, output_file)
    data = obtain_rows (data, 30)
    
    data_json = data.to_dict(orient='records')


    return {"message": "Datos recibidos correctamente", "data": data_json}

@prediction.post("/predict")
async def receive_prediction(request: Request):
    data = await request.json()

    stock_name = data.get('stockName')
    prediction_date_str = data.get('predictionDate')
    
    # NECESITO LA FECHA EN FORMATO DATE
    prediction_date = datetime.strptime(prediction_date_str, '%Y-%m-%d')
    
    start_date = datetime(2023, 1, 1)
    end_date = datetime.now()
    
    # PREDICTOR
    predictor = StockPricePredictor(stock_name, start_date, end_date)
    
    try:
        prediction = predictor.predict_for_date(prediction_date)
        return {
            "message": "Predicción realizada correctamente",
            "prediction": prediction.to_dict()
        }
    except ValueError as e:
        return {
            "message": str(e),
        }

