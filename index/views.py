from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render

from index.forms import LogisticForm

from index.utils.new_to_excel import parse_from_excel_function


def upload_file(request):
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
                return render(request, 'index/upload.html', {'form': form,})
            try:
                if password != '1234':
                    raise Exception('Неверный пароль')
                print('c')
                all_unchanged_tracks = parse_from_excel_function(excel_file, admin_status, field_to_parse)
                return JsonResponse({'success': True, 'message': 'Трек коды успешно изменены', 'all_unchanged_tracks': all_unchanged_tracks})
            except Exception as e:
                print(e)
                return JsonResponse({'success': False, 'error_message': str(e)})
        else:
            print('no')
    else:
        print('no2')
        form = LogisticForm()
    return render(request, 'index/upload.html', {'form': form})
