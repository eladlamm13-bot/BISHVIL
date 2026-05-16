from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()

# ---------------------------------------------------------
# 1. משתמש מחובר (מתוקן)
# ---------------------------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user

    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name or '',
        'last_name': user.last_name or '',
        'phone': getattr(user, 'phone', ''),
        'is_active': user.is_active,
        'is_superuser': user.is_superuser,
        'is_staff': user.is_staff,
        'role': user.role,  # 👈 עכשיו נכון!
    })


# ---------------------------------------------------------
# 2. ViewSets למשתמשים
# ---------------------------------------------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class OrgUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


# ---------------------------------------------------------
# 3. Dummy endpoints (כמו שהיה)
# ---------------------------------------------------------
@api_view(['GET'])
def system_notifications(request):
    return Response([])


@api_view(['GET'])
def task_views_dummy(request):
    return Response([])


@api_view(['GET', 'PATCH'])
def org_user_dummy(request):
    return Response({
        "id": 1,
        "first_name": "מעוז",
        "last_name": "דמרי",
        "phone": "0547695452",
        "is_profile_complete": True
    })


@api_view(['POST'])
def check_calendar_dummy(request):
    return Response({"connected": False})


@api_view(['POST'])
def upsert_org_user_dummy(request):
    return Response({
        "success": True,
        "message": "User updated successfully"
    })