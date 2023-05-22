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

output_filename = f'{os.path.splitext(input_filename)[0]}_hte.tif'
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