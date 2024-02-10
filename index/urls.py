from django.urls import path
from rest_framework.routers import DefaultRouter

from index import views

router = DefaultRouter()
router.register(r'upload-excel', views.FileUploadViewSet, basename='upload_excel')

urlpatterns = router.urls