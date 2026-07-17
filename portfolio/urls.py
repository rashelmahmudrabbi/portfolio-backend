from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def health(request):
    return JsonResponse({'ok': True})


def root(request):
    return JsonResponse({
        'status': 'ok',
        'message': 'Portfolio API is running',
        'endpoints': {
            'admin': '/admin/',
            'health': '/api/health',
            'api': '/api/',
        }
    })


urlpatterns = [
    path('', root),
    path('admin/', admin.site.urls),
    path('api/health', health),
    path('api/', include('content.urls')),
]
