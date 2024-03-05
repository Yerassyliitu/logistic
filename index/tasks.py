from celery import shared_task

from index.utils.new_to_excel import parse_from_excel_function


@shared_task
def process_excel_file(filename):
    try:
        print('try')
        parse_from_excel_function(filename)
        return {'success': 'Файл успешно обработан'}
    except Exception as e:
        print('aaaa')
        return {'error': str(e)}