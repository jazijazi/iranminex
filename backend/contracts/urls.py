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

    FazKaderContractListView,
    FazKaderContractDetailsView,

    ShrhContractListApiViews,
    ShrhContractDetailsApiViews,

    PackageShrhListApiViews,
    PackageShrhDetailsApiViews,
    
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
    path('sharhcatalog/<int:id>/' , ShrhCatalogDetailsApiViews.as_view() , name="shathcatalog-details"),

    path('<uuid:contractid>/faz-kaders/' , FazKaderContractListView.as_view() , name="faz-kader-list"),
    path('<uuid:contractid>/faz-kaders/<int:fazkaderid>/' , FazKaderContractDetailsView.as_view() , name="faz-kader-details"),

    path('<uuid:contractid>/sharh-items/' , ShrhContractListApiViews.as_view() , name="sharcontract-list"),
    path('<uuid:contractid>/sharh-items/<int:sharhcontractid>/' , ShrhContractDetailsApiViews.as_view() , name="sharcontract-details"),

    path('<uuid:contractid>/packagesharh/' , PackageShrhListApiViews.as_view(), name="packageshrh-list"),
    path('<uuid:contractid>/packagesharh/<int:id>/' , PackageShrhDetailsApiViews.as_view(), name="packageshrh-details"),

    # Sharhkhadamat layers
    # path('<uuid:contractid>/sharhkhadamat-layers/', SharhKhadamatLayerListApiView.as_view(), name='contract-shrlyr-list'),
    # path('<uuid:contractid>/sharhkhadamat-layers/<int:shrhid>/', SharhKhadamatLayerDetailApiView.as_view(), name='contract-shrlyr-detail'),

    # Sharhbase attachments
    # path('<uuid:contractid>/sharhkhadamat/<int:shrhbaseid>/attachments/', SharhbaseAttachmentListApiView.as_view(), name='sharhbaseattachment-list'),
    # path('<uuid:contractid>/sharhkhadamat/<int:shrhbaseid>/attachments/<int:sharhbaseattachmentid>/', SharhbaseAttachmentDetailsApiView.as_view(), name='sharhbaseattachment-details'),



    #Dominas
    path('vahed/' , VahedListApiViews.as_view(), name="vahed-list"),
    path('vahed/<int:id>/' , VahedDetailsApiViews.as_view(), name="vahed-details"),
    path('faz/' , FazListApiViews.as_view(), name="faz-list"),
    path('faz/<int:id>/' , FazDetailsApiViews.as_view(), name="faz-details"),
    path('domain/' , ContractDominListApiViews.as_view(), name="domain-list"),
    path('domain/<int:id>/' , ContractDominDetailsApiViews.as_view(), name="domain-details"),
    path('naghsh-sherkat/' , NaghshSherkatListApiViews.as_view(), name="naghsh-list"),
    path('naghsh-sherkat/<int:id>/' , NaghshSherkatDetailsApiViews.as_view(), name="naghsh-details"),
    path('contractattachmentdomain/' , ContractAttachmentDomainListApiViews.as_view(), name="contract-atach-domin-list"),
    path('contractattachmentdomain/<int:id>/' , ContractAttachmentDomainDetailsApiViews.as_view(), name="contract-atach-domin-details"),
    path('sharhattachmentdomain/' , ShrhAttachmentDomainListApiViews.as_view(), name="sharh-atach-domin-list"),
    path('sharhattachmentdomain/<int:id>/' , ShrhAttachmentDomainDetailsApiViews.as_view(), name="sharh-atach-domin-details"),

]