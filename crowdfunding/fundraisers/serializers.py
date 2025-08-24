from rest_framework import serializers
from django.apps import apps

class FundraiserSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source= 'owner.id')
    progress = serializers.ReadOnlyField()

    class Meta:
        model = apps.get_model ('fundraisers.Fundraiser')
        fields = '__all__'
        def get_progress(self, obj):
            return obj.progress()

class PledgeSerializer(serializers.ModelSerializer):
    supporter = serializers.ReadOnlyField (source ='supporter.id')

    class Meta:
        model = apps.get_model('fundraisers.Pledge')
        fields = '__all__'

class FundraiserDetailSerializer(FundraiserSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField (source='user.id')
    class Meta:
        model = apps.get_model('fundraisers.Comment')
        fields = '__all__'


