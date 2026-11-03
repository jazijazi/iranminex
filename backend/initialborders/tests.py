"""
Tests for proccess_initialborder_zipfile().

ADJUST BEFORE RUNNING:
    - `borders.utils` -> the actual module where proccess_initialborder_zipfile
      (and drop_zm / validate_geodataframe / get_geometry_type /
      convert_gdf_to_multipolygon) live. The @patch targets below patch these
      names *as imported into that module*, not where they're originally
      defined (the classic mock.patch gotcha) - split the patch targets up if
      your helpers actually live in a different module than the main function.

These tests assume geopandas / shapely (and a working GDAL/Fiona or pyogrio
backend) are already installed, since the function under test already
imports `gpd` directly.
"""
import io
import os
import shutil
import tempfile
import zipfile
from unittest.mock import patch, MagicMock

import geopandas as gpd
from shapely.geometry import Polygon
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import SimpleTestCase

from initialborders.services.gis import proccess_initialborder_zipfile  # adjust


def _build_shapefile_zip(work_dir, crs='EPSG:4326', include_shx=True, include_dbf=True):
    """Builds a tiny *real* shapefile with geopandas and zips its components."""
    shp_dir = os.path.join(work_dir, 'shp_src')
    os.makedirs(shp_dir, exist_ok=True)

    polygon = Polygon([(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)])
    gdf = gpd.GeoDataFrame({'id': [1]}, geometry=[polygon], crs=crs)
    gdf.to_file(os.path.join(shp_dir, 'test_border.shp'), driver='ESRI Shapefile')

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w') as zf:
        for fname in os.listdir(shp_dir):
            ext = os.path.splitext(fname)[1].lower()
            if ext == '.shx' and not include_shx:
                continue
            if ext == '.dbf' and not include_dbf:
                continue
            zf.write(os.path.join(shp_dir, fname), arcname=fname)
    buffer.seek(0)
    return buffer.read()


def _uploaded_zip(content: bytes, name='border.zip'):
    return InMemoryUploadedFile(
        file=io.BytesIO(content),
        field_name='file',
        name=name,
        content_type='application/zip',
        size=len(content),
        charset=None,
    )


