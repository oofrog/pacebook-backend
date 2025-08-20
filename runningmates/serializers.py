from rest_framework import serializers
from .models import RunningMate

class RunningMateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RunningMate
        fields = '__all__'
