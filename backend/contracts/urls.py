from django.urls import path, include

from contracts.views.contractviews import (
    ContractListApiViews,
    ContractDetailsApiViews,

    ContractElhaghyeListApiViews,
    ContractElhaghyeDetailsApiViews,

    ContractDomainsListApiView,

    ContractBorderListApiView,
    ContractBorderDetailsApiView,
    ContractBorderDownloadExportShapeApiViews,
    AllContractBorderDownloadExportShapeApiViews,
)
from contracts.views.sharhkhadamatviews import (
    SharhkhadamatListApiView,
    SharhkhadamatDetailApiView,

    SharhKhadamatLayerListApiView,
    SharhKhadamatLayerDetailApiView,
)
from contracts.views.commnentsview import(
    CommentListApiView,
    # CommentDetailsApiView,
)
from contracts.views.attachmentviews import(
    ContractBorderAttachmentDomainListApiView,
    ContractBorderAttachmentDomainDetailsApiView,

    ContractAttachmentDomainListApiView,
    ContractAttachmentDomainDetailsApiView,

    ContractBorderAttachmentListApiView,
    ContractBorderAttachmentDetailsApiView,

    ContractAttachmentListApiView,
    ContractAttachmentDetailsApiView,

    SharhbaseAttachmentDomainListApiView,
    SharhbaseAttachmentDomainDetailsApiView,
    
    SharhbaseAttachmentListApiView,
    SharhbaseAttachmentDetailsApiView,
)

urlpatterns = [
    path('' , ContractListApiViews.as_view() , name="contract-list"),
    path('<uuid:contractid>/' , ContractDetailsApiViews.as_view() , name="contract-details"),

    path('<uuid:contractid>/elhaghye/' , ContractElhaghyeListApiViews.as_view() , name="contractelhaghye-list"),
    path('<uuid:contractid>/elhaghye/<int:id>/' , ContractElhaghyeDetailsApiViews.as_view() , name="contractelhaghye-details"),
    
    path('domains/' , ContractDomainsListApiView.as_view() , name='contractdomains-list'),

    path('contractborder/' , ContractBorderListApiView.as_view() , name='contractborders-list'),
    path('contractborder/<uuid:pk>/' , ContractBorderDetailsApiView.as_view() , name='contractborders-detail'),
    path('contractborder/<uuid:pk>/downloadexportshape/' , ContractBorderDownloadExportShapeApiViews.as_view() , name="contractborder-downloadexportshape"),
    path('contractborder/alldownloadexportshape/' , AllContractBorderDownloadExportShapeApiViews.as_view() , name="contractborder-downloadexportshape-all"),

    #Attachment
    path('contractborderattachmentdomain/' , ContractBorderAttachmentDomainListApiView.as_view() , name='contractborderattachmentdomain-list'),
    path('contractborderattachmentdomain/<int:pk>/' , ContractBorderAttachmentDomainDetailsApiView.as_view() , name='contractborderattachmentdomain-details'),

    path('contractattachmentdomain/' , ContractAttachmentDomainListApiView.as_view() , name='contractattachmentdomain-list'),
    path('contractattachmentdomain/<int:pk>/' , ContractAttachmentDomainDetailsApiView.as_view() , name='contractattachmentdomain-details'),

    path('sharhbaseattachmentdomain/' , SharhbaseAttachmentDomainListApiView.as_view() , name='sharhbaseattachmentdomain-list'),
    path('sharhbaseattachmentdomain/<int:pk>/' , SharhbaseAttachmentDomainDetailsApiView.as_view() , name='sharhbaseattachmentdomain-details'),

    path('contractborderattachment/<uuid:contractborderid>/' , ContractBorderAttachmentListApiView.as_view() , name='contractborderattachment-list'),
    path('contractborderattachment/<int:contractborderattachmentid>/' , ContractBorderAttachmentDetailsApiView.as_view() , name='contractborderattachment-details'),

    path('contractattachment/<uuid:contractid>/' , ContractAttachmentListApiView.as_view() , name='contractattachment-list'),
    path('contractattachment/<int:contractattachmentid>/' , ContractAttachmentDetailsApiView.as_view() , name='contractattachment-details'),

    path('sharhbaseattachment/<int:sharhbaseid>/' , SharhbaseAttachmentListApiView.as_view() , name='sharhbaseattachment-list'),
    path('sharhbaseattachment/<int:sharhbaseid>/<int:sharhbaseattachmentid>/' , SharhbaseAttachmentDetailsApiView.as_view() , name='sharhbaseattachment-details'),

    #Sharhkhadamat
    path('sharhkhadamat/<uuid:contractid>/' , SharhkhadamatListApiView.as_view() , name='contract-shrbase-list'),
    path('sharhkhadamat/<uuid:contractid>/<int:shrhbaseid>/' , SharhkhadamatDetailApiView.as_view() , name='contract-shrbase-detail'),

    #Shrhkhadamat Layer
    path('sharhkhadamatlayer/<uuid:contractid>/' , SharhKhadamatLayerListApiView.as_view() , name='contract-shrlyr-list'),
    path('sharhkhadamatlayer/<uuid:contractid>/<int:shrhid>/' , SharhKhadamatLayerDetailApiView.as_view() , name='contract-shrlyr-detail'),

    path('comments/<int:shrhlayerid>/' , CommentListApiView.as_view() , name='comments-list'),
    # path('comments/<int:shrhlayerid>/<int:commentid>/' , CommentDetailsApiView.as_view() , name='comments-details'),
]
