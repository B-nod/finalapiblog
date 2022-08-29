from dataclasses import fields
import json
from rest_framework import serializers
from .models import *

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['user_id', 'comment']

class PostSerializer(serializers.ModelSerializer):
    poster = serializers.ReadOnlyField(source='poster.username')
    poster_id = serializers.ReadOnlyField(source='poster.id')
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'description','image', 'poster','poster_id', 'created', 'comments']
    
    def get_comments(self, post):

        data = Comment.objects.filter(post=post).values('user_id', 'user__username', 'comment')
        return data

    

