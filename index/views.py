from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render

from index.forms import LogisticForm

from index.utils.new_to_excel import parse_from_excel_function


def upload_file(request):
    with open('index/order_count.txt', 'r') as file:
        current_count = int(file.read())
    with open('index/last_changed_date.txt', 'r') as file:
        current_last_changed_date = file.read()
    if request.method == 'POST':
        print('a')
        form = LogisticForm(request.POST, request.FILES)
        if form.is_valid():
            print('b')
            excel_file = request.FILES['file']
            password = request.POST['password']
            admin_status = request.POST['admin_status']
            field_to_parse = int(request.POST['field_choice'])
            if not excel_file.name.endswith('.xlsx'):
                return render(request, 'index/upload.html', {'form': form, 'current_count': current_count, 'current_last_changed_date': current_last_changed_date})
            try:
                if password != '123':
                    raise Exception('Неверный пароль')
                print('c')
                count = parse_from_excel_function(excel_file, admin_status, field_to_parse)
                total_count = current_count + count

                with open('index/order_count.txt', 'w') as file:
                    file.write(str(total_count))

                new_time = datetime.now().strftime("Последнее изменение: %d.%m.%Y | Время: %H:%M:%S")
                with open('index/last_changed_date.txt', 'w') as file:
                    file.write(new_time)
                return JsonResponse({'success': True})
            except Exception as e:
                print(e)
                return JsonResponse({'success': False, 'error_message': str(e)})
        else:
            print('no')
    else:
        print('no2')
        form = LogisticForm()
    return render(request, 'index/upload.html', {'form': form, 'current_count': current_count, 'current_last_changed_date': current_last_changed_date})
