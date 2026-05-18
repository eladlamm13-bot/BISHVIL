from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # טוקנים
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # משתמשים
    path('api/users/', include('users.urls')), 
    
    # אזורים
    path('api/regions/', include('regions.urls')), 

    # מקומות וסוגי מקומות
    path('api/', include('places.urls')),
    
    # משימות
    path('api/', include('tasks.urls')),

    # תוכן - הנה השורה החדשה!
    path('api/', include('content_items.urls')),
]