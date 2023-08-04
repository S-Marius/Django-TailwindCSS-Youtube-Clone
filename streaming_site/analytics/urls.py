# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('analytics-dashboard/', views.analytics_dashboard_view, name='analytics-dashboard'),
]