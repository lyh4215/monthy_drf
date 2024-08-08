from rest_framework import serializers
from nudge.models import Nudge

class NudgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nudge
        fields = '__all__'