import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
from datetime import datetime
from downloader.yahoo import YahooFinanceDownloader


def download_and_load_data(ticker: str, start_date: datetime, end_date: datetime, output_file: str):
  downloader = YahooFinanceDownloader(ticker=ticker, start_date=start_date, end_date=end_date)
  downloader.download_data(output_file=output_file)
  data = pd.read_csv(output_file)
  return data

