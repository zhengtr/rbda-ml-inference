from os import listdir
from os.path import isfile, join
import pandas as pd

if __name__ == "__main__":
    data_path = "./trino_res_clean/"
    file_list = [f for f in listdir(data_path) if isfile(join(data_path, f)) if not f.endswith(".py")]

    df_res = pd.read_csv(data_path + file_list[0]).set_index("year")
    for txt_file in file_list[1:]:
        df_new = pd.read_csv(data_path + txt_file).set_index("year")
        df_res = df_res.merge(df_new, how="left", left_index=True, right_index=True, sort=False, suffixes=("", ""), copy=None, indicator=False, validate=None)
    
    df_res.to_csv(data_path + "join_all_clean.csv", index=True, header=True)



