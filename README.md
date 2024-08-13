# Predictor de Precio de una Acción para un Día Determinado

Este es el backend de una pequeña aplicación que tiene como objetivo predecir el precio de una acción, así como obtener los valores de la misma en los últimos 30 días pasados. Se realiza en el marco de una prueba de concepto de las librerías Prophet y Optuna, para entrenar un modelo basado en series temporales, en este caso, los valores diarios de una acción, y luego predecir un valor futuro.

La siguiente explicación detalla el uso de los parámetros para el análisis de series temporales, que utiliza en el proyecto:

- **CHANGEPOINT_PRIOR_SCALE**: Detecta fluctuaciones en la serie temporal, con un rango de 0.001 a 0.5.
- **SEASONALITY_PRIOR_SCALE**: Analiza los efectos estacionales que se repiten en un período, como la publicación de informes trimestrales, compras a principios de mes de fondos financieros, lanzamientos de productos, o crisis financieras, con un rango de 0.01 a 10.
- **HOLIDAY_PRIOR_SCALE**: Considera el impacto de los días festivos, eventos especiales y períodos de ventas por ejemplo, navidad, Black Friday, etc en el modelo.

- **CHANGE_RANGE**: Modela cambios significativos, donde 0.8 no tiene en cuenta los datos actuales, y valores de 0.9 a 1 (por ejemplo, 0.5, 0.6) reflejan tendencias de datos pasados (útil para analizar tendencias pasadas de una acción).
- **SEASONALITY_MODE**: Tiene en cuenta si las fluctuaciones estacionales son aditivas o multiplicativas. Por ejemplo, una empresa puede ver un aumento de $100 en su valor durante las temporadas festivas, independientemente de su precio actual o tendencia.

# Github FrontEnd
https://github.com/Cbravor1991/StockPredictor


# Estado
Finalizado. Se deja la configuración para una conexión básica a una base de datos, asi como el modelo y tabla para guardar datos
de un usuario, por si se quiere continuar desarrollando el mismo. Además en la clase `stockPricePredictor` se cuenta con el método
`def predict_future(self, days_ahead: int = 30)`, que no es utilizado y te permite predecir el precio de la acción para los 
próximos 30 días

# Stock Price Predictor for a Specific Day

This is the backend of a small application designed to predict the price of a stock and retrieve its values from the past 30 days. It is part of a proof of concept using the Prophet and Optuna libraries to train a time-series model based on daily stock values and predict a future value.

The following explanation details the use of parameters for time series analysis employed in the project:

- **CHANGEPOINT_PRIOR_SCALE**: Detects fluctuations in the time series, with a range from 0.001 to 0.5.
- **SEASONALITY_PRIOR_SCALE**: Analyzes seasonal effects that repeat over a period, such as quarterly reports, end-of-month financial purchases, product launches, or financial crises, with a range from 0.01 to 10.
- **HOLIDAY_PRIOR_SCALE**: Considers the impact of holidays, special events, and sales periods (e.g., Christmas, Black Friday) on the model.

- **CHANGE_RANGE**: Models significant changes, where 0.8 disregards current data, and values from 0.9 to 1 (e.g., 0.5, 0.6) reflect past data trends (useful for analyzing past trends of a stock).
- **SEASONALITY_MODE**: Accounts for whether seasonal fluctuations are additive or multiplicative. For example, a company might see a $100 increase in value during holiday seasons, regardless of its current price or trend.

# Status
Completed. The configuration for a basic database connection is included, as well as the model and table to store user data, in case further development is desired. Additionally, the `StockPricePredictor` class includes the method `predict_future(self, days_ahead: int = 30)`, which is not currently used but allows for predicting the stock price for the next 30 days.





