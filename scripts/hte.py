import os
import otbApplication as otb


## DATA
data_folder = os.path.normpath('/app/data')

code_insee = os.getenv('CODE_INSEE')

try:
    os.makedirs(data_folder)
except FileExistsError:
    pass

# TODO dynamic input file and verify input exist
input_filename = f'{code_insee}.tif'
input_filepath = os.path.join(data_folder, input_filename)

output_filename = f'{code_insee}_hte.tif'
output_filepath = os.path.join(data_folder, output_filename)


## PROCESSING
app = otb.Registry.CreateApplication("HaralickTextureExtraction")

# TODO config file
# Documentation : https://www.orfeo-toolbox.org/CookBook/Applications/app_HaralickTextureExtraction.html?highlight=haralick
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
    'texture': 'advanced',
    'out': output_filepath,
    'ram' : int(os.getenv('OTB_MAX_RAM_HINT'))
}

app.SetParameters(params)

app.ExecuteAndWriteOutput()