class ProcessInitialborderZipfileTests(SimpleTestCase):
    """Pure function, no DB needed - runs fine under SimpleTestCase."""

    def setUp(self):
        self.work_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.work_dir, ignore_errors=True)

    # --- structural / file-format errors: no mocking needed ---

    def test_bad_zip_returns_persian_error(self):
        uploaded = _uploaded_zip(b'this is definitely not a zip file')
        success, result, message = proccess_initialborder_zipfile(uploaded)

        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertIn('نامعتبر', message)

    def test_missing_shp_returns_error(self):
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w') as zf:
            zf.writestr('readme.txt', b'no shapefile in here')
        uploaded = _uploaded_zip(buffer.getvalue())

        success, result, message = proccess_initialborder_zipfile(uploaded)

        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertIn('.shp', message)

    def test_missing_shx_component_returns_error(self):
        content = _build_shapefile_zip(self.work_dir, include_shx=False)
        uploaded = _uploaded_zip(content)

        success, result, message = proccess_initialborder_zipfile(uploaded)

        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertIn('.shx', message)

    def test_missing_dbf_component_returns_error(self):
        content = _build_shapefile_zip(self.work_dir, include_dbf=False)
        uploaded = _uploaded_zip(content)

        success, result, message = proccess_initialborder_zipfile(uploaded)

        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertIn('.dbf', message)

    def test_nested_shapefile_in_subfolder_is_currently_not_found(self):
        """
        Regression marker for the review note: os.listdir() only looks one
        level deep, so a shapefile inside a subfolder inside the zip is a
        legitimate case that currently gets misreported as 'no .shp found'.
        This documents current behavior; flip the assertion once os.walk()
        is used instead.
        """
        shp_dir = os.path.join(self.work_dir, 'nested', 'inner')
        os.makedirs(shp_dir, exist_ok=True)
        polygon = Polygon([(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)])
        gdf = gpd.GeoDataFrame({'id': [1]}, geometry=[polygon], crs='EPSG:4326')
        gdf.to_file(os.path.join(shp_dir, 'test_border.shp'), driver='ESRI Shapefile')

        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w') as zf:
            for root, _, files in os.walk(os.path.join(self.work_dir, 'nested')):
                for fname in files:
                    full_path = os.path.join(root, fname)
                    arcname = os.path.join('inner', fname)  # keep it nested inside the zip
                    zf.write(full_path, arcname=arcname)

        uploaded = _uploaded_zip(buffer.getvalue())
        success, result, message = proccess_initialborder_zipfile(uploaded)

        self.assertFalse(success)
        self.assertIn('.shp', message)

    # # --- happy path + CRS handling (mocks isolate your custom validation helpers) ---

    @patch('initialborders.services.gis.convert_gdf_to_multipolygon')
    @patch('common.services.gis_services.get_geometry_type', return_value='polygon')
    @patch('common.services.gis_services.validate_geodataframe', return_value=(True, ''))
    @patch('common.services.gis_services.drop_zm', side_effect=lambda geom: geom)
    def test_valid_wgs84_shapefile_succeeds(
        self, mock_drop_zm, mock_validate, mock_geom_type, mock_convert
    ):
        content = _build_shapefile_zip(self.work_dir, crs='EPSG:4326')
        uploaded = _uploaded_zip(content)

        expected = MagicMock(name='multipolygon')
        mock_convert.return_value = expected

        success, result, message = proccess_initialborder_zipfile(uploaded)

        self.assertTrue(success)
        self.assertIs(result, expected)
        self.assertEqual(message, '')
        mock_convert.assert_called_once()

    @patch('initialborders.services.gis.convert_gdf_to_multipolygon')
    @patch('common.services.gis_services.get_geometry_type', return_value='polygon')
    @patch('common.services.gis_services.validate_geodataframe', return_value=(True, ''))
    @patch('common.services.gis_services.drop_zm', side_effect=lambda geom: geom)
    def test_non_wgs84_crs_gets_reprojected(
        self, mock_drop_zm, mock_validate, mock_geom_type, mock_convert
    ):
        # UTM zone 39N (common for Iran-based data) should get reprojected to 4326
        content = _build_shapefile_zip(self.work_dir, crs='EPSG:32639')
        uploaded = _uploaded_zip(content)
        mock_convert.return_value = MagicMock()

        success, result, message = proccess_initialborder_zipfile(uploaded)

        self.assertTrue(success)
        called_gdf = mock_convert.call_args[0][0]
        self.assertEqual(called_gdf.crs.to_epsg(), 4326)

    def test_missing_crs_returns_error(self):
        # Build a shapefile then strip its .prj so gdf.crs comes back None
        content_with_crs = _build_shapefile_zip(self.work_dir, crs='EPSG:4326')

        buffer = io.BytesIO()
        with zipfile.ZipFile(io.BytesIO(content_with_crs)) as src_zf:
            with zipfile.ZipFile(buffer, 'w') as dst_zf:
                for item in src_zf.infolist():
                    if item.filename.lower().endswith('.prj'):
                        continue  # drop projection info entirely
                    dst_zf.writestr(item, src_zf.read(item.filename))

        uploaded = _uploaded_zip(buffer.getvalue())
        success, result, message = proccess_initialborder_zipfile(uploaded)

        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertIn('مختصات', message)

    # --- cleanup behavior ---

    def test_temp_directory_removed_after_success_and_failure(self):
        created_dirs = []
        real_mkdtemp = tempfile.mkdtemp

        def _spy_mkdtemp(*args, **kwargs):
            path = real_mkdtemp(*args, **kwargs)
            created_dirs.append(path)
            return path

        with patch('initialborders.services.gis.tempfile.mkdtemp', side_effect=_spy_mkdtemp):
            # failure case (bad zip)
            proccess_initialborder_zipfile(_uploaded_zip(b'not a zip'))

            # success-ish case
            with patch('common.services.gis_services.validate_geodataframe', return_value=(True, '')), \
                 patch('common.services.gis_services.get_geometry_type', return_value='polygon'), \
                 patch('initialborders.services.gis.convert_gdf_to_multipolygon', return_value=MagicMock()), \
                 patch('common.services.gis_services.drop_zm', side_effect=lambda geom: geom):

                
                
                content = _build_shapefile_zip(self.work_dir, crs='EPSG:4326')
                proccess_initialborder_zipfile(_uploaded_zip(content))

        self.assertTrue(created_dirs, 'expected mkdtemp to have been called at least once')
        for d in created_dirs:
            self.assertFalse(os.path.exists(d), f'{d} should have been cleaned up in the `finally` block')

    # # --- security regression guard ---

    def test_path_traversal_entry_does_not_escape_extraction_dir(self):
        """
        Guardrail, not a bug report: Python's zipfile already strips '..'
        path segments during extractall() in most cases, so this should
        currently PASS. If it ever starts failing (e.g. after a library or
        Python version change), that's a signal this needs explicit path
        validation before extraction - don't just delete the test.
        """
        marker_path = os.path.join(tempfile.gettempdir(), 'zzz_should_not_exist.txt')
        if os.path.exists(marker_path):
            os.remove(marker_path)

        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w') as zf:
            zf.writestr('../zzz_should_not_exist.txt', b'malicious payload')
        uploaded = _uploaded_zip(buffer.getvalue())

        try:
            proccess_initialborder_zipfile(uploaded)
            self.assertFalse(
                os.path.exists(marker_path),
                'a path-traversal zip entry escaped the temp extraction directory'
            )
        finally:
            if os.path.exists(marker_path):
                os.remove(marker_path)