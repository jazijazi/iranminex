
from rest_framework import serializers
from initialborders.models.models import InitialBorder

from initialborders.models.metadata import (
    InitialBorderMetadataPahneh,
    InitialBorderMetadataDarkhastekteshaf,
    InitialBorderMetadataParvaneekteshaf,
    InitialBorderMetadataGovahikashf,
    InitialBorderMetadataParvanebahrebardai,
    InitialBorderMetadataPotansielyabi,
    InitialBorderMetadataCoal
)

def get_metadatamodel_from_initialborder(initialborder_id : int):
    result = None
    try:
        this_initialborder = InitialBorder.objects.get(pk=initialborder_id)
    except InitialBorder.DoesNotExist:
        return None
    
    code_initialborderdomain = this_initialborder.dtyp.code

    if code_initialborderdomain == 404: #pahne
        return InitialBorderMetadataPahneh
    if code_initialborderdomain == 22: #darkast ekteshaf
        return InitialBorderMetadataDarkhastekteshaf
    if code_initialborderdomain == 33: #parvaneh ekteshaf
        return InitialBorderMetadataParvaneekteshaf
    if code_initialborderdomain == 44: #govahi kashf
        return InitialBorderMetadataGovahikashf
    if code_initialborderdomain == 55: #parvane bahre bardari
        return InitialBorderMetadataParvanebahrebardai
    if code_initialborderdomain == 303: #potanselyabe
        return InitialBorderMetadataPotansielyabi
    if code_initialborderdomain == 737: #coal
        return InitialBorderMetadataCoal
    
def create_serializer_for_initialbordermetadata(model_class):
    """
        create serializer for tarh shenasame ha dynamically
        get a model calss and return serializer class for it
    """
    class Meta:
        model = model_class
        # fields = '__all__'
        exclude = ('id', ) # all fields except id

    serializer_name = f"{model_class.__name__}Serializer"
    return type(serializer_name, (serializers.ModelSerializer,), {'Meta': Meta})