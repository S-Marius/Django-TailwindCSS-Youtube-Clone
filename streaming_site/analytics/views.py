from django.shortcuts import render

# Create your views here.
def analytics_dashboard_view(request):
    return render(request, 'analytics_dashboard.html')