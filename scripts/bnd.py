import os
import sys
import time
import toml
import logging

from osgeo import gdal


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

simple_channels = {
    'energy': 1,
    'entropy': 2,
    'correlation': 3,
    'inverse_difference_moment': 4,
    'inertia': 5,
    'cluster_shade': 6,
    'cluster_prominence': 7,
    'haralick_correlation': 8
    }

advanced_channels = {
    'mean': 1,
    'variance': 2,
    'dissimilarity': 3,
    'sum_average': 4,
    'sum_variance': 5,
    'sum_entropy': 6,
    'difference_of_entropies': 7,
    'difference_of_variances': 8,
    'ic1': 9,
    'ic2': 10
    }

higher_channels = {
    'short_run_emphasis': 1,
    'long_run_emphasis': 2,
    'grey_level_nonuniformity': 3,
    'run_length_nonuniformity': 4,
    'run_percentage': 5,
    'low_grey_level_run_emphasis': 6,
    'high_grey_level_run_emphasis': 7,
    'short_run_low_grey_level_emphasis': 8,
    'short_run_high_grey_level_emphasis': 9,
    'long_run_low_grey_level_emphasis': 10,
    'long_run_high_grey_level_emphasis': 11
    }

# Setup data folders
city_folder = os.path.join(data_folder, code_insee)
haralick_folder = os.path.join(city_folder, 'haralick')
features_folder = os.path.join(city_folder, 'features')

try:
    os.makedirs(features_folder)  
except FileExistsError as e:
    pass

for filename in os.listdir(features_folder):
    if 'hte' in filename:
        os.remove(os.path.join(features_folder, filename))

def process_hte_features(set: str):
    # Get features to compute
    if set == 'simple':
        features = {feature: simple_channels[feature] for feature, feature_bool in config_hte_simple.items() if feature_bool}
    elif set == 'advanced':
        features = {feature: advanced_channels[feature] for feature, feature_bool in config_hte_advanced.items() if feature_bool}
    elif set == 'higher':
        features = {feature: higher_channels[feature] for feature, feature_bool in config_hte_higher.items() if feature_bool}

    logging.info(f'Computed features: {features}')

    for feature, channel in features.items():
        hte_set_filepath = os.path.join(haralick_folder, f'{code_insee}_hte_{set}.tif')
        feature_filepath = os.path.join(features_folder, f'{code_insee}_hte_{feature}.tif')

        gdal.UseExceptions()

        dataset = gdal.Open(hte_set_filepath, gdal.GA_ReadOnly)

        band_number = channel
        band = dataset.GetRasterBand(band_number)

        band_data = band.ReadAsArray()

        driver = gdal.GetDriverByName("GTiff")
        output_dataset = driver.Create(feature_filepath, band.XSize, band.YSize, 1, band.DataType)

        output_band = output_dataset.GetRasterBand(1)
        output_band.WriteArray(band_data)

        output_dataset.SetGeoTransform(dataset.GetGeoTransform())

        logging.info(f'TEST2')
        output_dataset.SetProjection(dataset.GetProjection())

        logging.info(f'TEST1')

        band = None
        dataset = None
        output_dataset = None

# Compute
if any(config_hte_simple.values()):
    process_hte_features('simple')

if any(config_hte_advanced.values()):
    process_hte_features('advanced')

if any(config_hte_higher.values()):
    process_hte_features('higher')

# Elapsed time
elapsed_time = time.time() - start_time
logging.info(f"Channel selection time: {elapsed_time: .2f}s")