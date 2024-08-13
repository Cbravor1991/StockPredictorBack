import pandas as pd
import optuna
from .time_series_predictor import TimeSeriesPredictor

class OptimizeSeriesPredictor:
    def __init__(self):
        """
        Inicia el predictor de series de tiempo y el optimizador optuna.
        *CHANGEPOINT_PRIOR_SCALE = Detectar fluctuaciones en la seria temporales 0.001 a 0.5
        *SEASONALYTY_PRIOR_SCALE: Analiza efectos estacionales, que se repiten en un periodo por ejemplo, la salida de informes
        trimestrales y la compra a principio de mes de fondos financieros, también el lanzamiento de productos , crisis financiera 0.01 a 10
        *HOLIDAY_PRIOR_SCALE: Impactos del días festivos en los modelos, feriados, fiestas, lo que es el blackfriday en compañias ecomerce
        
        *CHANGE_RANGE: Modelar en base a los cambios significativos, por ejemplo 0.8 no tiene en cuenta los datos actuales, 0.9 y 1 0.5 0.6 bien el en pasado
        (ANALIZO UNA ACCION SI ME INTERESA VER SU TENDENCIA PASADA)
        *seasionality_mode: tiene en cuenta si las fluctuaciones estacionales, son aditivas o multiplicativas, por ejemplo una empresa en épocas de fiesta
        puede aumentar su valor 5 dolares independientemente de cual es precio que tiene y la tendencia que venia teniendo
         
        """
        self.model = TimeSeriesPredictor(changepoint_prior_scale = 0.05, seasonality_prior_scale= 10, holidays_prior_scale= 10, changepoint_range=0.8, seasonality_mode='additive')
        self.optuna = optuna.create_study(direction='minimize')

    def fit(self, dataframe: pd.DataFrame):
        """
        Realiza la optimización de hiperparametros y entrena el modelo
        """
        self.optuna.optimize(lambda trial: self.objective(trial, dataframe), n_trials=10)
        self.model = TimeSeriesPredictor(
            
            self.optuna.best_params["changepoint_prior_scale"], 
            self.optuna.best_params["seasonality_prior_scale"], 
            self.optuna.best_params["holidays_prior_scale"],
            changepoint_range=self.optuna.best_params["changepoint_range"],
            seasonality_mode=self.optuna.best_params.get("seasonality_mode", 'additive')  # Utiliza 'additive' por defecto si no está presente
        )
        return self.model.fit(dataframe)

    def predict(self, dataframe: pd.DataFrame):
        """
        Realiza predicciones utilizando el mejor modelo ajustado.
        """
        return self.model.predict(dataframe)

    def objective(self, trial, dataframe):
        """
        Define la función objetivo para Optuna.
        """
        changepoint_prior_scale = trial.suggest_float('changepoint_prior_scale', 0.001, 0.5, step=0.001)
        seasonality_prior_scale = trial.suggest_float('seasonality_prior_scale', 0.01, 10, step=0.01)
        holidays_prior_scale = trial.suggest_float('holidays_prior_scale', 0.01, 10, step=0.01)
        changepoint_range = trial.suggest_float('changepoint_range', 0.8, 0.95, step=0.01)
        seasonality_mode = trial.suggest_categorical('seasonality_mode', ['additive', 'multiplicative'])

        predictor = TimeSeriesPredictor(
            changepoint_prior_scale, 
            seasonality_prior_scale, 
            holidays_prior_scale, 
            changepoint_range=changepoint_range,
            seasonality_mode=seasonality_mode
        )
        return predictor.fit(dataframe)
