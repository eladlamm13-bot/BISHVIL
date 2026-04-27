from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# ייבוא כל הפונקציות מאפליקציית משתמשים 
from users.views import (
    current_user, 
    UserViewSet, 
    OrgUserViewSet, 
    system_notifications,
    task_views_dummy,
    org_user_dummy,
    check_calendar_dummy,
    upsert_org_user_dummy  # <--- הוספנו את זה
)

# ייבוא משאר האפליקציות
from projects.views import ProjectViewSet
from tasks.views import TaskViewSet, ProjectTaskViewSet
from regions.views import RegionViewSet, PlaceViewSet

# בניית הראוטר האוטומטי
router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'project-tasks', ProjectTaskViewSet, basename='project-task')
router.register(r'regions', RegionViewSet, basename='region')
router.register(r'places', PlaceViewSet, basename='place')
router.register(r'users', UserViewSet, basename='user')
router.register(r'org-users', OrgUserViewSet, basename='org-user')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # נתיבים עבור מערכת ההתחברות והטוקנים
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # זיהוי משתמש והתראות
    path('api/users/me/', current_user, name='current_user'),
    path('api/system-notifications/', system_notifications, name='system_notifications'),
    
    # כדורי ההרגעה לריאקט 
    path('api/task-views/', task_views_dummy, name='task_views_dummy'),
    path('api/users/me/org-user/', org_user_dummy, name='org_user_dummy'),
    path('api/functions/checkCalendarConnection/', check_calendar_dummy, name='check_calendar_dummy'),
    path('api/functions/upsertOrgUser/', upsert_org_user_dummy, name='upsert_org_user_dummy'), # <--- הנתיב החדש!
    
    # הוספת כל שאר הנתיבים של הראוטר
    path('api/', include(router.urls)),
]