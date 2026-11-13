from django.urls import path, include

from contracts.views.contractviews import (
    ContractListApiViews,
    ContractDetailsApiViews,

    ContractElhaghyeListApiViews,
    ContractElhaghyeDetailsApiViews,
)
from contracts.views.attachmentviews import(
    ContractAttachmentListApiView,
    ContractAttachmentDetailsApiView,
)
from contracts.views.donmains import (
    VahedListApiViews,
    VahedDetailsApiViews,

    FazListApiViews,
    FazDetailsApiViews,
    
    ContractDominListApiViews,
    ContractDominDetailsApiViews,
    
    NaghshSherkatListApiViews,
    NaghshSherkatDetailsApiViews,
    
    ContractAttachmentDomainListApiViews,
    ContractAttachmentDomainDetailsApiViews,
    
    ShrhAttachmentDomainListApiViews,
    ShrhAttachmentDomainDetailsApiViews,
)
from contracts.views.sharhkhadamatviews import(
    ShrhCatalogListApiViews,
    ShrhCatalogDetailsApiViews,
)

urlpatterns = [
    # Contracts
    path('', ContractListApiViews.as_view(), name='contract-list'),
    path('<uuid:contractid>/', ContractDetailsApiViews.as_view(), name='contract-details'),


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
    path('sharhcatalog/' , ShrhCatalogListApiViews.as_view() , name="shathcatalog-list"),
    path('sharhcatalog/<int:pk>/' , ShrhCatalogDetailsApiViews.as_view() , name="shathcatalog-details"),

    # Sharhkhadamat layers
    # path('<uuid:contractid>/sharhkhadamat-layers/', SharhKhadamatLayerListApiView.as_view(), name='contract-shrlyr-list'),
    # path('<uuid:contractid>/sharhkhadamat-layers/<int:shrhid>/', SharhKhadamatLayerDetailApiView.as_view(), name='contract-shrlyr-detail'),

    # Sharhbase attachments
    # path('<uuid:contractid>/sharhkhadamat/<int:shrhbaseid>/attachments/', SharhbaseAttachmentListApiView.as_view(), name='sharhbaseattachment-list'),
    # path('<uuid:contractid>/sharhkhadamat/<int:shrhbaseid>/attachments/<int:sharhbaseattachmentid>/', SharhbaseAttachmentDetailsApiView.as_view(), name='sharhbaseattachment-details'),



    #Dominas
    path('vahed/' , VahedListApiViews.as_view(), name="vahed-list"),
    path('vahed/<int:pk>/' , VahedDetailsApiViews.as_view(), name="vahed-details"),
    path('faz/' , FazListApiViews.as_view(), name="faz-list"),
    path('faz/<int:pk>/' , FazDetailsApiViews.as_view(), name="faz-details"),
    path('domain/' , ContractDominListApiViews.as_view(), name="domain-list"),
    path('domain/<int:pk>/' , ContractDominDetailsApiViews.as_view(), name="domain-details"),
    path('naghsh/' , NaghshSherkatListApiViews.as_view(), name="naghsh-list"),
    path('naghsh/<int:pk>/' , NaghshSherkatDetailsApiViews.as_view(), name="naghsh-details"),
    path('contractattachmentdomain/' , ContractAttachmentDomainListApiViews.as_view(), name="contract-atach-domin-list"),
    path('contractattachmentdomain/<int:pk>/' , ContractAttachmentDomainDetailsApiViews.as_view(), name="contract-atach-domin-details"),
    path('sharhattachmentdomain/' , ShrhAttachmentDomainListApiViews.as_view(), name="sharh-atach-domin-list"),
    path('sharhattachmentdomain/<int:pk>/' , ShrhAttachmentDomainDetailsApiViews.as_view(), name="sharh-atach-domin-details"),

]