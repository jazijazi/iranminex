from django.urls import path, include


from report.views.views import (
    ReportMain,
    ReportMainByOstan,
)
from report.views.layerreport import (
    ReportLayers,
    ReportLayersByProvince,
    ReportLayersByCounty,
)
from report.views.contracts import (
    ReportContracts,
    ReportContractsByCompany,
    ReportContractsBySharh,
    ReportContractsByInitialBorder,
    ReportContractsByDomin,
    ReportContractSummary,
)
from report.views.initialborder import (
    ReportInitialborderContracts,
    InitFileReport,
    InitSummaryFileReport,
)
from report.views.initialborder import (
    InitContractFileReport,
    InitDocFileReport,
)


urlpatterns = [
    path('' , ReportMain.as_view() , name="main"),
    path('byostan/<int:provinceid>/' , ReportMainByOstan.as_view() , name="main"),

    # layer report
    path('layers/byinitborder/<int:initialborderid>/' , ReportLayers.as_view() , name="layer-report-main"),
    path('layers/byprovince/<int:provinceid>/', ReportLayersByProvince.as_view(), name="layer-report-byproviance"),
    path('layers/bycounty/<int:countyid>/', ReportLayersByCounty.as_view(), name="layer-report-bycounty"),
    # path('layers//<int:initialborderid>/' , ReportContractsByInitialBorder.as_view() , name="contracts-byinitborder"),

    #initialborder report
    path('initreport/<int:initborderid>/' , InitFileReport.as_view() , name="initborder-wordfile-report"),
    path('initsummaryreport/<int:initborderid>/' , InitSummaryFileReport.as_view() , name="initborder-wordfile-summary-report"),
    path('initcontractreport/<int:initborderid>/<uuid:contractid>/' , InitContractFileReport.as_view() , name="initborder-contract-report"),
    path('initdocfilereport/<int:initborderid>/' , InitDocFileReport.as_view() , name="initborder-doc-report"),
    

    # contract report
    path('contracts/' , ReportContracts.as_view() , name="contracts-main"),
    path('contracts/bycompany/' , ReportContractsByCompany.as_view() , name="contracts-bycompany"),
    path('contracts/bysharh/' , ReportContractsBySharh.as_view() , name="contracts-bysharh"),
    path('contracts/byinitborder/<int:initialborderid>/' , ReportContractsByInitialBorder.as_view() , name="contracts-byinitborder"),
    path('contracts/bycontractdomain/<int:contractdoamincode>/' , ReportContractsByDomin.as_view() , name="contarcts-bycontractdomain"),
    path('contracts/contractsummaryreport/<uuid:contractid>/' , ReportContractSummary.as_view() , name='contract-excelfile-summary-report'),


    # initialborder report
    path('initialborders/' , ReportInitialborderContracts.as_view() , name="initialbordercontract")
]
