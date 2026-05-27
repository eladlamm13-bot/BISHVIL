from django.urls import path
from .views import dashboard_stats, dashboard_report_data

urlpatterns = [
    path("dashboard/stats/", dashboard_stats, name="dashboard-stats"),
    path("dashboard/report-data/", dashboard_report_data, name="dashboard-report-data"),
]