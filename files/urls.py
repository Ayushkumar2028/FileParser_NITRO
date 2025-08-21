from django.urls import path
from .views import FileUploadView, FileProgressView, FileContentView, FileDeleteView

urlpatterns = [
    path("files", FileUploadView.as_view()),
    path("files/<uuid:file_id>/progress", FileProgressView.as_view()),
    path("files/<uuid:file_id>", FileContentView.as_view()),
    path("files/<uuid:file_id>/delete", FileDeleteView.as_view())
]