import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from predictors.optimize_time_series_predictor import OptimizeSeriesPredictor
import pandas as pd
from datetime import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from downloader.stockDataProcessor import download_and_load_data

class StockPricePredictor:
    def __init__(self, ticker: str, start_date: datetime, end_date: datetime):
      
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.data = None
        #INSTANCIO OPTUNA
        self.optimize_predictor = OptimizeSeriesPredictor()
        
        # CARGO LO DATOS 
        self.load_data()
        
        # SE UTILIZA EL OBJETO PROPIO DE OPTUNA Y SE REALIZA LA OPTIMIZACIÓN QUE ENTRENA EL MODELO
        self.optimize_model()
        
        
    

    def load_data(self):
        
        '''CARGO LA DATA Y LA PREPARO PARA PASARLA A OPTUNA QUE NECESITA LAS FILAS DS E Y'''
      
        self.data = download_and_load_data(ticker=self.ticker, start_date=self.start_date, end_date=self.end_date, output_file="stock_data.csv")
        
        self.data.columns = ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
        self.data = self.data[["Date", "Adj Close"]]
        self.data.columns = ["ds", "y"]
        
        print("Datos preparados:")
        print(self.data.tail())
        
        
    def optimize_model(self):
        
        '''
        Optimiza el modelo y lo devuelve optimizado
        
        '''
       
        mape_optimized = self.optimize_predictor.fit(self.data)
        print(f'MAPE después de optimización: {mape_optimized}')
        return mape_optimized
    
    def predict_for_date(self, target_date: datetime):
        """
        Predice una fecha
        """
        if self.data is None:
            raise ValueError("Los datos no están cargados.")

        # TENGO QUE VER QUE LA FECHA QUE SE PIDE NO SEA UNA FECHA VIEJA
        last_date = pd.to_datetime(self.data['ds'].iloc[-1])
        if target_date <= last_date:
            raise ValueError("La fecha objetivo debe ser posterior a la última fecha en los datos históricos.")

        # LLAMO A OPTUNA PARA PREDECIR
        future_dataframe = pd.DataFrame({'ds': [target_date]})
        forecast = self.optimize_predictor.predict(dataframe=future_dataframe)
        
        prediction = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].iloc[0]
        print(f"Predicción para {target_date}:")
        print(prediction)
        return prediction
   
    def predict_future(self, days_ahead: int = 30):
        """
        Predice 30 adías a futuro
        """
        if self.data is None:
            raise ValueError("Los datos no están cargados. Llama a `load_data` primero.")

        #Genero las fechas por las que voy a cosultar
        last_date = pd.to_datetime(self.data['ds'].iloc[-1])
        future_dates = pd.date_range(start=last_date + pd.DateOffset(days=1), periods=days_ahead, freq='D')
        future_dataframe = pd.DataFrame({'ds': future_dates})
        #realizo la prediccion, para las fechas que paso
        prediccion_30_dias = self.optimize_predictor.predict(dataframe=future_dataframe)
        
        print("Predicciones futuras:")
        print(prediccion_30_dias[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
        return prediccion_30_dias[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    
   

if __name__ == "__main__":

    predictor = StockPricePredictor(ticker="TSLA", start_date=datetime(2023, 1, 1), end_date=datetime.now())

  
    prediccion_30_dias = predictor.predict_future(days_ahead=30)

    prediccion_dia = predictor.predict_for_date(target_date=datetime(2024, 12, 31))
