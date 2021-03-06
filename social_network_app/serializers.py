from django.contrib.auth.models import User
from rest_framework import serializers
from social_network_app.models import Post, Like, Profile


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], password=validated_data['password']
        )
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'posts', 'last_login']
        extra_kwargs = {'last_login': {'read_only': True}}


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = [
            'url', 'id', 'owner', 'title',
            'content', 'created_at', 'likes',
        ]
        extra_kwargs = {
            'owner': {'read_only': True},
            'created_at': {'read_only': True},
            'likes': {'required': False, 'read_only': True}
        }


class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = ['id', 'post', 'owner', 'created_at']
        extra_kwargs = {
            'owner': {'required': False, 'read_only': True},
            'created_at': {'read_only': True}
        }


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Profile
        fields = ['user', 'last_activity']
        extra_kwargs = {'last_activity': {'read_only': True}}
