import openpyxl

from index.utils.connect_firebase import default_user_reference, created_status_reference
from index.utils.orders import add_order


def parse_from_excel_function(filename):
    # Открыть Excel файл
    wb = openpyxl.load_workbook(filename)
    sheet = wb.active

    # Пройти по всем строкам второго и третьего столбца
    for row in sheet.iter_rows(min_row=2, values_only=True):
        column_2_data = row[1]
        added_status = add_order({
            "track_id": column_2_data,
            "user": default_user_reference,
            "status": created_status_reference
        })
        print(added_status)


