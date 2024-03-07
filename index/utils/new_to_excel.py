import openpyxl
from index.utils.orders import change_order_status


def parse_from_excel_function(filename, status_admin, field_to_parse):
    try:
        wb = openpyxl.load_workbook(filename)
        sheet = wb.active
        all_unchanged_track_ids = change_order_status(sheet.iter_rows(min_row=0, values_only=True), status_admin, field_to_parse)

        return all_unchanged_track_ids
    except Exception as e:
        print(e)


