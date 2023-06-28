import os
import sys
import time
import toml
import logging
import subprocess
import re


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
features_folder = os.path.join(city_folder, 'features')
zst_folder = os.path.join(city_folder, 'zonal_stats')

try:
    os.makedirs(zst_folder)  
except FileExistsError as e:
    pass

# Read vector file reference
vector_filepath = os.path.join(segmentation_folder, f'{code_insee}_seg.gpkg')

# Processing
for feature_filename in os.listdir(features_folder):
    result = re.search(r'\d{5}_(.*).tif', feature_filename)
    if result:
        feature = result.group(1)

    logging.info(f'Compute zonal mean for {feature}')
    raster_filepath = os.path.join(features_folder, f'{code_insee}_{feature}.tif')
    output_filepath = os.path.join(zst_folder, f'{code_insee}_{feature}_zst.csv')

    command = [
        "exactextract",
        "-r", f"{feature}:{raster_filepath}",
        "-p", vector_filepath,
        "-f", "DN",
        "-s", f"mean({feature})",
        "-o", output_filepath
        ]

    subprocess.run(command)

# Elapsed time
elapsed_time = time.time() - start_time
logging.info(f"Zonal statistics computation time: {elapsed_time: .2f}s")