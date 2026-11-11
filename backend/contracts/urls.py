from django.urls import path, include

from contracts.views.contractviews import (
    ContractListApiViews,
    ContractDetailsApiViews,

    ContractElhaghyeListApiViews,
    ContractElhaghyeDetailsApiViews,

    ContractDomainsListApiView,
)
# from contracts.views.sharhkhadamatviews import (
    # SharhkhadamatListApiView,
    # SharhkhadamatDetailApiView,

    # SharhKhadamatLayerListApiView,
    # SharhKhadamatLayerDetailApiView,
# )
from contracts.views.commnentsview import(
    CommentListApiView,
    # CommentDetailsApiView,
)
from contracts.views.attachmentviews import(

    ContractAttachmentDomainListApiView,
    ContractAttachmentDomainDetailsApiView,

    ContractAttachmentListApiView,
    ContractAttachmentDetailsApiView,

    # SharhbaseAttachmentDomainListApiView,
    # SharhbaseAttachmentDomainDetailsApiView,
    
    # SharhbaseAttachmentListApiView,
    # SharhbaseAttachmentDetailsApiView,
)

urlpatterns = [
    # Contracts
    path('', ContractListApiViews.as_view(), name='contract-list'),
    path('<uuid:contractid>/', ContractDetailsApiViews.as_view(), name='contract-details'),

    # Contract domains (global resources)
    path('domains/', ContractDomainsListApiView.as_view(), name='contractdomains-list'),

    # Contract attachment domains (global resources)
    path('attachment-domains/', ContractAttachmentDomainListApiView.as_view(), name='contractattachmentdomain-list'),
    path('attachment-domains/<int:pk>/', ContractAttachmentDomainDetailsApiView.as_view(), name='contractattachmentdomain-details'),

    # Sharhbase attachment domains (global resources)
    # path('sharhbase-attachment-domains/', SharhbaseAttachmentDomainListApiView.as_view(), name='sharhbaseattachmentdomain-list'),
    # path('sharhbase-attachment-domains/<int:pk>/', SharhbaseAttachmentDomainDetailsApiView.as_view(), name='sharhbaseattachmentdomain-details'),

    # Contract Elhaghye
    path('<uuid:contractid>/elhaghye/', ContractElhaghyeListApiViews.as_view(), name='contractelhaghye-list'),
    path('<uuid:contractid>/elhaghye/<int:id>/', ContractElhaghyeDetailsApiViews.as_view(), name='contractelhaghye-details'),

    # Contract attachments
    path('<uuid:contractid>/attachments/', ContractAttachmentListApiView.as_view(), name='contractattachment-list'),
    path('<uuid:contractid>/attachments/<int:contractattachmentid>/', ContractAttachmentDetailsApiView.as_view(), name='contractattachment-details'),

    # Sharhkhadamat
    # path('<uuid:contractid>/sharhkhadamat/', SharhkhadamatListApiView.as_view(), name='contract-shrbase-list'),
    # path('<uuid:contractid>/sharhkhadamat/<int:shrhbaseid>/', SharhkhadamatDetailApiView.as_view(), name='contract-shrbase-detail'),

    # Sharhkhadamat layers
    # path('<uuid:contractid>/sharhkhadamat-layers/', SharhKhadamatLayerListApiView.as_view(), name='contract-shrlyr-list'),
    # path('<uuid:contractid>/sharhkhadamat-layers/<int:shrhid>/', SharhKhadamatLayerDetailApiView.as_view(), name='contract-shrlyr-detail'),

    # Sharhbase attachments
    # path('<uuid:contractid>/sharhkhadamat/<int:shrhbaseid>/attachments/', SharhbaseAttachmentListApiView.as_view(), name='sharhbaseattachment-list'),
    # path('<uuid:contractid>/sharhkhadamat/<int:shrhbaseid>/attachments/<int:sharhbaseattachmentid>/', SharhbaseAttachmentDetailsApiView.as_view(), name='sharhbaseattachment-details'),

    # Comments
    path('<uuid:contractid>/sharhkhadamat-layers/<int:shrhlayerid>/comments/', CommentListApiView.as_view(), name='comments-list'),
]