from django.urls import path, include

from initialborders.views.initialborders import (
    InitialBorderListViews,
    InitialBorderDetailViews,
    InitialBorderDownloadExportShape,
    AllInitialBorderDownloadExportShape,
    #attahcment
    InitialBorderAttachmentListView,
    InitialBorderAttachmentDetailView,
)
from initialborders.views.domains import (
    InitialBorderDominListView,
    InitialBorderDominDetailsView,

    InitialBorderMadeDominListView,
    InitialBorderMadeDominDetailsView,

    InitialBorderAttachmentDomainListApiView,
    InitialBorderAttachmentDomainDetailsApiView,
)


urlpatterns = [
    path('' , InitialBorderListViews.as_view() , name="initialborder-list"), 
    path('<int:pk>/' , InitialBorderDetailViews.as_view() , name="initialborder-detail"),
    path('<int:pk>/downloadexportshape/' , InitialBorderDownloadExportShape.as_view() , name="initialborder-downloadexportshape"),
    path('downloadallexportshape/' , AllInitialBorderDownloadExportShape.as_view() , name="initialborder-downloadallexportshape"),
    path('<int:initialborderpk>/attachments/' , InitialBorderAttachmentListView.as_view() , name="initialborder-atach-list"),
    path('attachment/<int:attachmentpk>/' , InitialBorderAttachmentDetailView.as_view() , name="initialborder-atach-detail"),
    
    # domains
    path('domins/' , InitialBorderDominListView.as_view() , name="initialborderdomins-list"),
    path('domins/<int:id>/' , InitialBorderDominDetailsView.as_view() , name="initialborderdomins-detail"),
    path('made-domins/' , InitialBorderMadeDominListView.as_view() , name="initialbordermade-domins-list"),
    path('made-domins/<int:id>/' , InitialBorderMadeDominDetailsView.as_view() , name="initialbordermade-domins-detail"),
    path('attach-domains/' , InitialBorderAttachmentDomainListApiView.as_view() , name="initialborder-atach-domain-list"),
    path('attach-domains/<int:id>/' , InitialBorderAttachmentDomainDetailsApiView.as_view() , name="initialborder-atach-domain-detail"),
]
