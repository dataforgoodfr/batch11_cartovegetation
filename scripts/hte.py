import os
import sys
import time
import toml
import logging
import shutil

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
config_hte_simple = config['haralick']['simple']
config_hte_advanced = config['haralick']['advanced']
config_hte_higher = config['haralick']['higher']
config_otb = config['otb']

# Setup data folders
city_folder = os.path.join(data_folder, code_insee)
haralick_folder = os.path.join(city_folder, 'haralick')

try:
    if os.path.exists(haralick_folder) and os.path.isdir(haralick_folder):
        shutil.rmtree(haralick_folder)
except Exception as e:
    logging.error(e)

try:
    os.makedirs(haralick_folder)  
except FileExistsError as e:
    pass

# Processing
app = otb.Registry.CreateApplication("HaralickTextureExtraction")

input_filepath = os.path.join(city_folder, f'{code_insee}.tif')

def compute_hte(set: str):
    params = {
        'in': input_filepath,
        'channel': 1,
        'step': 1,
        'parameters.xrad': 3,
        'parameters.yrad' : 3,
        'parameters.xoff': 1,
        'parameters.yoff': 1,
        'parameters.min': 0,
        'parameters.max': 255,
        'parameters.nbbin': 8,
        'texture': set,
        'out': os.path.join(city_folder, 'haralick', f'{code_insee}_hte_{set}.tif'),
        'ram' : config_otb['OTB_MAX_RAM_HINT']
    }
    app.SetParameters(params)
    app.ExecuteAndWriteOutput()

if any(config_hte_simple.values()):
    compute_hte('simple')

if any(config_hte_advanced.values()):
    compute_hte('advanced')

if any(config_hte_higher.values()):
    compute_hte('higher')

# Elapsed time
elapsed_time = time.time() - start_time
logging.info(f"Haralick texture extraction time: {elapsed_time: .2f}s")