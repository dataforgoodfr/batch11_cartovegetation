import os
import otbApplication as otb

# TODO ENV
os.environ['OTB_MAX_RAM_HINT'] = '256'
os.environ['OTB_LOGGER_LEVEL'] = 'DEBUG'


## DATA
data_folder = os.path.normpath('/app/data')

try:
    os.makedirs(data_folder)
except FileExistsError:
    pass

# TODO dynamic input file and verify input exist
input_filename = 'artassenx.tif'
input_filepath = os.path.join(data_folder, input_filename)

output_filename = f'{os.path.splitext(input_filename)[0]}_seg.gpkg'
output_filepath = os.path.join(data_folder, output_filename)


## PROCESSING
app = otb.Registry.CreateApplication("Segmentation")

# TODO config file
# Documentation : https://www.orfeo-toolbox.org/CookBook/Applications/app_Segmentation.html?highlight=segmentation
params = {
    'in': input_filepath,
    'filter': 'meanshift',
    'filter.meanshift.spatialr': 5,
    'filter.meanshift.ranger': 15,
    'filter.meanshift.thres': 0.1,
    'filter.meanshift.maxiter': 100,
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