from rest_framework import serializers
from .models import Region

class RegionSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = Region
        fields = '__all__'

    def get_tasks(self, obj):
        # ביצוע Import בתוך הפונקציה כדי למנוע יבוא מעגלי (Circular Import) מול משימות
        from tasks.serializers import TaskSerializer
        tasks = obj.tasks.all()
        return TaskSerializer(tasks, many=True).data

        