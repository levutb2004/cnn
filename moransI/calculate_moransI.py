import geopandas as gpd
import pandas as pd
from libpysal.weights import KNN
from esda.moran import Moran
import os

results = []

base_path = r'E:/fake-pomelo/pomelo_input_data'

for i in range(1, 19):
    try:
        shp_path = os.path.join(
            base_path,
            f'VNM_Sample_{i}',
            f'Sample_{i}.shp'
        )
        
        # Load
        gdf = gpd.read_file(shp_path)

        # Dissolve
        dissolved = gdf.dissolve(
            by="GR_SID",
            aggfunc={
                "Total_popu": "sum",
                "is_train": "max"
            }
        ).reset_index()

        # Filter train
        train_gdf = dissolved[dissolved['is_train'] == 1]

        # Spatial weights
        w = KNN.from_dataframe(train_gdf, k=3)

        # Target
        y = train_gdf['Total_popu'].values

        # Moran's I
        mi = Moran(y, w)

        results.append({
            "sample": i,
            "moran_I": mi.I,
            "p_value": mi.p_sim
        })

        print(f"Sample {i}: Moran's I = {mi.I:.4f}")

    except Exception as e:
        print(f"Sample {i} error:", e)

# Save CSV
df_results = pd.DataFrame(results)
df_results.to_csv("E:/fake-pomelo/moransI/moransI_results.csv", index=False)

print("Saved to moransI_results.csv")