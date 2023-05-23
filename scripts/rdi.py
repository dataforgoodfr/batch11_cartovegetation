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

output_filename = f'{os.path.splitext(input_filename)[0]}_rdi.tif'
output_filepath = os.path.join(data_folder, output_filename)


## PROCESSING
app = otb.Registry.CreateApplication("RadiometricIndices")

# TODO config file
# Documentation : https://www.orfeo-toolbox.org/CookBook/Applications/app_RadiometricIndices.html?highlight=radiometric

'''
Vegetation:NDVI                     Normalized difference vegetation index (Red, NIR)
Vegetation:TNDVI                    Transformed normalized difference vegetation index (Red, NIR)
Vegetation:RVI                      Ratio vegetation index (Red, NIR)
Vegetation:SAVI                     Soil adjusted vegetation index (Red, NIR)
Vegetation:TSAVI                    Transformed soil adjusted vegetation index (Red, NIR)
Vegetation:MSAVI                    Modified soil adjusted vegetation index (Red, NIR)
Vegetation:MSAVI2                   Modified soil adjusted vegetation index 2 (Red, NIR)
Vegetation:GEMI                     Global environment monitoring index (Red, NIR)
Vegetation:IPVI                     Infrared percentage vegetation index (Red, NIR)
Vegetation:LAIFromNDVILog           Leaf Area Index from log NDVI (Red, NIR)
Vegetation::LAIFromReflLinear       Leaf Area Index from reflectances with linear combination (Red, NIR)
Vegetation::LAIFromNDVIFormo        Leaf Area Index from Formosat 2 TOC (Red, NIR)
Water:NDWI                          Normalized difference water index (Gao 1996) (NIR, MIR)
Water:NDWI2                         Normalized difference water index (Mc Feeters 1996) (Green, NIR)
Water:MNDWI                         Modified normalized difference water index (Xu 2006) (Green, MIR)
Water:NDTI                          Normalized difference turbidity index (Lacaux et al.) (Red, Green)
Soil:RI                             Redness index (Red, Green)
Soil:CI                             Color index (Red, Green)
Soil:BI                             Brightness index (Red, Green)
Soil:BI2                            Brightness index 2 (NIR, Red, Green)
BuiltUp:ISU                         Built Surfaces Index (NIR,Red)
'''

params = {
    'in': input_filepath,
    'out': output_filepath,
    'channels.blue': 4,
    'channels.green': 3,
    'channels.red': 2,
    'channels.nir': 1,
    'channels.mir': 4,
    'list': ['Vegetation:MSAVI2', 'Water:NDWI2', 'Soil:BI2'],
    'ram': int(os.getenv('OTB_MAX_RAM_HINT'))
}

app.SetParameters(params)

app.ExecuteAndWriteOutput()