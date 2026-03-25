import geopandas as gpd
import numpy as np
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt
import pandas as pd
import libpysal
from esda.moran import Moran
import os

gdf = gpd.read_file(r'F:\pomelo\Shape file-20251216T041154Z-3-001\moransI\residualMoransI.shp')
dict = {'Total_popu':'pop_p', 'pop_dens_1': 'dens_p_val', 'pop_built_': 'builtDensP'}
# Get data

output_folder = r'F:\pomelo\morans_output2'
os.makedirs(output_folder, exist_ok=True)
gdf = gdf[gdf['Total_popu']>0]
for key,value in dict.items():
    results = []
    fig, axes = plt.subplots(3,7, figsize=(28, 10))
    axes = axes.flatten()

    
    data = gdf[key]

    w = libpysal.weights.KNN.from_dataframe(gdf, k=3)
    moran = Moran(data, w).I
    results.append({"dataset": 'base',"morans_I": moran})
    # Compute log
    data = data[data > 0]
    log_data = np.log(data)

    kde = gaussian_kde(log_data)
    x = np.linspace(log_data.min(), log_data.max(), 500)
    y = kde(x)

    axes[0].plot(x, y)
    axes[0].set_title("Base")
    
    size = len(gdf[gdf[value] < 0.1])
    gdf_concat = gdf.sample(n=size, random_state=42)

    data = gdf_concat[key]
    
    w = libpysal.weights.KNN.from_dataframe(gdf_concat, k=3)
    moran = Moran(data, w).I
    results.append({"dataset": 'SRS',"morans_I": moran})
    # Compute log
    data = data[data > 0]
    log_data = np.log(data)

    kde = gaussian_kde(log_data)
    x = np.linspace(log_data.min(), log_data.max(), 500)
    y = kde(x)

    axes[1].plot(x, y)
    axes[1].set_title('SRS')
    significants = []
    insignificants = []
    for i in range(1,19):
        significant_sample = int(size * i * 0.05)
        significants = gdf[gdf[value] < 0.1].sample(n = significant_sample)
        insignificants = gdf[gdf[value] > 0.1].sample(n = size - significant_sample)
        gdf_concat = gpd.GeoDataFrame(
        pd.concat([significants, insignificants], ignore_index=True),
        crs=insignificants.crs)

        data = gdf_concat[key]
        
        w = libpysal.weights.KNN.from_dataframe(gdf_concat, k=3)
        moran = Moran(data, w).I
        results.append({"dataset": f'Sample {i}',"morans_I": moran})
        data = data[data > 0]
        log_data = np.log(data)

        kde = gaussian_kde(log_data)
        x = np.linspace(log_data.min(), log_data.max(), 500)
        y = kde(x)

        axes[i+1].plot(x, y)
        axes[i+1].set_title(f'Sample {i}')
    fig_path = os.path.join(output_folder, f"{key}_kde.png")
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    plt.close(fig)

    df_results = pd.DataFrame(results)
    csv_path = os.path.join(output_folder, key +'_samples.csv')
    df_results.to_csv(csv_path, index=False)
        