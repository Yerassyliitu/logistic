import openpyxl
from index.utils.orders import change_order_status


def parse_from_excel_function(filename, status_admin, field_to_parse):
    try:
        wb = openpyxl.load_workbook(filename)
        sheet = wb.active

        # Пройти по всем строкам второго и третьего столбца
        count = 0
        for row in sheet.iter_rows(min_row=3, values_only=True):
            column_1_data = row[field_to_parse - 1]
            if column_1_data != None:
                change_order_status(column_1_data, status_admin)
                count += 1
        return count
    except Exception as e:
        print(e)


