# serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Post, Comments, Friendship, FriendRequest, UserProfilePic
from .models import Group, Membership, Like
from .models import ChatRoom

class PostLikeSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'likes_count']

    def get_likes_count(self, obj):
        # Count the number of likes for the post
        return Like.objects.filter(post=obj).count()

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')

class UserField(serializers.RelatedField):
    def to_internal_value(self, data):
        try:
            return User.objects.get(pk=int(data))
        except (ValueError, User.DoesNotExist):
            try:
                return User.objects.get(username=data)
            except User.DoesNotExist:
                raise serializers.ValidationError("User not found")

    def to_representation(self, obj):
        return obj.username

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    mentioned_user = UserField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Post
        fields = ('id', 'mentioned_user', 'content', 'date_posted', 'author', 'color_code')

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = "__all__"

    def create(self, validated_data):
        user_commented_username = validated_data.pop('user_commented', None)
        if user_commented_username is not None:
            try:
                user_commented = User.objects.get(username=user_commented_username)
                validated_data['user_commented'] = user_commented
                comment = Comments.objects.create(**validated_data)

                return comment
            except User.DoesNotExist:
                raise serializers.ValidationError("User with username {} does not exist".format(user_commented_username))
        else:
            raise serializers.ValidationError("Invalid user_commented data")



class FriendshipSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    friend = UserSerializer(read_only=True)

    class Meta:
        model = Friendship
        fields = ('friendship_id', 'user', 'friend', 'status', 'created_at')

class FriendRequestSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    receiver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = FriendRequest
        fields = ('request_id', 'sender', 'receiver', 'status', 'created_at')


class UserProfilePicSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfilePic
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = '__all__'


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = '__all__'  # Add specific fields if needed


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
