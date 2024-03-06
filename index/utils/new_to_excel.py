import openpyxl
from index.utils.orders import change_order_status


def parse_from_excel_function(filename, status_admin, field_to_parse):
    try:
        wb = openpyxl.load_workbook(filename)
        sheet = wb.active
        all_unchanged_track_ids = []
        # Пройти по всем строкам второго и третьего столбца
        count = 0
        for row in sheet.iter_rows(min_row=3, values_only=True):
            column_1_data = row[field_to_parse - 1]
            if column_1_data != None:
                if change_order_status(column_1_data, status_admin):
                    count += 1
                else:
                    all_unchanged_track_ids.append(column_1_data)
        return all_unchanged_track_ids
    except Exception as e:
        print(e)


