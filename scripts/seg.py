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

# Setup data folders
city_folder = os.path.join(data_folder, code_insee)
raster_folder = os.path.join(city_folder, 'raster')
segmentation_folder = os.path.join(city_folder, 'segmentation')

try:
    os.makedirs(segmentation_folder)  
except FileExistsError as e:
    pass

for filename in os.listdir(segmentation_folder):
    os.remove(os.path.join(segmentation_folder, filename))

# Processing
app = otb.Registry.CreateApplication("Segmentation")

for raster_file in os.listdir(raster_folder):

    input_filepath = os.path.join(raster_folder, raster_file)
    output_filepath = os.path.join(segmentation_folder, f'{os.path.splitext(raster_file)[0]}_seg.gpkg')

    params = {
        'in': input_filepath,
        'filter': 'meanshift',
        'filter.meanshift.spatialr': 20,
        'filter.meanshift.ranger': 10,
        'filter.meanshift.thres': 0.1,
        'filter.meanshift.maxiter': 200,
        'filter.meanshift.minsize': 100, 
        'mode': 'vector',
        'mode.vector.out': output_filepath,
        'mode.vector.outmode': 'ulovw',
        # 'mode.vector.inmask': 'NC'
        'mode.vector.neighbor': False,
        'mode.vector.stitch' : True,
        'mode.vector.minsize': 1,
        'mode.vector.simplify': 0.1,
        'mode.vector.layername': 'layer',
        'mode.vector.fieldname': 'DN',
        'mode.vector.tilesize': 0, # If null, optimal size selected according to available RAM
        'mode.vector.startlabel': 1,
    }

    app.SetParameters(params)
    app.ExecuteAndWriteOutput()

# Elapsed time
elapsed_time = time.time() - start_time
logging.info(f"Segmentation computation time: {elapsed_time: .2f}s")