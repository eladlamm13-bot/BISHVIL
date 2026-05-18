from django.db import models
from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import UserSerializer

User = get_user_model()


# ---------------------------------------------------------
# 1. משתמש מחובר
# ---------------------------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


# ---------------------------------------------------------
# 2. ViewSet למשתמשים
# ---------------------------------------------------------
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = User.objects.all().order_by(
            'first_name',
            'last_name',
            'username'
        )

        role = self.request.query_params.get('role')
        region_id = self.request.query_params.get('region')
        is_active_worker = self.request.query_params.get('is_active_worker')
        search = self.request.query_params.get('search')

        # -------------------------------------------------
        # Filter by role
        # -------------------------------------------------
        if role:
            queryset = queryset.filter(role=role)

        # -------------------------------------------------
        # Filter by region
        # -------------------------------------------------
        if region_id:
            queryset = queryset.filter(region_id=region_id)

        # -------------------------------------------------
        # Filter by active worker
        # -------------------------------------------------
        if is_active_worker is not None:
            if is_active_worker.lower() == 'true':
                queryset = queryset.filter(is_active_worker=True)

            elif is_active_worker.lower() == 'false':
                queryset = queryset.filter(is_active_worker=False)

        # -------------------------------------------------
        # Search
        # -------------------------------------------------
        if search:
            queryset = queryset.filter(
                models.Q(username__icontains=search) |
                models.Q(first_name__icontains=search) |
                models.Q(last_name__icontains=search) |
                models.Q(email__icontains=search)
            )

        return queryset


# ---------------------------------------------------------
# 3. Org Users (זמנית אותו דבר)
# ---------------------------------------------------------
class OrgUserViewSet(UserViewSet):
    pass


# ---------------------------------------------------------
# 4. Dummy endpoints זמניים
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