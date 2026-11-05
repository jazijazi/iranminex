import zipfile
import tempfile
import os
import shutil
from typing import Tuple, Dict, Any, Optional , List  , TypedDict
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
import geopandas as gpd
import pandas as pd
from geopandas import GeoDataFrame
from django.contrib.gis.geos import MultiPolygon, Polygon
from shapely.geometry import MultiPolygon as ShapelyMultiPolygon, Polygon as ShapelyPolygon

from django.core.files.uploadedfile import InMemoryUploadedFile

from common.constants import SCALE_CHOICES
from common.services.gis import (
    validate_geodataframe,
    get_geometry_type,
    drop_zm
)