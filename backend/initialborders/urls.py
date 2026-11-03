from django.urls import path, include

from initialborders.views.initialborders import (
    InitialBorderListViews,
    InitialBorderDetailViews,
    InitialBorderDownloadExportShape,
    AllInitialBorderDownloadExportShape,
    #contracts
    InitialBorderContractsApiView,
    #domin
    InitialBorderDominListView,
    #metadata
    InitialBorderMetadatDetailsView,
    #attahcment
    InitialBorderAttachmentListView,
    InitialBorderAttachmentDetailView,
    #attachment domain
    InitialBorderAttachmentDomainListApiView,
    InitialBorderAttachmentDomainDetailsApiView,
)

#amar
from initialborders.views.amarviews import(
    AmarKarKhanehListApiView,
    AmarKarKhanehDetailsApiView,
    AmarEstekhrajListApiView,
    AmarEstekhrajDetailsApiView,
    HSEPASMANDListApiView,
    HSEPASMANDDetailsApiView,
    HSEHADESEListApiView,
    HSEHADESEDetailsApiView,
    AmarEkteshafListApiView,
    AmarEkteshafDetailsApiView,
    AmarAmalkardTajhizCoalListApiView,
    AmarAmalkardTajhizCoalDetailsApiView,
    AmarAmalkardBahrebardariCoalListApiView,
    AmarAmalkardBahrebardariCoalDetailsApiView
)
from initialborders.views.ipcamarviews import (
    IpcAmarEkteshafListApiView,
    IpcAmarEkteshafDetailsApiView,
    IpcBarnamehEkteshafListApiView,
    IpcBarnamehEkteshafDetailsApiView,

    IpcTafazolByYear,
)

urlpatterns = [
    path('' , InitialBorderListViews.as_view() , name="initialborder-list"), 
    path('<int:pk>/' , InitialBorderDetailViews.as_view() , name="initialborder-detail"),
    path('<int:pk>/downloadexportshape/' , InitialBorderDownloadExportShape.as_view() , name="initialborder-downloadexportshape"),
    path('downloadallexportshape/' , AllInitialBorderDownloadExportShape.as_view() , name="initialborder-downloadallexportshape"),
    path('domins/' , InitialBorderDominListView.as_view() , name="initialborderdomins-list"),
    path('metadata/<int:initialborderpk>/' , InitialBorderMetadatDetailsView.as_view() , name="initialborder-metadata-detail"),
    path('<int:initialborderpk>/attachments/' , InitialBorderAttachmentListView.as_view() , name="initialborder-atach-list"),
    path('attachment/<int:attachmentpk>/' , InitialBorderAttachmentDetailView.as_view() , name="initialborder-atach-detail"),
    path('attachdomains/' , InitialBorderAttachmentDomainListApiView.as_view() , name="initialborder-atach-domain-list"),
    path('attachdomains/<int:attachdomainpk>/' , InitialBorderAttachmentDomainDetailsApiView.as_view() , name="initialborder-atach-domain-detail"),
    path('<int:initialborderpk>/contracts/' , InitialBorderContractsApiView.as_view() , name="initialborder-all-contracts"),

    #amar
    path('<int:initialborderid>/amarkarkhaneh/' , AmarKarKhanehListApiView.as_view() , name="initialborder-amarkarkhaneh-list"),
    path('amarkarkhaneh/<int:amarkarkhanehid>/' , AmarKarKhanehDetailsApiView.as_view() , name="initialborder-amarkarkhaneh-details"),
    path('<int:initialborderid>/amarestekhraj/' , AmarEstekhrajListApiView.as_view() , name="initialborder-amarestekhraj-list"),
    path('amarestekhraj/<int:amarestekhrajid>/' , AmarEstekhrajDetailsApiView.as_view() , name="initialborder-amarestekhraj-details"),
    path('<int:initialborderid>/amarhsepasmand/' , HSEPASMANDListApiView.as_view() , name="initialborder-hsepasmand-list"),
    path('amarhsepasmand/<int:hsepasmandid>/' , HSEPASMANDDetailsApiView.as_view() , name="initialborder-hsepasmand-details"),
    path('<int:initialborderid>/amarhsehadese/' , HSEHADESEListApiView.as_view() , name="initialborder-hsehadese-list"),
    path('amarhsehadese/<int:hsehadeseid>/' , HSEHADESEDetailsApiView.as_view() , name="initialborder-hsehadese-details"),
    path('<int:initialborderid>/amarekteshaf/' , AmarEkteshafListApiView.as_view() , name="initialborder-amarekteshaf-list"),
    path('amarekteshaf/<int:amarekteshafid>/' , AmarEkteshafDetailsApiView.as_view() , name="initialborder-amarekteshaf-details"),
    path('<int:initialborderid>/amaramalkardtajhizcoal/' , AmarAmalkardTajhizCoalListApiView.as_view() , name="initialborder-amaramalkardtajhizcoal-list"),
    path('amaramalkardtajhizcoal/<int:amaramalkardtajhizcoalid>/' , AmarAmalkardTajhizCoalDetailsApiView.as_view() , name="initialborder-amaramalkardtajhizcoal-details"),
    path('<int:initialborderid>/amaramalkardbahrebardaricoal/' , AmarAmalkardBahrebardariCoalListApiView.as_view() , name="initialborder-amaramalkardbahrebardaricoal-list"),
    path('amaramalkardbahrebardaricoal/<int:amaramalkardbahrebardaricoalid>/' , AmarAmalkardBahrebardariCoalDetailsApiView.as_view() , name="initialborder-amaramalkardbahrebardaricoal-details"),

    path('<int:initialborderid>/ipcamarekteshaf/' , IpcAmarEkteshafListApiView.as_view() , name=''),
    path('ipcamarekteshaf/<int:ipcamarekteshafid>/' , IpcAmarEkteshafDetailsApiView.as_view() , name=''),
    path('ipcbarnamehekteshaf/' , IpcBarnamehEkteshafListApiView.as_view() , name=''),
    path('ipcbarnamehekteshaf/<int:ipcbarnamehekteshafid>/' , IpcBarnamehEkteshafDetailsApiView.as_view() , name=''),

    path('ipctafazolbyyear/<int:sal>/' , IpcTafazolByYear.as_view() , name=''),
]
