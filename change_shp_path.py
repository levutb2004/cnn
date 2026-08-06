import pickle
shp_url = 'E:/fake-pomelo/pomelo_input_data/VNM_Sample_4/Sample_4.shp'

with open(r"E:\fake-pomelo\datasets\vnm\additional_train_vars_c.pkl", "rb") as f:
    data = pickle.load(f)
data[9] = shp_url
with open(r"E:\fake-pomelo\datasets\vnm\additional_train_vars_c.pkl", "wb") as f:
    pickle.dump(data, f)

with open(r"E:\fake-pomelo\datasets\vnm\additional_train_vars_f.pkl", "rb") as f:
    data = pickle.load(f)
data[9] = shp_url
with open(r"E:\fake-pomelo\datasets\vnm\additional_train_vars_f.pkl", "wb") as f:
    pickle.dump(data, f)

print(data[9])
