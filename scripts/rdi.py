import os
import sys
import time
import toml
import logging

import otbApplication as otb


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
config_otb = config['otb']

# Setup data folders
city_folder = os.path.join(data_folder, code_insee)
features_folder = os.path.join(city_folder, 'features')

try:
    os.makedirs(features_folder)  
except FileExistsError as e:
    pass

# Select features to compute
features = []
for section_key, section_value in config['radiometrics'].items():
    for feature, filter_bool in section_value.items():
        if filter_bool:
            features.append(feature)

# Processing
app = otb.Registry.CreateApplication("RadiometricIndices")
input_filepath = os.path.join(city_folder, f'{code_insee}.tif')

for feature in features:
    feature_acronym = feature.split(':')[1]
    output_filename = f'{code_insee}_rdi_{feature_acronym}.tif'
    output_filepath = os.path.join(features_folder, output_filename)

    params = {
        'in': input_filepath,
        'out': output_filepath,
        'channels.blue': 4,
        'channels.green': 3,
        'channels.red': 2,
        'channels.nir': 1,
        'channels.mir': 4,
        'list': [feature],
        'ram': config_otb['OTB_MAX_RAM_HINT']
    }

    app.SetParameters(params)
    app.ExecuteAndWriteOutput()

# Elapsed time
elapsed_time = time.time() - start_time
logging.info(f"Radiometric indices computation time: {elapsed_time: .2f}s")