from django.contrib.auth.views import PasswordResetView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    UserViewSet,
    PostViewSet,
    FriendshipViewSet,
    FriendRequestViewSet,
    PostByAuthorViewSet,
    CommentsViewSet,
    UserSearchView, FriendsByUsernameView, UserProfilePicListCreateView, UserProfilePicDetailView,
    UserProfilePicByUsernameView,
    UserProfilePicByEmailView,
    MentionedPostsViewSet,
    UserFriendsView,
    PostLikeCountView
)
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from . import views



router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
# router.register(r'friendships', FriendshipViewSet)
router.register(r'comments', CommentsViewSet)
router.register(r'friend-requests', FriendRequestViewSet, basename='friendrequest')
router.register(r'friendships', FriendshipViewSet)
router.register(r'mentioned-posts', MentionedPostsViewSet, basename='mentioned-posts')

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += [
    # firebase
    # path('fetch-data-from-firebase/', views.fetch_data_from_firebase, name='fetch_data_from_firebase'),
    # firebase-close

    # chatroom
    path('chatrooms/', views.ChatRoomListCreateView.as_view(), name='chatroom-list-create'),
    path('chatrooms/<int:pk>/', views.ChatRoomRetrieveUpdateDestroyView.as_view(), name='chatroom-detail'),

    # likes
    path('likes/', views.LikeListCreateView.as_view(), name='like-list-create'),
    path('likes/<int:pk>/', views.LikeDetailView.as_view(), name='like-detail'),
    path('likes/count/<int:pk>/', views.LikesCountView.as_view(), name='likes-count'),

    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('api/users/search/', UserSearchView.as_view(), name='user-search'), #http://localhost:8000/api/users/search/?search=<name>/<email>
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    # path('friend-requests/received/<str:user_identifier>/', FriendRequestViewSet.as_view({'get': 'received'}), name='received-friend-requests'),
    # path('friend-requests/sent/<str:user_identifier>/', FriendRequestViewSet.as_view({'get': 'sent'}), name='sent-friend-requests'),
    path('', include(router.urls)),
    path('users/<int:pk>/user-details/', UserViewSet.as_view({'get': 'user_details'}), name='user-details'),
    path('comments/comments_on_post/<int:post_id>/', CommentsViewSet.as_view({'get': 'comments_on_post'}),
         name='comments-on-post'),
    path('users/by-userid/<int:pk>/', UserViewSet.as_view({'get': 'retrieve_by_userid'}), name='user-retrieve-by-userid'),
    path('users/by-username/<str:pk>/', UserViewSet.as_view({'get': 'retrieve_by_username'}), name='user-retrieve-by-username'),
    path('api/friends/by-username/<str:username>/', FriendsByUsernameView.as_view(), name='friends-by-username'),
    path('profile-pics/', UserProfilePicListCreateView.as_view(), name='profile-pic-list-create'),
    path('profile-pics/<int:pk>/', UserProfilePicDetailView.as_view(), name='profile-pic-detail'),
    path('profile-pics/by-username/<str:username>/', UserProfilePicByUsernameView.as_view(),
         name='profile-pic-by-username'),
    path('profile-pics/by-email/<str:email>/', UserProfilePicByEmailView.as_view(),
         name='profile-pic-by-email'),
    path('api/mentioned-posts/<str:username>/', MentionedPostsViewSet.as_view({'get': 'list'}), name='mentioned-posts-by-username'),
    path('api/posts-by-author/<str:username>/', PostByAuthorViewSet.as_view({'get': 'list'}), name='post-by-author'),
    path('user-friends/<int:user_id>/', UserFriendsView.as_view(), name='user-friends'),
    path('groups/', views.GroupListCreateView.as_view(), name='group-list'),
    path('groups/<int:pk>/', views.GroupDetailView.as_view(), name='group-detail'),
    path('memberships/', views.MembershipListCreateView.as_view(), name='membership-list'),
    path('memberships/<int:pk>/', views.MembershipDetailView.as_view(), name='membership-detail'),
    path('user-groups/', views.UserGroupsView.as_view(), name='user-groups'),
    path('api/branches/', views.BranchList.as_view(), name='branch-list'),
    path('posts/<int:post_id>/likes/', PostLikeCountView.as_view(), name='post-like-count'),
]

'''
    Create User: POST /users/
    Retrieve User: GET /users/{user_id}/
    Update User: PUT /users/{user_id}/
    Delete User: DELETE /users/{user_id}/
    Find User: GET /users/find_user/?username={username}
    /users/by-userid/{pk}/: Retrieves a user by userid.
    /users/by-username/{pk}/: Retrieves a user by username.
'''

'''
    List all posts: GET /posts/
    Create a new post: POST /posts/
    Retrieve a specific post: GET /posts/{post_id}/
    Update a specific post: PUT /posts/{post_id}/
    Partially update a specific post: PATCH /posts/{post_id}/
    Delete a specific post: DELETE /posts/{post_id}/
'''

'''
    Create Comment:
    HTTP Method: POST
    URL: /comments/
    Action Method: create
    Retrieve Comment by ID or Author's Username:

    HTTP Method: GET
    URL (by Comment ID): /comments/{comment_id}/
    URL (by Author's Username): /comments/{author_username}/
    Action Method: retrieve
    Update Comment by ID:

    HTTP Method: PUT or PATCH
    URL: /comments/{comment_id}/
    Action Method: update
    Delete Comment by ID:

    HTTP Method: DELETE
    URL: /comments/{comment_id}/
    Action Method: destroy
    List Comments (All Comments):

    HTTP Method: GET
    URL: /comments/
    Action Method: list
'''

'''
    List all friend requests: GET /api/friend-requests/
    Create a new friend request: POST /api/friend-requests/
    Retrieve a specific friend request: GET /api/friend-requests/{request_id}/
    /friend-requests/sent_requests/: Retrieves friend requests where the user is the sender.
    /friend-requests/received_requests/: Retrieves friend requests where the user is the receiver.
'''

'''
    Create: POST to /api/friendships/
    Read (List): GET to /api/friendships/
    Read (Detail): GET to /api/friendships/{friendship_id}/
    Update: PUT or PATCH to /api/friendships/{friendship_id}/
    Delete: DELETE to /api/friendships/{friendship_id}/
    retrieve a user's friends by specifying their username in the URL, like /api/friends/by-username/{username}/.

'''