from rest_framework import serializers
from instagram.models import InstagramPost, InstagramComment


class InstagramPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramPost
        fields = ["full_text", "post_id", "user_id", "name", "screen_name"]


class InstagramCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramComment
        fields = ["full_text", "post_id", "user_id", "name", "screen_name"]
