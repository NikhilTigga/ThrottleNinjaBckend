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


from django.views.decorators.csrf import csrf_exempt

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
]