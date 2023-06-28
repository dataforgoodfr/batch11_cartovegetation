import os
import sys
import time
import toml
import json
import logging

import requests

from pathlib import Path

import geopandas as gpd

from osgeo import gdal

import rasterio
from rasterio.mask import mask


start_time = time.time()

data_folder = os.path.normpath('/app/data')

# Logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

root_logger.addHandler(console_handler)

# Config
config = toml.load('/app/config/config.toml')
code_insee = config['city']['CODE_INSEE']

# Get city boundaries using IGN TOPO BD
url_topo = 'https://wxs.ign.fr/topographie/geoportail/wfs?'

params_get_features = {
    'service': 'wfs',
    'version' : '2.0.0',
    'request' : 'GetFeature',
    'typeName' : 'BDTOPO_V3:commune',
    'filter' : f'<Filter><PropertyIsEqualTo><PropertyName>code_insee</PropertyName><Literal>{code_insee}</Literal></PropertyIsEqualTo></Filter>',
    'outputFormat' : 'json'
}

response = requests.get(url_topo, params=params_get_features)
commune = gpd.read_file(json.dumps(response.json()))
commune.crs = "EPSG:4326"

# Setup data folders
city_folder = os.path.join(data_folder, code_insee)

try:
    os.makedirs(city_folder)  
except FileExistsError as e:
    pass


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

vrt_filepath = os.path.join(city_folder, f'{code_departement}.vrt')

tiles_filepaths = [str(x) for x in tiles_folderpath.rglob('*.jp2')]  # list of paths to raster files

dataset = gdal.BuildVRT(vrt_filepath, tiles_filepaths)

dataset.FlushCache()

communeL93 = commune.to_crs(epsg=2154)
with rasterio.open(vrt_filepath) as raster_vrt:
    cropped, crop_trans = mask(raster_vrt, [communeL93.iloc[0].geometry], crop=True)

# Specify the path where you want to save the GeoTIFF file
output_path = os.path.join(city_folder, f'{code_insee}.tif')

# Open a new GeoTIFF file in write mode
with rasterio.open(output_path, 'w', driver='GTiff', height=cropped.shape[1], width=cropped.shape[2], count=cropped.shape[0], dtype=cropped.dtype, crs=raster_vrt.crs, transform=crop_trans) as dst:
    # Write the cropped data to the GeoTIFF file
    dst.write(cropped)

os.remove(vrt_filepath)

# Elapsed time
elapsed_time = time.time() - start_time
logging.info(f"Joining execution time: {elapsed_time: .2f}s")