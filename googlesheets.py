import pandas as pd
import gspread
from gspread_pandas import Spread, Client
from gspread_pandas.conf import get_config
import traceback
import sys
from pathlib import Path

class GoogleSheets:
  SCOPE = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive'
  ]

  def __init__(self, title, sheet_num, log, conf_file) -> None:
      self.log = log

      if isinstance(conf_file, str):
        conf_file = Path(conf_file)
      assert conf_file.is_file(), f"File does not exist, {conf_file}"
 
      conf_dir = conf_file.parents[0]
      file_name = conf_file.name
      self.log.info(f"Conf Dir: {conf_dir}")
      self.log.info(f"Conf Filename: {file_name}")

      conf = get_config(conf_dir=conf_dir, file_name=file_name)
      client = Client(config=conf)
      try:
        self.spread = Spread(title, sheet=sheet_num, client=client)
      except gspread.exceptions.WorksheetNotFound:
        e = traceback.format_exc()
        self.log.error(e)
        self.log.error(f"sheet_num does not exist.")
        sys.exit(1)

  def get_sheet(self):
    sheet_df = self.spread.sheet_to_df(index=None)
    # Parse date, status, mac columns
    if 'date' in sheet_df.columns.tolist():
      sheet_df['date'] = pd.to_datetime(sheet_df['date'])
  
    return sheet_df
  
  def write_sheet(self, sheet_name, data):
    self.spread.df_to_sheet(data, sheet=sheet_name, start='A1', replace=True, index=False)