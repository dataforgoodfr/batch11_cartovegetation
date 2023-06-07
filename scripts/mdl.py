import os
import pickle
import geopandas as gpd

from sklearn.cluster import KMeans


data_folder = os.path.normpath('/app/data')

code_insee = os.getenv('CODE_INSEE')

try:
    os.makedirs(data_folder)
except FileExistsError:
    pass


input_filepath = os.path.join(data_folder, f'{code_insee}_zst.gpkg')


# with open('/app/models/model.pkl', 'rb') as mdl_pkl:
#     model = pickle.load(mdl_pkl)


# pipe = model.best_estimator_

gdf = gpd.read_file(input_filepath)


X = gdf.copy()
# rename_mapping = {
#     'segment_primitive_Harilick_H_mean': 'mean_hte_IC1',
#     'segment_primitive_BI2_B_mean': 'mean_rdi_BI2',
#     'segment_primitive_MSAVI2_M_mean': 'mean_rdi_MSAVI2',
#     'segment_primitive_NDWI2_N_mean': 'mean_rdi_NDWI2'
# }

# X_new = X_new.rename(columns=rename_mapping)
X = X.set_index('DN')

geometry_serie = X['geometry']

X = X.drop(columns='geometry')

# X = pipe.transform(X)

kmeans = KMeans(n_clusters=5, random_state=0).fit(X)

gdf['class'] = kmeans.labels_

# gdf['class'] = pipe.predict(X)

gdf.to_file(os.path.join(data_folder, f'{code_insee}_cls.gpkg'), driver="GPKG")