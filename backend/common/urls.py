from django.urls import path, include

from common.views import (
    OstanListApiView,
    ShahrestanListApiView,

    SherkatListApiView,
    SherkatDetailsApiView,

    HealthCheck,
)


urlpatterns = [
    path('ostan/' , OstanListApiView.as_view() , name="ostan-list"),
    path('shahrestan/' , ShahrestanListApiView.as_view() , name="shahrestan-list"),

    path('sherkat/' , SherkatListApiView.as_view() , name="sherkat-list"),
    path('sherkat/<int:sherkatid>/' , SherkatDetailsApiView.as_view() , name="sherkat-details"),

    path('healthcheck/' , HealthCheck.as_view() , name="healthcheck"),
    
]
