from django.urls import path
from accounts.views.views import (
    LoginUser,
    RefreshToken,
    LogoutUser,
    UserProfile,
    UserContracts,
    NotificationListApiViews,
    NotificationDetailsApiViews,
    ChangePassword,
)

from accounts.views.userpermsviews import (
    ApisListApiViews,
    ApisDetailApiViews,
    ToolsListApiViews,
    ToolsDetailApiViews,
    RolesListApiViews,
    RolesDetailApiViews
)

from accounts.views.usermanagemetviews import (
    UserManagementListApiView,
    UserManagementDetailsApiView,
)

from django.conf import settings
from django.conf.urls.static import static

app_name = 'accounts'

# prefix is auth (in url.py) 
urlpatterns = [
    # path('refresh/', RefreshToken.as_view()),
    path('login/', LoginUser.as_view(),name="login"),
    path('refresh/',RefreshToken.as_view(),name="refresh"),
    path('logout/', LogoutUser.as_view(),name="logout"),
    path('userprofile/',UserProfile.as_view(),name="userprofile"),
    path('usercontracts/',UserContracts.as_view(),name="user-contract-list"),
    path('changepassword/',ChangePassword.as_view(),name="chngpass"),


    path('notification/' , NotificationListApiViews.as_view() , name='user-notification-list'),
    path('notification/<int:notifid>/' , NotificationDetailsApiViews.as_view() , name='user-notification-details'),

    path('usermanagement/',UserManagementListApiView.as_view(),name="user-managemant-list"),
    path('usermanagement/<int:userid>/',UserManagementDetailsApiView.as_view(),name="user-managemant-detail"),


    path('apis/',ApisListApiViews.as_view(),name="apis-list"),
    path('apis/<int:apiid>/',ApisDetailApiViews.as_view(),name="apis-detail"),
    path('tools/',ToolsListApiViews.as_view(),name="tools-list"),
    path('tools/<int:toolid>/',ToolsDetailApiViews.as_view(),name="tools-detail"),
    path('roles/',RolesListApiViews.as_view(),name="roles-list"),
    path('roles/<int:roleid>/',RolesDetailApiViews.as_view(),name="roles-detail"),
]
