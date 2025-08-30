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

    def update ( self, instance, validated_data):
        instance.title =validated_data.get('title', instance.title)
        instance.description= validated_data.get('description', instance.description)
        instance.goal= validated_data.get('goal', instance.goal)
        instance.image= validated_data.get('image', instance.image)
        instance.is_open = validated_data.get('is_open', instance.is_open)
        instance.save()
        return instance

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    class Meta:
        model = apps.get_model('fundraisers.Comment')
        fields = '__all__'

    def update ( self, instance, validated_data):
        instance.text =validated_data.get('text', instance.text)
        instance.save()
        # If you have already migrated and the column exists in your model,
        # the next thing to check is your database schema directly.
        # Run the following command to inspect your database:
        # python manage.py dbshell
        # Then, in the shell, run:
        # .schema fundraisers_comment
        # This will show you the columns in the fundraisers_comment table.
        # Ensure that user_id is present.

        # If user_id is missing, try running:
        # python manage.py makemigrations
        # python manage.py migrate

        # If it still doesn't work, check your migration files in fundraisers/migrations/
        # Look for any migration that adds the user field to Comment.
        # If missing, create a new migration.

        # Also, ensure your model's app label is correct and matches your database table.
