import datetime as dt
import yfinance as yf
import pandas as pd

class YahooFinanceDownloader:
    def __init__(self, ticker, start_date, end_date=None):
   
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date if end_date else dt.datetime.now()

    def download_data(self, output_file="stock_data.csv"):
     
        data = yf.download(self.ticker, start=self.start_date, end=self.end_date)
        data.to_csv(output_file)
        return data
