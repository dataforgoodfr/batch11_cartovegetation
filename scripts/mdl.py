import os
import re
import sys
import time
import toml
import pickle
import numpy as np
import geopandas as gpd
import logging
import shutil


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
zst_folder = os.path.join(city_folder, 'zonal_stats', 'final')
classification_folder = os.path.join(city_folder, 'classification')

try:
    if os.path.exists(classification_folder) and os.path.isdir(classification_folder):
        shutil.rmtree(classification_folder)
except Exception as e:
    logging.error(e)

try:
    os.makedirs(classification_folder)
except FileExistsError:
    pass


with open('/app/models/model.pkl', 'rb') as mdl_pkl:
    model = pickle.load(mdl_pkl)
    
# Processing
for filename in os.listdir(zst_folder):

    pattern = r'\d{5}_(\d)_(.*)'
    tile_id = re.search(pattern, filename).group(1)

    input_filepath = os.path.join(zst_folder, filename)

    gdf = gpd.read_file(input_filepath)

    X = gdf.copy()
    X = X.set_index('DN')

    geometry_serie = X['geometry']
    X = X.drop(columns='geometry')

    column_selection = ['rdi_MSAVI2_mean', 'rdi_NDWI2_mean', 'rdi_BI2_mean', 'hte_ic1_mean']
    X_reorder = X[column_selection]

    X_arr = np.asarray(X_reorder)

    gdf['class'] = model.predict(X_arr)

    gdf.to_file(os.path.join(classification_folder, f'{code_insee}_{tile_id}_cls.gpkg'), driver="GPKG")


# Elapsed time
elapsed_time = time.time() - start_time
logging.info(f'Model prediction time: {elapsed_time: .2f}s')