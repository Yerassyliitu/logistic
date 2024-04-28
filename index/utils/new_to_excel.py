import openpyxl
from index.utils.orders import change_order_status


def parse_from_excel_function(filename, status_admin, field_to_parse, editor_Ref):
    all_columns = []
    try:
        wb = openpyxl.load_workbook(filename)
        sheet = wb.active
        for row in sheet.iter_rows(min_row=0, values_only=True):
            column_1_data = row[field_to_parse - 1]
            if column_1_data != None:
                all_columns.append(column_1_data)
        unchanged = change_order_status(all_columns, status_admin, editor_Ref)
        return unchanged
    except Exception as e:
        print(e)


