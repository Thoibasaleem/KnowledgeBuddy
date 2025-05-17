from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static
from students.views import chat_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  
    path("api/", include("students.urls")),  # All student-related API endpoints
    path("", lambda request: render(request, 'index.html'), name='index'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token
    path('chat/', chat_view, name='chat'),
    path('api/', include('students.urls')),
    path('', include('students.urls')),
]

# 🚀 Add this for serving media files during development:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
