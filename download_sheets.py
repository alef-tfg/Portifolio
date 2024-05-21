import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name("macros-key.json", scope)
client = gspread.authorize(creds)
print(client.openall())

Macros = client.open("Macros Tracker").worksheet("Data(Macros)")
Medidas = client.open("Macros Tracker").worksheet("Medidas")

Macros = pd.DataFrame( Macros.get_all_values()[1:], columns= Macros.row_values(1) )
Macros['Data'] = pd.to_datetime(Macros['Data'])
Macros.set_index('Data', inplace=True)
Macros = Macros.iloc[:, -4:]

Medidas = pd.DataFrame(Medidas.get_all_values()[1:], columns=Medidas.row_values(1))
Medidas['Data'] = pd.to_datetime(Medidas['Data'])
Medidas.set_index('Data', inplace=True)
Medidas = Medidas.iloc[:, :1]

Macros.to_parquet('macros.parquet')
Medidas.to_parquet('medidas.parquet')