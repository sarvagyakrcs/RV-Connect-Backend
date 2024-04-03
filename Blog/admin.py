from django.contrib import admin
from Blog.models import Post, Comments, Friendship, FriendRequest, UserProfilePic, Group, Membership, Like, ChatRoom

admin.site.register(Post)
admin.site.register(Comments)
admin.site.register(Friendship)
admin.site.register(FriendRequest)
admin.site.register(UserProfilePic)
admin.site.register(Group)
admin.site.register(Membership)
admin.site.register(Like)
admin.site.register(ChatRoom)