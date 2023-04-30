import argparse
from csv_dataset import CSVDataset, my_collate
from detoxify import Detoxify
from logger import create_logger
import torch
import pandas as pd
import os
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Inference')
parser.add_argument("--data_type", required=True, choices=['questions', 'answers', 'reddit'], type=str, help="Data Type")
parser.add_argument("--data_path", default="./full_data",type=str, help="Path to data file")
parser.add_argument("--chunk_size", default=100, type=int, help="Inference batch size")


def main():
    args = parser.parse_args()
    logger = create_logger("inference.log")
    if torch.cuda.is_available():
        device = torch.device('cuda') 
    else:
        device = torch.device('cpu')
    logger.info(f'Using device: {str(device).upper()}.')

    input_file = args.data_path + f"/{args.data_type}_part-r-00000.csv"
    output_file = args.data_path + f"/{args.data_type}_score.csv"

    # dataset
    if args.data_type == "questions":
        header = ["Source", "YearOfCreation", "Id", "Score", "CW_count", "Body"]
    elif args.data_type == "answers":
        header = ["Source", "YearOfCreation", "ParentId", "Score", "CW_count","Body"]
    elif args.data_type == "reddit":
        header = ["Source","Body"]

    my_dataset = CSVDataset(path=input_file, header=header, chunk_size=args.chunk_size)
    data_loader = torch.utils.data.DataLoader(my_dataset, collate_fn=my_collate, batch_size=1, shuffle=False)
    
    model = Detoxify('original', device=device)
    use_header = True
    for key, body in tqdm(data_loader, desc="Scoring"):
        res = model.predict(body)
        pd.DataFrame(res, index=key).round(5).rename_axis('Source').reset_index().to_csv(output_file, mode="a", index=False, header=use_header)
        use_header = False

if __name__ == "__main__":
    main()