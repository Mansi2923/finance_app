from django.urls import path
from .views import home, download_report  # Make sure download_report is imported

urlpatterns = [
    path('', home, name='home'),  # Assuming this is the home page
    path('download-report/', download_report, name='download_report'),  # Correct path for the download report view
]
