from utils.utils import get_parameter

from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
import gspread
import json
import pytz
import time


def update_google_sheet(product_name, ganancia_neta, shop_name):
    try:
        credentials = get_parameter('google_credentials')
        credentials = json.loads(credentials)

        # Autenticación y conexión a Google Sheets
        scope = ["https://spreadsheets.google.com/feeds", 
                "https://www.googleapis.com/auth/spreadsheets", 
                "https://www.googleapis.com/auth/drive.file", 
                "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
        try:
            client = gspread.authorize(creds)
        except Exception as e:
            print(f"Error authorizing gspread client: {e}")
            raise Exception(f"Error authorizing gspread client: {e}")

        max_retries = 3  # Número máximo de intentos
        retry_delay = 90  # Tiempo de espera en segundos entre intentos

        for attempt in range(1, max_retries + 1):
            try:
                # Acceder al archivo de Google Sheets
                spreadsheet_name = f"{shop_name} - {product_name}"
                print(f"Opening spreadsheet: {spreadsheet_name}")
                spreadsheet = client.open(spreadsheet_name)
                
                print(f"Spreadsheet opened: {spreadsheet_name}")
                
                break  # Salir del bucle si la operación tiene éxito
            except Exception as e:
                if attempt == max_retries:
                    print(f"Error opening spreadsheet: {e}")
                    raise Exception(f"Error opening spreadsheet: {e}")
                print(f"Waiting {retry_delay} seconds before retrying...")
                time.sleep(retry_delay)

        # Definir la zona horaria de Argentina
        tz_argentina = pytz.timezone('America/Argentina/Buenos_Aires')

        # Obtener la fecha y hora actual y ajustarla a la zona horaria de Argentina y restarle un día
        now_argentina = datetime.now(tz_argentina) - timedelta(days=1)

        print(f"Current date in Argentina: {now_argentina}")
        
        # Generar el nombre de la hoja en el formato "Octubre-2023"
        month_year_name = now_argentina.strftime('%B-%Y').capitalize()
        month_year_name_es = {
            'January': 'Enero', 'February': 'Febrero', 'March': 'Marzo',
            'April': 'Abril', 'May': 'Mayo', 'June': 'Junio',
            'July': 'Julio', 'August': 'Agosto', 'September': 'Septiembre',
            'October': 'Octubre', 'November': 'Noviembre', 'December': 'Diciembre'
        }
        month_year_name = month_year_name_es[month_year_name.split('-')[0]] + "-" + month_year_name.split('-')[1]

        try:
            worksheet = spreadsheet.worksheet(month_year_name)

        except gspread.exceptions.WorksheetNotFound:
            raise Exception(f"La hoja de cálculo '{month_year_name}' no fue encontrada en el archivo de Google Sheets.")

        # Identificar la fila correspondiente a la fecha actual en Argentina
        today_date_full = now_argentina.strftime('%-d/%m/%Y')  # Formato sin cero adelante y año completo
        today_date_short = now_argentina.strftime('%-d/%m/%y')  # Formato sin cero adelante y año abreviado
        date_column_values = worksheet.col_values(1)

        print(f"Searching for date {today_date_full} or {today_date_short} in column 1 of worksheet {month_year_name}")

        try:
            date_row = date_column_values.index(today_date_full) + 1
        except ValueError:
            try:
                date_row = date_column_values.index(today_date_short) + 1
            except ValueError:
                date_row = len(date_column_values) + 1
                worksheet.update_cell(date_row, 1, today_date_full)

        # Identificar la columna "FACT neta(mp)"
        header_row = worksheet.row_values(1)

        print(f"Searching for column 'FACT neta(mp)' in row 1 of worksheet {month_year_name}")

        try:
            ganancia_column = header_row.index("FACT neta(mp)") + 1
        except ValueError:
            raise Exception("La columna 'FACT neta(mp)' no fue encontrada en la hoja de cálculo.")

        # Reemplazar comas con puntos y puntos con comas
        ganancia_neta = ganancia_neta.replace(",", "X").replace(".", ",").replace("X", ".")

        try:
            print(f"Updating cell {date_row}, {ganancia_column} with value {ganancia_neta}, {type(ganancia_neta)}")
            # Actualizar el valor en la celda correspondiente
            worksheet.update_cell(date_row, ganancia_column, ganancia_neta)
        except Exception as e:
            print(f"Error updating cell: {e}")
            raise Exception(f"Error updating cell: {e}")

        print(f"Finished updating spreadsheet: {spreadsheet_name}")
        
        return True

    except Exception as e:
        raise Exception(f"Error in update_google_sheet function: {e}")
