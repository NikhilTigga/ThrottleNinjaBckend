from django.urls import path

from .accounts.views import (
    UserRegisterAPI,
    LoginAPI,
    UpdateProfileAPI,
    RefreshTokenAPI,
    CheckNicknameAvailabilityAPI
)

from .post.views import(
    CreatePostAPI,
    GetFeedAPI,
    ToggleLikeAPI,
    AddCommentAPI,
)

from .follow.views import(
    FollowUserAPI,
     UnfollowUserAPI,
     FollowingListAPI,
     FollowersListAPI,
     FriendSuggestionsAPI
)

from .profile.views import(
    UserProfileAPI
)

from .getCreateChatRoom.views import(
    getCreateChatRoomAPI
)

from .searchFriends.views import (
    SearchFriendsAPI
)

from .CheckUserExistsAPI.views import (
    CheckUserExistsAPI
)

from .chatListAPI.views import (
    ChatUserListAPI
)
from .club.clubapis import *
from django.views.decorators.csrf import csrf_exempt
from .Trip.createTripAPIs import *

urlpatterns = [
    
    path(
        "userRegister/",
        csrf_exempt(UserRegisterAPI.as_view()),
        name="userregisterapi"
    ),
    
    path(
        "userLogin/",
        csrf_exempt(LoginAPI.as_view()),
        name="userloginapi"
    ),
    
    path("updateProfileAPI/",csrf_exempt(UpdateProfileAPI.as_view()),name="updateProfileAPI"),
    
    path("createdpostapi/",csrf_exempt(CreatePostAPI.as_view()), name="createPost"),
    
    path("getfeedapi/",csrf_exempt(GetFeedAPI.as_view()),name = "getfeedapi"),
    path("togglelikeapi/",csrf_exempt(ToggleLikeAPI.as_view()),name="togglelikeapi"),
    
    path("refreshTokenAPI/",csrf_exempt(RefreshTokenAPI.as_view()),name="refreshTokenApi"),
    
    path("addCommentApi/",csrf_exempt(AddCommentAPI.as_view()), name="addComment"),
    
    path("followuserapi/",csrf_exempt(FollowUserAPI.as_view()),name="followuser"),
    path("unfollowuserapi/",csrf_exempt(UnfollowUserAPI.as_view()),name="unfollowuser"),
    
    path("userprofile/",csrf_exempt(UserProfileAPI.as_view()),name="userprofile"),
    
    path("followersListapi/",csrf_exempt(FollowersListAPI.as_view()), name="followersListapi"),
    
    path("followingListapi/",csrf_exempt(FollowingListAPI.as_view()),name="followingList"),
    
    
    path("friendSuggestionApi/",csrf_exempt(FriendSuggestionsAPI.as_view()),name = "friendSuggestion"),
    
    path("checknicknameavailability/",csrf_exempt(CheckNicknameAvailabilityAPI.as_view()),name="checknickname"),
    
    
    path("getCreateChatRoomAPI/",csrf_exempt(getCreateChatRoomAPI.as_view()),name="getCreateChatRoomAPI"),
    
    
    path("searchFriends/",csrf_exempt(SearchFriendsAPI.as_view()), name="searchFriends"),
    
    path("checkUserExistAPI/",csrf_exempt(CheckUserExistsAPI.as_view()), name="checkUserExist"),
    
    path("chatListAPI/",csrf_exempt(ChatUserListAPI.as_view()), name="chatlistapi"),
    
    path("createClubAPI/",csrf_exempt(CreateClubAPI.as_view()), name="createClubAPI"),
    
    path("joinClubAPI/",csrf_exempt(JoinClubAPI.as_view()),name='joinClubAPI'),
    
    path('approveClubJoinRequestAPI/',csrf_exempt(ApproveClubJoinRequestAPI.as_view()),name="approveClubJoinRequestAPI"),
    
    path('rejectClubJoinRequestAPI/',csrf_exempt(RejectClubJoinRequestAPI.as_view()),name="rejectClubJoinRequestAPI"),
    
    path('createTripAPI/',csrf_exempt(CreateTripAPI.as_view()),name='createTripAPI'),
    
    path("userCreatedTripListAPI/",csrf_exempt(UserCreatedTripListAPI.as_view()),name="userCreatedTripListAPI"),
    
    path("user-club-list/",csrf_exempt(UserClubListAPI.as_view()),name="user-club-list"),
    
    path("discover-clubs/",csrf_exempt(DiscoverClubAPI.as_view()),name="discover-clubs"),
    
    
    path("discover-trips/",csrf_exempt(DiscoverTripAPI.as_view()),name="discover-trips"),
    
    
]