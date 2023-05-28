import os
from osgeo import gdal


## DATA
data_folder = os.path.normpath('/app/data')

try:
    os.makedirs(data_folder)
except FileExistsError:
    pass

code_insee = os.environ.get('CODE_INSEE')

# TODO dynamic input file and verify input exist
input_filename = f"{code_insee}.tif"
input_filepath = os.path.join(data_folder, input_filename)

hte_filename = f'{os.path.splitext(input_filename)[0]}_hte.tif'
hte_filepath = os.path.join(data_folder, hte_filename)

output_filename = f'{os.path.splitext(hte_filename)[0]}_IC1.tif'
output_filepath = os.path.join(data_folder, output_filename)


# PROCESSING
gdal.UseExceptions()

dataset = gdal.Open(hte_filepath, gdal.GA_ReadOnly)

band_number = 9
band = dataset.GetRasterBand(band_number)

band_data = band.ReadAsArray()

driver = gdal.GetDriverByName("GTiff")
output_dataset = driver.Create(output_filepath, band.XSize, band.YSize, 1, band.DataType)

output_band = output_dataset.GetRasterBand(1)
output_band.WriteArray(band_data)

output_dataset.SetGeoTransform(dataset.GetGeoTransform())
output_dataset.SetProjection(dataset.GetProjection())

# Free
band = None
dataset = None
output_dataset = None