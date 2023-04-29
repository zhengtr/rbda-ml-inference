import argparse
from csv_dataset import CSVDataset
from detoxify import Detoxify
from logger import create_logger
import torch
import pandas as pd
import os
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Inference')
parser.add_argument("--data_type", choices=['questions', 'answers'], type=str, help="Data Type")
parser.add_argument("--data_path", default="./sample_data/mini_answers_id",type=str, help="Path to data file")
parser.add_argument("--chunk_size", default=2, type=int, help="Inference batch size")
parser.add_argument("--output_path", default="./sample_data/mini_answers_score",type=str, help="Path to output file")


def main():
    args = parser.parse_args()
    logger = create_logger("inference.log")
    if torch.cuda.is_available():
        device = torch.device('cuda') 
    else:
        device = torch.device('cpu')
    logger.info(f'Using device: {str(device).upper()}.')

    # dataset
    if args.data_type == "questions":
        header = ["Source", "YearOfCreation", "Id", "Score", "Body"]
    else:
        header = ["Source", "YearOfCreation", "ParentId", "Score", "Body"]
    my_dataset = CSVDataset(path=args.data_path, header=header, chunk_size=args.chunk_size)
    data_loader = torch.utils.data.DataLoader(my_dataset, collate_fn=lambda x: x[0], batch_size=1, shuffle=False)
    
    model = Detoxify('original', device=device)
    use_header = True
    for key, body in tqdm(data_loader, desc="Scoring"):
        res = model.predict(body)
        pd.DataFrame(res, index=key).round(5).rename_axis('Source').reset_index().to_csv(args.output_path, mode="a", index=False, header=use_header)
        use_header = False

if __name__ == "__main__":
    main()