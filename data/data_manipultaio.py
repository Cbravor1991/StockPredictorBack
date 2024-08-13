import pandas as pd

def obtain_rows(dataset, number_rows):

    ultimas_filas = dataset.tail(number_rows)

 
    resultado = ultimas_filas[['Date', 'Open', 'Close', 'Volume']]
    resultado.columns = ['Fecha', 'Apertura', 'Cierre', 'Volumen']

    return resultado
    