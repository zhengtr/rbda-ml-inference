from os import listdir
from os.path import isfile, join

if __name__ == "__main__":
    my_path = "./trino_res/"
    out_path = "./trino_res_clean/"
    file_list = [f for f in listdir(my_path) if isfile(join(my_path, f))]

    for txt_file in file_list:
        with open(my_path + txt_file, 'r') as f_in, open(out_path + 'cln_' + txt_file, 'w') as f_out:
            for line in f_in:
                if line.startswith(('#', '-', '\n')):
                    continue
                cols = line.strip().split(' | ')
                for i in range(len(cols)):
                    cols[i] = cols[i].strip()
                f_out.write(",".join(cols) + '\n')
