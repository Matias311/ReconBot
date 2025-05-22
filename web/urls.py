from django.urls import path

from .views import FullAnalysisView, download_report

urlpatterns = [
    path("", FullAnalysisView.as_view(), name="full_analysis"),
    path("download-report/<int:pk>/", download_report, name="download_report"),
]
