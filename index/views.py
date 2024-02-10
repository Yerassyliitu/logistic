from rest_framework import status, viewsets
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response

from index.serializer import FileUploadSerializer
from index.utils.new_to_excel import parse_from_excel_function


class FileUploadViewSet(viewsets.ViewSet):
    serializer_class = FileUploadSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            excel_file = serializer.validated_data['file']
            if not excel_file.name.endswith('.xlsx'):
                return Response({'error': 'Пожалуйста, загрузите файл с расширением .xlsx'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                parse_from_excel_function(excel_file)  # Вызываем функцию для обработки файла
                return Response({'success': 'Файл успешно обработан'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
