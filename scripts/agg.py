import os
import re
import sys
import time
import toml
import logging

import pandas as pd
import geopandas as gpd


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

# Setup data folders
city_folder = os.path.join(data_folder, code_insee)
segmentation_folder = os.path.join(city_folder, 'segmentation')
zst_folder = os.path.join(city_folder, 'zonal_stats')
zst_final_folder = os.path.join(zst_folder, 'final')

try:
    os.makedirs(zst_final_folder)  
except FileExistsError as e:
    pass

for segmentation_file in os.listdir(segmentation_folder):
    pattern = r'\d{5}_(\d)_(.*)'
    seg_tile_id = re.search(pattern, segmentation_file).group(1)
    # Read vector file reference
    output_df = gpd.read_file(os.path.join(segmentation_folder, segmentation_file))

    # Join features to vector file using common 'DN' segment identifier
    feature_filenames = []
    for item in os.listdir(zst_folder):
        if os.path.isfile(os.path.join(zst_folder, item)):
            item_tile_id = re.search(pattern, item).group(1)
            if seg_tile_id == item_tile_id:
                feature_filenames.append(item)

    
    for zst_filename in feature_filenames:
        zst_filepath = os.path.join(zst_folder, zst_filename)
        zst_df = pd.read_csv(zst_filepath).set_index('DN')
        output_df = output_df.join(zst_df, on='DN')
        logging.info(f"Joined: {zst_filename}")

    # Convert dataframe to geodataframe
    output_gdf = gpd.GeoDataFrame(output_df, geometry="geometry")

    # Save in file
    output_filepath = os.path.join(zst_final_folder, f'{code_insee}_{seg_tile_id}_zst.gpkg')
    output_gdf.to_file(output_filepath, driver="GPKG")

# Elapsed time
elapsed_time = time.time() - start_time
logging.info(f"Zonal statistics joining time: {elapsed_time: .2f}s")
