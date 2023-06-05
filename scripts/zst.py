import os
import rasterstats
import geopandas as gpd
import rasterio
import rasterio.mask
import numpy as np



### DATA ###

data_folder = os.path.normpath('/app/data')

code_insee = os.getenv('CODE_INSEE')

try:
    os.makedirs(data_folder)
except FileExistsError:
    pass

# TODO dynamic input file and verify input exist

vector_filename = f'{code_insee}_seg.gpkg'
vector_filepath = os.path.join(data_folder, vector_filename)

# Load GeoPackage as GeoDataFrame
gdf = gpd.read_file(vector_filepath)

processing_ids = ['hte_IC1', 'rdi_BI2', 'rdi_MSAVI2', 'rdi_NDWI2']

for processing_id in processing_ids:
    print(f'Calculating zonal mean for {processing_id}')
    raster_filepath = os.path.join(data_folder, f'{code_insee}_{processing_id}.tif')
    output_filepath = os.path.join(data_folder, f'{code_insee}_{processing_id}_zst.gpkg')

    # Calculate zonal statistics
    stats = rasterstats.zonal_stats(gdf, raster_filepath, stats="mean", all_touched=True)

    # Create a new GeoDataFrame with the statistics
    stat_values = [feature['mean'] for feature in stats]
    gdf[f'mean_{processing_id}'] = stat_values

    # Save the GeoDataFrame to a new GeoPackage file
    gdf.to_file(output_filepath, driver='GPKG')