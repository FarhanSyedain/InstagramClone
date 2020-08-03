from rest_framework import serializers
from Configrations.models import Post


class PostSerilizer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = '__all__'