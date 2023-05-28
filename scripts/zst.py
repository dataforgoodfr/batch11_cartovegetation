import os

### QGIS PRESCRIPT ###
from qgis.core import QgsApplication, QgsVectorLayer, QgsRasterLayer

QgsApplication.setPrefixPath("/QGIS", True)

qgs = QgsApplication([], False)
qgs.initQgis()

if qgs:
    print("QGIS installation is working.")
else:
    print("QGIS installation is not found.")

### DATA ###

data_folder = os.path.normpath('/app/data')

code_insee = os.getenv('CODE_INSEE')

try:
    os.makedirs(data_folder)
except FileExistsError:
    pass

# TODO dynamic input file and verify input exist
input_filename = f'{code_insee}.tif'
input_filepath = os.path.join(data_folder, input_filename)

output_filename = f'{code_insee}_zst.gpkg'
output_filepath = os.path.join(data_folder, output_filename)

### PROCESSING ### 
import processing
from processing.core.Processing import Processing
Processing().initialize()


processing_ids = ['hte_IC1', 'rdi_BI2', 'rdi_MSAVI2', 'rdi_NDWI2']

input_vector_data_filepath = os.path.join(data_folder, f'{code_insee}_seg.gpkg')
vector_layer = QgsVectorLayer(input_vector_data_filepath, 'vector_layer', 'ogr')

for processing_id in processing_ids:
    print(processing_id)

    input_raster_filepath = os.path.join(data_folder, f'{code_insee}_{processing_id}.tif')
    raster_layer = QgsRasterLayer(input_raster_filepath, 'raster_layer')

    output_filename = f'{code_insee}_{processing_id}_zst.gpkg'
    output_filepath = os.path.join(data_folder, output_filename)

    params = {
        'INPUT': vector_layer,
        'INPUT_RASTER': raster_layer,
        'RASTER_BAND': 1,  # Specify the raster band to use for zonal statistics
        'COLUMN_PREFIX': f'{processing_id}_',  # Prefix for the result columns
        'STATISTICS': [2],  # Example: calculate minimum, maximum, mean, sum, and count
        'OUTPUT': output_filepath
    }

    processing.run("native:zonalstatisticsfb", params)

### JOIN ###

# Documentation: https://docs.qgis.org/3.28/en/docs/user_manual/processing_algs/qgis/vectorgeneral.html#join-attributes-by-field-value
output_join_filename = f'{code_insee}_zst.gpkg'
output_join_filepath = os.path.join(data_folder, output_join_filename)

for idx, processing_id in enumerate(processing_ids[1:]):
    if idx == 0:
        layer1 = QgsVectorLayer(os.path.join(data_folder, f'{code_insee}_{processing_ids[0]}_zst.gpkg'), 'Layer1', 'ogr')
    else:
        layer1 = QgsVectorLayer(output_join_filepath, 'Layer1', 'ogr')

    layer2 = QgsVectorLayer(os.path.join(data_folder, f'{code_insee}_{processing_id}_zst.gpkg'), 'Layer2', 'ogr')  # Replace with the path to your second layer

    parameters = {
        'INPUT': layer1,
        'FIELD': 'DN',
        'INPUT_2': layer2,
        'FIELD_2': 'DN',
        'FIELDS_TO_COPY': ['mean'],
        'METHOD': 1,
        'DISCARD_NONMATCHING': True,
        'PREFIX': '',
        'OUTPUT': output_join_filepath
    }

    processing.run('native:joinattributestable', parameters)


### EXIT ###
qgs.exitQgis()