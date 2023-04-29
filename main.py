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
parser.add_argument("--data_path", default="./sample_data/mini_answers",type=str, help="Path to data file")
parser.add_argument("--chunk_size", default=2, type=int, help="Inference batch size")


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
    for key, body in tqdm(data_loader, desc="Scoring"):
        res = model.predict(body)
        print(pd.DataFrame(res, index=key).round(5))
        
    raise NotImplementedError
    
    test_text = [
        "<p>the solution can be obtained by using the <strong>outputstream</strong> and using <strong>files.",
        "Hey fk you",
        "<p>Dumbass, the solution can be obtained by using the <strong>outputstream</strong> and using <strong>files.",
    ]
    result = model.predict(test_text)
    print(pd.DataFrame(result, index=test_text).round(5))

if __name__ == "__main__":
    main()