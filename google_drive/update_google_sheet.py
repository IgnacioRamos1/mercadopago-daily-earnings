from utils.utils import get_parameter

from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from calendar import monthrange
import gspread
import json
import pytz
import time
import random


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
            raise Exception(f"Error authorizing gspread client: {e}")

        try:
            # Acceder al archivo de Google Sheets
            spreadsheet_name = f"{shop_name} - {product_name}"
            spreadsheet = client.open(spreadsheet_name)
        except Exception as e:
            print(f"Error opening spreadsheet: {e}")
            return # Si hay un error, simplemente retornar sin hacer nada

        # Generar el nombre de la hoja en el formato "Octubre-2023"
        month_year_name = datetime.now().strftime('%B-%Y').capitalize()
        month_year_name_es = {
            'January': 'Enero', 'February': 'Febrero', 'March': 'Marzo',
            'April': 'Abril', 'May': 'Mayo', 'June': 'Junio',
            'July': 'Julio', 'August': 'Agosto', 'September': 'Septiembre',
            'October': 'Octubre', 'November': 'Noviembre', 'December': 'Diciembre'
        }
        month_year_name = month_year_name_es[month_year_name.split('-')[0]] + "-" + month_year_name.split('-')[1]

        # Intentar obtener la hoja del mes actual hasta un máximo de 3 veces
        retries = 3
        for _ in range(retries):
            try:
                worksheet = spreadsheet.worksheet(month_year_name)
                break

            except gspread.exceptions.WorksheetNotFound:
                # Si no existe, duplicamos la hoja template
                template_sheet_name = "Template"

                # Si no existe la hoja template, skippear y retornar sin hacer nada
                try:
                    template_sheet = spreadsheet.worksheet(template_sheet_name)
                except gspread.exceptions.WorksheetNotFound:
                    return

                template_sheet = spreadsheet.worksheet(template_sheet_name)
                spreadsheet.duplicate_sheet(template_sheet.id, new_sheet_name=month_year_name)
                worksheet = spreadsheet.worksheet(month_year_name)

                # Ajustar la columna de fechas
                days_in_month = monthrange(datetime.now().year, datetime.now().month)[1]
                date_column = 1

                # Lista para almacenar las celdas que se actualizarán
                update_cells = []

                for day in range(1, days_in_month + 1):
                    date_value = f"{day}/{datetime.now().month}/{datetime.now().year}"
                    cell = worksheet.cell(day + 1, date_column)
                    cell.value = date_value
                    update_cells.append(cell)

                # Hacer un solo llamado para actualizar todas las celdas
                worksheet.update_cells(update_cells)
            
            except Exception as e:
                if 'RATE_LIMIT_EXCEEDED' in str(e) and _ < retries - 1:
                    # Esperar con un retroceso exponencial
                    time.sleep((2 ** _) + random.uniform(0, 1))
                else:
                    raise

        # Definir la zona horaria de Argentina
        tz_argentina = pytz.timezone('America/Argentina/Buenos_Aires')

        # Obtener la fecha y hora actual y ajustarla a la zona horaria de Argentina
        now_argentina = datetime.now(tz_argentina)

        # Identificar la fila correspondiente a la fecha actual en Argentina
        today_date_full = now_argentina.strftime('%-d/%m/%Y')  # Formato sin cero adelante y año completo
        today_date_short = now_argentina.strftime('%-d/%m/%y')  # Formato sin cero adelante y año abreviado
        date_column_values = worksheet.col_values(1)

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
        try:
            ganancia_column = header_row.index("FACT neta(mp)") + 1
        except ValueError:
            raise Exception("La columna 'FACT neta(mp)' no fue encontrada en la hoja de cálculo.")

        # Reemplazar comas con puntos y puntos con comas
        ganancia_neta = ganancia_neta.replace(",", "X").replace(".", ",").replace("X", ".")

        # Actualizar el valor en la celda correspondiente
        worksheet.update_cell(date_row, ganancia_column, ganancia_neta)

        return True

    except Exception as e:
        raise Exception(f"Error in update_google_sheet function: {e}")
