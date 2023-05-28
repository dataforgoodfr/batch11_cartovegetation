import os
from pathlib import Path
import requests
import json
from osgeo import gdal
import geopandas as gpd
import rasterio
from rasterio.mask import mask


code_insee = os.getenv('CODE_INSEE')

url_topo = 'https://wxs.ign.fr/topographie/geoportail/wfs?'

params_get_features = {
    'service': 'wfs',
    'version' : '2.0.0',
    'request' : 'GetFeature',
    'typeName' : 'BDTOPO_V3:commune',
    'filter' : f'<Filter><PropertyIsEqualTo><PropertyName>code_insee</PropertyName><Literal>{code_insee}</Literal></PropertyIsEqualTo></Filter>',
    'outputFormat' : 'json'
}

# Send the HTTP GET request to the WFS endpoint
response = requests.get(url_topo, params=params_get_features)

# Read the GeoJSON response using geopandas
commune = gpd.read_file(json.dumps(response.json()))
commune.crs = "EPSG:4326"

## DATA
data_folder = os.path.normpath('/app/data')

data_subfolders = [name for name in os.listdir(data_folder) if os.path.isdir(os.path.join(data_folder, name))]

#TODO Corse
if int(code_insee[:2]) >= 97:
    code_departement = code_insee[:3]
else:
    code_departement = f'0{code_insee[:2]}'

# TODO Manage case where there are multiple matches of the departement
departement_folder = None
for data_subfolder in data_subfolders:   
    if f'D{code_departement}' in data_subfolder:
        departement_folder = os.path.join(data_folder, data_subfolder)
        break

livraison_folder = None
tiles_folderpath = None
for root, dirs, files in os.walk(departement_folder):
    for dir in dirs:
        if '1_DONNEES_LIVRAISON' in dir:
            livraison_folder = os.path.join(root, dir)
            for name in os.listdir(livraison_folder):
                if os.path.isdir(os.path.join(livraison_folder, name)):
                    tiles_folderpath = Path(os.path.join(livraison_folder, name))

# TODO à automatiser
path = Path('/app/data/ORTHOHR_1-0_IRC-0M20_JP2-E080_LAMB93_D091_2021-01-01/ORTHOHR/1_DONNEES_LIVRAISON_2022-06-00154/OHR_IRC_0M20_JP2-E080_LAMB93_D91-2021')

vrt_filepath = os.path.join(data_folder, f'{code_insee}.vrt')

tiles_filepaths = [str(x) for x in tiles_folderpath.rglob('*.jp2')]  # list of paths to raster files
dataset = gdal.BuildVRT(vrt_filepath, tiles_filepaths)
dataset.FlushCache()

communeL93 = commune.to_crs(epsg=2154)
with rasterio.open(vrt_filepath) as raster_vrt:
    cropped, crop_trans = mask(raster_vrt, [communeL93.iloc[0].geometry], crop=True)

# Specify the path where you want to save the GeoTIFF file
output_path = os.path.join(data_folder, f'{code_insee}.tif')

# Open a new GeoTIFF file in write mode
with rasterio.open(output_path, 'w', driver='GTiff', height=cropped.shape[1], width=cropped.shape[2], count=cropped.shape[0], dtype=cropped.dtype, crs=raster_vrt.crs, transform=crop_trans) as dst:
    # Write the cropped data to the GeoTIFF file
    dst.write(cropped)

