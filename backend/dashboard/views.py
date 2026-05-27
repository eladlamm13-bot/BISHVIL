from collections import Counter
from datetime import timedelta

from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from tasks.models import Task
from projects.models import Project
from regions.models import Region
from places.models import Place
from content_items.models import ContentItem


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):

    today = timezone.localdate()
    week_from_today = today + timedelta(days=7)

    User = get_user_model()

    active_tasks = Task.objects.exclude(
        status__in=["completed", "cancelled"]
    ).count()

    active_projects = Project.objects.filter(
        status="active"
    ).count()

    urgent_tasks = Task.objects.filter(
        priority="high"
    ).exclude(
        status__in=["completed", "cancelled"]
    ).count()

    total_content = ContentItem.objects.count()

    regions = [
        {
            "id": region.id,
            "name": region.name
        }
        for region in Region.objects.all().order_by("name")
    ]

    users = [
        {
            "id": user.id,
            "full_name": (
                getattr(user, "full_name", None)
                or user.get_full_name()
                or user.username
            ),
        }
        for user in User.objects.filter(
            is_active=True
        ).order_by("id")
    ]

    projects_list = [
        {
            "id": project.id,
            "name": project.name,
            "regionId": project.region.id if project.region else None,
            "region": project.region.name if project.region else "",
            "status": project.get_status_display(),
            "priority": "",
            "project_type": "",
        }
        for project in Project.objects.select_related(
            "region"
        ).all().order_by("-created_at")
    ]

    places_list = [
        {
            "id": place.id,
            "name": place.name,
            "regionId": place.region.id if place.region else None,
            "region": place.region.name if place.region else "",
            "address": place.address or "",
            "type": (
                place.place_type.name
                if place.place_type
                else ""
            ),
            "responsible_user_name": "",
        }
        for place in Place.objects.select_related(
            "region",
            "place_type"
        ).all().order_by("name")
    ]

    due_soon_tasks = [
        {
            "id": task.id,
            "title": task.title,
            "assigneeName": (
                task.assigned_to.get_full_name()
                or task.assigned_to.username
                if task.assigned_to
                else "-"
            ),
            "dueDate": (
                task.due_date.isoformat()
                if task.due_date
                else None
            ),
            "priority": task.get_priority_display(),
        }
        for task in Task.objects.select_related(
            "assigned_to"
        ).filter(
            due_date__gte=today,
            due_date__lte=week_from_today
        ).exclude(
            status__in=["completed", "cancelled"]
        ).order_by("due_date")[:10]
    ]

    content_counter = Counter(
        ContentItem.objects.values_list(
            "content_type",
            flat=True
        )
    )

    content_data = [
        {
            "name": content_type,
            "value": count
        }
        for content_type, count in content_counter.items()
    ]

    top_projects = []

    for project in Project.objects.select_related(
        "region"
    ).prefetch_related("tasks").all():

        total_tasks = project.tasks.count()

        completed_tasks = project.tasks.filter(
            status="completed"
        ).count()

        progress = (
            round((completed_tasks / total_tasks) * 100)
            if total_tasks
            else 0
        )

        top_projects.append({
            "id": project.id,
            "name": project.name,
            "regionId": (
                project.region.id
                if project.region
                else None
            ),
            "region": (
                project.region.name
                if project.region
                else ""
            ),
            "totalTasks": total_tasks,
            "completedTasks": completed_tasks,
            "progress": progress,
        })

    top_projects = sorted(
        top_projects,
        key=lambda item: item["progress"],
        reverse=True
    )[:5]

    user_stats = []

    for user in User.objects.filter(
        is_active=True
    ).order_by("id"):

        tasks = Task.objects.select_related(
            "region",
            "project"
        ).filter(
            assigned_to=user
        )

        total = tasks.count()

        completed = tasks.filter(
            status="completed"
        ).count()

        in_progress = tasks.filter(
            status="in_progress"
        ).count()

        new = tasks.filter(
            status="new"
        ).count()

        completion_rate = (
            round((completed / total) * 100)
            if total
            else 0
        )

        user_tasks = [
            {
                "id": task.id,
                "title": task.title,
                "status": task.get_status_display(),
                "priority": task.get_priority_display(),
                "regionId": (
                    task.region.id
                    if task.region
                    else None
                ),
                "regionName": (
                    task.region.name
                    if task.region
                    else "-"
                ),
                "projectName": (
                    task.project.name
                    if task.project
                    else "-"
                ),
                "due_date": (
                    task.due_date.isoformat()
                    if task.due_date
                    else None
                ),
            }
            for task in tasks.order_by("-created_at")
        ]

        user_stats.append({
            "userId": user.id,
            "userName": (
                getattr(user, "full_name", None)
                or user.get_full_name()
                or user.username
            ),
            "total": total,
            "completed": completed,
            "inProgress": in_progress,
            "new": new,
            "completionRate": completion_rate,
            "tasks": user_tasks,
        })

    data = {
        "summary": {
            "activeTasks": active_tasks,
            "activeProjects": active_projects,
            "urgentTasks": urgent_tasks,
            "totalContent": total_content,
        },

        "regions": regions,
        "users": users,
        "projectsList": projects_list,
        "placesList": places_list,
        "userStats": user_stats,
        "dueSoonTasks": due_soon_tasks,
        "contentData": content_data,
        "placesCount": Place.objects.count(),
        "topProjects": top_projects,
    }

    return Response(data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_report_data(request):

    report_type = request.GET.get("reportType")
    region_id = request.GET.get("regionId")
    manager_id = request.GET.get("managerId")

    queryset = Task.objects.select_related(
        "assigned_to",
        "region",
        "project"
    ).all()

    if region_id and region_id != "all":
        queryset = queryset.filter(
            region_id=region_id
        )

    if manager_id and manager_id != "all":
        queryset = queryset.filter(
            assigned_to_id=manager_id
        )

    data = []

    if report_type == "tasks_status":

        for task in queryset.order_by("-created_at"):

            data.append({
                "id": task.id,
                "title": task.title,
                "status": task.get_status_display(),

                "assignee": (
                    task.assigned_to.get_full_name()
                    or task.assigned_to.username
                    if task.assigned_to
                    else "-"
                ),

                "region": (
                    task.region.name
                    if task.region
                    else "-"
                ),

                "project": (
                    task.project.name
                    if task.project
                    else "-"
                ),

                "date": (
                    task.due_date.strftime("%d/%m/%Y")
                    if task.due_date
                    else "-"
                ),
            })

    return Response({
        "success": True,
        "data": data
    })