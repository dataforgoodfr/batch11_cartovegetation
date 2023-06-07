import os

import geopandas as gpd


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

def get_mean_serie(processing_id):
    vector_filepath = os.path.join(data_folder, f'{code_insee}_{processing_id}_zst.gpkg')
    feature_name = f'mean_{processing_id}'
    gdf = gpd.read_file(vector_filepath)
    gdf = gdf.set_index('DN')
    return gdf[feature_name]
    

output = gpd.read_file(vector_filepaths[0])
for idx, processing_id in enumerate(processing_ids[1:]):
    output = output.join(get_mean_serie(processing_id), on='DN')


gdf = gpd.GeoDataFrame(output, geometry="geometry")
gdf.to_file(output_filepath, driver="GPKG")
