import pandas as pd
from datetime import datetime
from downloaders.yahoo import YahooFinanceDownloader
from predictors.time_series_predictor import TimeSeriesPredictor
from predictors.optimize_time_series_predictor import OptimizeSeriesPredictor

# Elijo las fechas sobre las cuales quiero obtener los datos
start_date = datetime(2023, 1, 1)
end_date = datetime.now()

# Lllamo al descargador de Yahoo y defino el nombre de la empresa que quiero obtener los datos
downloader = YahooFinanceDownloader(ticker="TSLA", start_date=start_date, end_date=end_date)

# Descargo los datos y los guardo en el csv
data = downloader.download_data(output_file="stock_data.csv")

# Cargo los datos desde el archivo CSV
data = pd.read_csv("stock_data.csv")

# Imprimir los datos sin procesar antes de las transformaciones
print("Datos sin procesar:")
print(data.tail())  # Imprimir las últimas filas del DataFrame cargado desde el CSV

# Selecciono las columnas que voy a usar y las renombro
data.columns = ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
data = data[["Date", "Adj Close"]]  # Seleccionar solo las columnas necesarias para Prophet
data.columns = ["ds", "y"]  # Renombrar las columnas para Prophet

# Optimizo el modelo
predictor = TimeSeriesPredictor(
    changepoint_prior_scale=0.05,
    seasonality_prior_scale=10,
    holidays_prior_scale=0.1  # Ajusta este valor según sea necesario
)
mape = predictor.fit(dataframe=data)
print(f'MAPE usando TimeSeriesPredictor: {mape}')

# Optimizacion adicional usando optuna
optimize_predictor = OptimizeSeriesPredictor()
mape_optimized = optimize_predictor.fit(dataframe=data)
print(f'MAPE después de optimización: {mape_optimized}')

# Calcular la fecha final para la predicción futura hasta julio (por ejemplo, 60 días adicionales)
last_date = pd.to_datetime(data['ds'].iloc[-1])  # Última fecha en los datos
future_dates = pd.date_range(start=last_date + pd.DateOffset(days=1), periods=30, freq='D')  # Generar fechas futuras

# Preparar el DataFrame para las predicciones futuras
future_dataframe = pd.DataFrame({'ds': future_dates})

# Realizar las predicciones lo que me importa es el yhat ese es el precio de acciones 
forecast = optimize_predictor.predict(dataframe=future_dataframe)
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
