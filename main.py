import argparse
from csv_dataset import CSVDataset, my_collate
from detoxify import Detoxify
from logger import create_logger
import torch
import pandas as pd
import os
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Inference')
parser.add_argument("--data_type", required=True, choices=['questions', 'answers', 'reddit', 'inst'], type=str, help="Data Type")
parser.add_argument("--data_path", default="./full_data",type=str, help="Path to data file")
parser.add_argument("--chunk_size", default=100, type=int, help="Inference batch size")
parser.add_argument("--partition", default=100000, type=int, help="Inference batch size")

def main():
    args = parser.parse_args()
    logger = create_logger("inference.log")
    if torch.cuda.is_available():
        device = torch.device('cuda') 
    else:
        device = torch.device('cpu')
    logger.info(f'Using device: {str(device).upper()}.')

    input_file = args.data_path + f"/{args.data_type}_part-r-00000.csv"
    # input_file = args.data_path + f"/mini_{args.data_type}.csv"
    output_file = args.data_path + f"/{args.data_type}_score"

    # dataset
    if args.data_type == "questions":
        header = ["Source", "YearOfCreation", "Id", "Score", "CW_count", "Body"]
    elif args.data_type == "answers":
        header = ["Source", "YearOfCreation", "ParentId", "Score", "CW_count","Body"]
    elif args.data_type == "reddit" or args.data_type == "inst":
        header = ["Source","Body"]

    my_dataset = CSVDataset(path=input_file, header=header, chunk_size=args.chunk_size)
    data_loader = torch.utils.data.DataLoader(my_dataset, collate_fn=lambda x: x[0], batch_size=1, shuffle=False)
    
    model = Detoxify('original', device=device)
    use_header, invalid_count, total_count = True, 0, 0
    pbar = tqdm(data_loader, desc="Scoring")
    for key, body in pbar:
        try:
            res = model.predict(body)
            pd.DataFrame(res, index=key).round(5).rename_axis('Source').reset_index().to_csv(output_file+".csv", mode='a', index=False, header=use_header)
        except Exception:
            invalid_count += args.chunk_size
            continue
        total_count += 1
        if total_count % args.partition == 0:
            output_file += '_p'
        use_header = False
        pbar.set_postfix({'Invalid': {f"{invalid_count}"}})

if __name__ == "__main__":
    main()