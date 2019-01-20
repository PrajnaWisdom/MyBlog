from rest_framework import serializers
from app import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'login', 'password', 'nicename', 'email', 'registered', 'activation_key', 'display_name') 


class TermsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Terms
        fields = ('id', 'name', 'slug', 'parent')

class PostsSerializer(serializers.ModelSerializer):
    # terms = TermsSerializer(many=True)
    class Meta:
        model = models.Posts
        fields = ('id', 'author', 'post_data', 'post_content', 'post_title', 'post_excerpt', 'post_status', 'comment_status', 
        'post_modified', 'post_type', 'menu_order', 'comment_count', 'terms')

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comments
        fields = ('id', 'comment_post_ID', 'comment_author', 'comment_author_email', 'comment_author_IP', 'comment_date',
        'comment_content', 'comment_approved', 'comment_parent')

class LinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Links
        fields = ('id', 'link_url', 'link_name', 'link_description', 'link_visible')