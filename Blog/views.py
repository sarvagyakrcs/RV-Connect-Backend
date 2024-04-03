from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, generics, filters, permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from .models import Post, Comments, Friendship, FriendRequest, ChatRoom
from .serializers import (
    PostSerializer,
    CommentsSerializer,
    FriendshipSerializer,
    FriendRequestSerializer,
    UserSerializer,
)
from rest_framework.views import APIView
from .models import UserProfilePic, Like
from .serializers import UserProfilePicSerializer
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .models import Group, Membership
from .serializers import GroupSerializer, MembershipSerializer, LikeSerializer
from .serializers import ChatRoomSerializer, PostLikeSerializer

class PostLikeCountView(APIView):
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostLikeSerializer(post)
        return Response(serializer.data)

class ChatRoomListCreateView(generics.ListCreateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

class ChatRoomRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

# firebase
# from django.http import JsonResponse
# from firebase_admin import firestore

# def fetch_data_from_firebase(request):
#     # Initialize Firebase Firestore
#     db = firestore.client()

#     # Example: Fetch data from a Firebase collection
#     firebase_data = db.collection('your_collection').get()

#     # Process data and convert to JSON
#     data_list = [doc.to_dict() for doc in firebase_data]

#     return JsonResponse(data_list, safe=False)


# Likes
class LikeListCreateView(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LikeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

class LikesCountView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        post_id = self.kwargs.get('pk')
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        likes_count = Like.objects.filter(post=post).count()
        return Response({"likes_count": likes_count})


from rest_framework.views import APIView
class BranchList(APIView):
    def get(self, request, format=None):
        branches = UserProfilePic.objects.values_list('branch', flat=True).distinct()
        serializer = UserProfilePicSerializer({'branch': branches}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email', '')

        # if not (email.endswith('@rvce.edu.in') or email.endswith('rvu.edu.in')):
        #     return Response({'detail': 'Email must end with @rvce.edu.in or rvu.edu.in'}, status=status.HTTP_400_BAD_REQUEST)

        # email_ids = [
        #     "daivikshenoy.cs23@rvce.edu.in",
        #     "bhuvaneshb.cd23@rvce.edu.in",
        #     "soumikh.bsc23@rvu.edu.in",
        #     "tejasr.cv22@rvce.edu.in",
        #     "hardikgd.ee23@rvce.edu.in",
        #     "adithyaganacharmj.ec22@rvce.edu.in",
        #     "jeevans.cs22@rvce.edu.in",
        #     "adarshs.cy22@rvce.edu.in",
        #     "ayushojha.cd22@rvce.edu.in",
        #     "anoushkad.cd22@rvce.edu.in",
        #     "vishnusingh.et22@rvce.edu.in",
        #     "tarunhs.cd22@rvce.edu.in",
        #     "mukundverma.cd22@rvce.edu.in",
        #     "prakharjain.cd22@rvce.edu.in",
        #     "sarvagyakumar.cd22@rvce.edu.in"
        # ]

        # if email not in email_ids:
        #     return Response({'detail': 'Email must end with @rvce.edu.in or rvu.edu.in'}, status=status.HTTP_400_BAD_REQUEST)


        hashed_password = make_password(request.data['password'])
        request.data['password'] = hashed_password
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'detail': f'User registered successfully: {user}'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve_by_username(self, request, *args, **kwargs):
        username = kwargs.get('pk')
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def retrieve_by_email(self, request, *args, **kwargs):
        email = kwargs.get('pk')  # Assuming the email is passed as 'pk'
        user = get_object_or_404(User, email=email)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class UserProfilePicListCreateView(generics.ListCreateAPIView):
    queryset = UserProfilePic.objects.all()
    serializer_class = UserProfilePicSerializer

class UserProfilePicDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfilePic.objects.all()
    serializer_class = UserProfilePicSerializer

from rest_framework.views import APIView
class UserProfilePicByUsernameView(APIView):
    def get(self, request, username, format=None):
        user_profile = get_object_or_404(UserProfilePic, user__username=username)
        serializer = UserProfilePicSerializer(user_profile)
        return Response(serializer.data)

    def update(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        email = request.data.get('email', '')

        if not email.endswith('@rvce.edu.in'):
            return Response({'detail': 'Email must end with @rvce.edu.in'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfilePicByEmailView(APIView):
    def get(self, request, email, format=None):
        user_profile = get_object_or_404(UserProfilePic, user__email=email)
        serializer = UserProfilePicSerializer(user_profile)
        return Response(serializer.data)

    def put(self, request, email, format=None):
        user_profile = get_object_or_404(UserProfilePic, user__email=email)
        serializer = UserProfilePicSerializer(user_profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    from django.shortcuts import get_object_or_404
    from django.http import Http404

    def retrieve(self, request, pk=None):
        try:
            # Try to retrieve by primary key (ID) first
            user = get_object_or_404(User, pk=pk)
        except (Http404, ValueError):
            # If not found or if pk is not a valid number, try to retrieve by username
            user = get_object_or_404(User, username=pk)

        serializer = UserSerializer(user)
        return Response(serializer.data)

    def retrieve_by_userid(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def retrieve_by_username(self, request, pk=None):
        user = get_object_or_404(User, username=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'])
    def find_user(self, request):
        username = request.query_params.get('username', None)
        if username:
            users = User.objects.filter(username=username)
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'])
    def user_details(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-date_posted')[:100]
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            mentioned_user_info = request.data.get('mentioned_user')
            mentioned_user = None

            if isinstance(mentioned_user_info, int):
                try:
                    mentioned_user = User.objects.get(pk=mentioned_user_info)
                except User.DoesNotExist:
                    mentioned_user = None
            elif isinstance(mentioned_user_info, str):
                try:
                    mentioned_user = User.objects.get(username=mentioned_user_info)
                except User.DoesNotExist:
                    mentioned_user = None

            serializer.validated_data['author'] = request.user
            serializer.validated_data['mentioned_user'] = mentioned_user
            post = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieveByID(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def update(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication required to create a comment.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        request.data['user_commented'] = request.user.pk

        serializer = CommentsSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            comment = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        comments = Comments.objects.filter(user_commented__username=pk)
        serializer = CommentsSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def comments_on_post(self, request, post_id=None):
        comments = Comments.objects.filter(post_id=post_id)
        serializer = CommentsSerializer(comments, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            comment = Comments.objects.get(pk=pk)

            if comment.user_commented != request.user:
                return Response({'detail': 'You do not have permission to delete this comment.'},
                                status=status.HTTP_403_FORBIDDEN)

            comment_data = CommentsSerializer(comment).data
            comment.delete()

            if not Comments.objects.filter(pk=pk).exists():
                return Response({'detail': 'Comment deleted successfully', 'comment': comment_data},
                                status=status.HTTP_200_OK)
            else:
                print(f"Warning: Comment with ID {pk} still exists after deletion.")
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Comments.DoesNotExist:
            return Response({'detail': 'The comment does not exist.'},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Exception during comment deletion: {e}")
            return Response({'detail': f'An error occurred during comment deletion. {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FriendshipViewSet(viewsets.ModelViewSet):
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer

class FriendRequestViewSet(viewsets.ModelViewSet):
    serializer_class = FriendRequestSerializer
    queryset = FriendRequest.objects.all()
    def create(self, request, *args, **kwargs):
        sender = request.user.id
        data = request.data.copy()
        data['sender'] = sender
        serializer = FriendRequestSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def received_requests(self, request):
        try:
            # Get all friend requests received by the user
            received_requests = FriendRequest.objects.filter(receiver=request.user)

            # Serialize the friend requests
            serializer = FriendRequestSerializer(received_requests, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'])
    def sent_requests(self, request):
        try:
            # Get all friend requests sent by the user
            sent_requests = FriendRequest.objects.filter(sender=request.user)

            # Serialize the friend requests
            serializer = FriendRequestSerializer(sent_requests, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['POST'])
    def accept_request(self, request, pk=None):
        try:
            friend_request = self.get_object()

            # Check if the friend request is pending
            if friend_request.status == 'pending' or 'Pending' or ('pending', 'Pending') or ["pending", "Pending"]:
                # Create a friendship object for the accepted request
                friendship = Friendship(user=friend_request.receiver, friend=friend_request.sender, status='accepted')
                friendship.save()

                # Delete the friend request from the database
                friend_request.delete()

                return Response({'detail': 'Friend request accepted and saved as friendship.'},
                                status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Friend request is not pending.'}, status=status.HTTP_400_BAD_REQUEST)
        except FriendRequest.DoesNotExist:
            return Response({'detail': 'Friend request not found.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['POST'])
    def reject_request(self, request, pk=None):
        try:
            friend_request = self.get_object()

            # Check if the friend request is pending
            if friend_request.status == 'pending' or 'Pending' or ('pending', 'Pending') or ["pending", "Pending"]:
                # Delete the friend request from the database
                friend_request.delete()

                return Response({'detail': 'Friend request rejected and removed.'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Friend request is not pending.'}, status=status.HTTP_400_BAD_REQUEST)
        except FriendRequest.DoesNotExist:
            return Response({'detail': 'Friend request not found.'}, status=status.HTTP_404_NOT_FOUND)

class FriendshipViewSet(viewsets.ModelViewSet):
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer



class FriendsByUsernameView(generics.ListAPIView):
    serializer_class = FriendshipSerializer

    def get_queryset(self):
        # Get the user by username
        username = self.kwargs['username']
        user = User.objects.get(username=username)

        # Get the user's friends
        return Friendship.objects.filter(user=user, status='accepted')

class UserSearchView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']


class MentionedPostsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        return Post.objects.filter(mentioned_user=user)

class PostByAuthorViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        return Post.objects.filter(author=user)

class UserFriendsView(APIView):
    def get(self, request, user_id, *args, **kwargs):
        friends1 = Friendship.objects.filter(user__id=user_id, status='accepted')
        friends2 = Friendship.objects.filter(friend__id=user_id, status='accepted')

        all_friends = friends1 | friends2
        serializer = FriendshipSerializer(all_friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class GroupListCreateView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class MembershipListCreateView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer

class MembershipDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer

class UserGroupsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        memberships = Membership.objects.filter(user=user)
        serializer = MembershipSerializer(memberships, many=True)
        groups = serializer.data

        return Response(groups, status=status.HTTP_200_OK)


from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(
    responses={
        200: "Success",
        400: "Bad Request",
        404: "Not Found",
    },
    operation_description="Description",
)
def your_view_name(self, request):
    pass
