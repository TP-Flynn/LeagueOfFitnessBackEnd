from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Friendship
from django.contrib.auth import get_user_model
from .serializers import FriendshipSerializer

# Send friend request
@api_view(['POST'])
def send_friend_request(request, friend_id):
    user = request.user
    friend = get_user_model().objects.get(id=friend_id)

    if user == friend:
        return Response({"error": "You cannot send a friend request to yourself."}, status=status.HTTP_400_BAD_REQUEST)
    
    friendship, created = Friendship.objects.get_or_create(user=user, friend=friend, status=Friendship.PENDING)
    
    if not created:
        return Response({"message": "Friend request already sent."}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({"message": "Friend request sent."}, status=status.HTTP_201_CREATED)

# Accept friend request
@api_view(['POST'])
def accept_friend_request(request, request_id):
    friendship = Friendship.objects.get(id=request_id)

    if friendship.friend != request.user:
        return Response({"error": "You cannot accept this request."}, status=status.HTTP_400_BAD_REQUEST)
    
    friendship.status = Friendship.ACCEPTED
    friendship.save()
    
    return Response({"message": "Friend request accepted."}, status=status.HTTP_200_OK)

# List of friends
@api_view(['GET'])
def friends_list(request):
    friends = Friendship.objects.filter(user=request.user, status=Friendship.ACCEPTED) | Friendship.objects.filter(friend=request.user, status=Friendship.ACCEPTED)
    serializer = FriendshipSerializer(friends, many=True)
    return Response(serializer.data)
