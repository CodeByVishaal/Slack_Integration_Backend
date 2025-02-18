from rest_framework import serializers
from .models import Program

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ['id', 'title', 'description', 'severity', 'status','taxonomy']
        extra_kwargs = {
            "taxonomy": {"required": False, "allow_null": True},
        }

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance