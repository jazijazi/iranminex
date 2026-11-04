from django.urls import path, include

from layers.views.layerviews import (
    LayerNamesListApiView,

    AllLayersOfAContractListApiView,
    ShpColumnOfVectorLayerApiView,
    AllColumnOfSharhlayerApiView,
    UploadVectorLayerApiView,
    DeleteVectorLayerApiView,
    RasterLayerApiView,
    DeleteRasterLayerApiView,
    DownloadRasterLayerApiView,
    VerifyLayerApiView,
    LayerFeatureDetails,
    DownloadVectorLayer,
    DownloadContractBorderVectorLayers,
    SingleFeatureDetailsApiView,
)
from layers.views.featureattachviews import (
    FeatureAttachmentListApiView,
    FeatureAttachmentDetailsApiView,
)
from layers.views.searchviews import (
    SearchLayerByLocation,
)

urlpatterns = [
    path('layernames/<int:contractcode>/' , LayerNamesListApiView.as_view() , name="layernames-list"),

    path('layercontract/<uuid:contractid>/<uuid:contractborderid>/' , AllLayersOfAContractListApiView.as_view() , name="layercontract-list"),
    
    path('shpcolsvectorlayer/' , ShpColumnOfVectorLayerApiView.as_view() , name="vectorlayer-shpcolnames"),
    path('shrlyrcol/' , AllColumnOfSharhlayerApiView.as_view() , name="sharhlayer-shpcolnames"),
    path('uploadvectorlayer/' , UploadVectorLayerApiView.as_view() , name="vectorlayer-upload"),
    path('deletevectorlayer/' , DeleteVectorLayerApiView.as_view() , name="vectorlayer-delete"),
    path('rasterlayer/' , RasterLayerApiView.as_view() , name="rasterlayer"),
    path('deleterasterlayer/' , DeleteRasterLayerApiView.as_view() , name="rasterlayer-delete"),
    path('downloadrasterlayer/' , DownloadRasterLayerApiView.as_view() , name="rasterlayer-download"),
    path('layerfeaturedetails/<int:shrhlayerid>/' , LayerFeatureDetails.as_view() , name="layer-feature-details"),

    path('downloadvectorlayer/<int:shrhlayerid>/' , DownloadVectorLayer.as_view() , name="vectorlayer-download"),
    path('downloadvectorlayerfromcontractbrder/<uuid:contractborderid>/' , DownloadContractBorderVectorLayers.as_view() , name="vectorlayer-download-contractborder"),

    path('verifylayer/' , VerifyLayerApiView.as_view() , name="verify-layer"),

    path('featureattachment/<int:shrhlyr_id>/<int:feature_id>/' , FeatureAttachmentListApiView.as_view() , name="featureattach-list"),
    path('featureattachment/<int:shrhlyr_id>/<int:feature_id>/<int:attach_id>/' , FeatureAttachmentDetailsApiView.as_view() , name="featureattach-details"),

    path('singlefeaturedetails/<int:shrhlyr_id>/<int:feature_id>/' , SingleFeatureDetailsApiView.as_view() , name="singlefeature-details"),

    path('searchlayerbylocation/' , SearchLayerByLocation.as_view() , name="search-by-location"),
]
