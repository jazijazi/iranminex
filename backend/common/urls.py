from django.urls import path, include

from common.views import (
    OstanListApiView,
    ShahrestanListApiView,

    CompanyListApiView,
    CompanyDetailsApiView,

    HealthCheck,
)


urlpatterns = [
    path('ostan/' , OstanListApiView.as_view() , name="ostan-list"),
    path('shahrestan/' , ShahrestanListApiView.as_view() , name="shahrestan-list"),

    path('company/' , CompanyListApiView.as_view() , name="company-list"),
    path('company/<int:companyid>/' , CompanyDetailsApiView.as_view() , name="company-details"),

    path('healthcheck/' , HealthCheck.as_view() , name="healthcheck"),
    
]
