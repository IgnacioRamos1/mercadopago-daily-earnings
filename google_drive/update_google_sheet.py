import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from utils.utils import get_parameter
import json
from calendar import monthrange
from datetime import timedelta


def update_google_sheet(product_name, ganancia_neta):
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
            spreadsheet = client.open(product_name)
        except Exception as e:
            print(f"Error opening spreadsheet: {e}")
            return # Si hay un error, simplemente retornar sin hacer nada

        # Verificar si existe la hoja del mes actual
        month_name = datetime.now().strftime('%B').capitalize()  # Nombre del mes en inglés
        month_name_es = {
            'January': 'Enero', 'February': 'Febrero', 'March': 'Marzo',
            'April': 'Abril', 'May': 'Mayo', 'June': 'Junio',
            'July': 'Julio', 'August': 'Agosto', 'September': 'Septiembre',
            'October': 'Octubre', 'November': 'Noviembre', 'December': 'Diciembre'
        }
        month_name = month_name_es[month_name]  # Convertir al nombre en español

        try:
            worksheet = spreadsheet.worksheet(month_name)
        
        # TODO: Esta parte no anda, hay que arreglarla, se traba despues de eliminar cierto numero de celdas y deja de trabajar.
        except gspread.exceptions.WorksheetNotFound:
            # Si no existe, copiar el formato de una hoja existente y crear una nueva
            template_sheet = spreadsheet.get_worksheet(0)
            spreadsheet.duplicate_sheet(template_sheet.id, new_sheet_name=month_name)
            worksheet = spreadsheet.worksheet(month_name)

            # Obtener todas las fórmulas de la hoja
            range_name = f"{month_name}!A1:Z1000"
            range_data = spreadsheet.values_get(range_name)
            values = range_data.get('values', [])

            formulas = []
            for i, row in enumerate(values):
                for j, cell in enumerate(row):
                    if cell.startswith('='):
                        formulas.append((i+1, j+1, cell))

            # Limpia la hoja duplicada manteniendo solo el encabezado y las fórmulas
            all_values = worksheet.get_all_values()
            for i, row in enumerate(all_values[1:], start=2):
                for j, cell in enumerate(row, start=1):
                    worksheet.update_cell(i, j, '')  # Limpiamos la celda

            # Volver a escribir solo las fórmulas
            for formula in formulas:
                row, col, formula_value = formula
                worksheet.update_cell(row, col, formula_value)

            # Ajustar la columna de fechas
            days_in_month = monthrange(datetime.now().year, datetime.now().month)[1]
            date_column = 1
            for day in range(1, days_in_month + 1):
                date_value = f"{day}/{datetime.now().month}/{datetime.now().year}"
                worksheet.update_cell(day + 1, date_column, date_value)

        # Identificar la fila correspondiente a la fecha de ayer
        yesterday_date = (datetime.now() - timedelta(days=1)).strftime('%-d/%-m/%y')
        date_column_values = worksheet.col_values(1)
        try:
            date_row = date_column_values.index(yesterday_date) + 1
        except ValueError:
            date_row = len(date_column_values) + 1
            worksheet.update_cell(date_row, 1, yesterday_date)
            
        # Identificar la columna "FACT neta(mp)"
        header_row = worksheet.row_values(1)
        try:
            ganancia_column = header_row.index("FACT neta(mp)") + 1
        except ValueError:
            raise Exception("La columna 'FACT neta(mp)' no fue encontrada en la hoja de cálculo.")
        
        print('ganancia_neta:', ganancia_neta, 'type:', type(ganancia_neta))

        # Reemplazar comas con puntos y puntos con comas
        ganancia_neta = ganancia_neta.replace(",", "X").replace(".", ",").replace("X", ".")

        # Actualizar el valor en la celda correspondiente
        worksheet.update_cell(date_row, ganancia_column, ganancia_neta)

        return True

    except Exception as e:
        raise Exception(f"Error in update_google_sheet function: {e}")
