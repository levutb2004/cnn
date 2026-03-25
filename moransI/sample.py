import geopandas as gpd 
import os 

dict = {'Total_popu':'popMoransP'
        #, 'pop_dens_1': 'dens_p_val'
        #, 'pop_built_': 'builtDensP'
        }
country = 'VNM'
dissolved_gdf = gpd.read_file(r'E:\fake-pomelo\moransI\quanhuyen.shp')
gdf = gpd.read_file(r'E:\fake-pomelo\moransI\residualMoransI.shp')
path = r'E:\fake-pomelo\pomelo_input_data'
for key,value in dict.items():
    for i in range(1,19):
        gdf_copy = gdf.copy()
        size = len(dissolved_gdf[dissolved_gdf[value] < 0.1])
        print(size)
        gdf_copy['is_train'] = 0 
        significant_sample = int(size * i * 0.05)
        significants = dissolved_gdf[dissolved_gdf[value] < 0.1].sample(n = significant_sample)
        insignificants = dissolved_gdf[dissolved_gdf[value] > 0.1].sample(n = size - significant_sample)
        sig_ids = significants["GR_SID"]
        insig_ids = insignificants["GR_SID"]

        gdf_copy.loc[gdf_copy["GR_SID"].isin(sig_ids), "is_train"] = 1
        gdf_copy.loc[gdf_copy["GR_SID"].isin(insig_ids), "is_train"] = 1
        output_folder = os.path.join(path, f'{country}_Sample_{i}')
        os.makedirs(output_folder, exist_ok=True)
        output_file = os.path.join(output_folder, f'Sample_{i}.shp')
        gdf_copy.to_file(output_file, driver='ESRI Shapefile')