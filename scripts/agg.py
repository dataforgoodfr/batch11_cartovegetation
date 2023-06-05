import os
import re

import logging

import geopandas as gpd
import pandas as pd


### DATA ###

data_folder = os.path.normpath('/app/data')

code_insee = os.getenv('CODE_INSEE')

try:
    os.makedirs(data_folder)
except FileExistsError:
    pass

# TODO dynamic input file and verify input exist
input_filepath = os.path.join(data_folder, f'{code_insee}.tif')
output_filepath = os.path.join(data_folder, f'{code_insee}_zst.gpkg')

processing_ids = ['hte_IC1', 'rdi_BI2', 'rdi_MSAVI2', 'rdi_NDWI2']
vector_filepaths = [os.path.join(data_folder, f'{code_insee}_{processing_id}_zst.gpkg') for processing_id in processing_ids]


# ### JOIN ###

output = gpd.read_file(vector_filepaths[0])
output = output
for idx, vector_filepath in enumerate(vector_filepaths[1:]):
    result = re.search(r'\d{5}_(.*)_zst\.gpkg', vector_filepath)
    mean_column_name = f'mean_{result.group(1)}'
    mean_serie = gpd.read_file(vector_filepath).set_index('DN')[mean_column_name]
    output = output.join(mean_serie, on='DN')

gdf = gpd.GeoDataFrame(output, geometry="geometry")
gdf.to_file(output_filepath, driver="GPKG")
