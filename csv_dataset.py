import torch
from torch.utils.data import Dataset, DataLoader
import pandas as pd

class CSVDataset(Dataset):
    def __init__(self, path, header=None, chunk_size=1000):
        self.path = path
        self.chunk_size = chunk_size
        self.header = header
        self.length = sum(1 for line in open(path))
        self.id_count = 0
        
    def __getitem__(self, idx):
        data_chunk = next(pd.read_csv(self.path,
                                skiprows=idx * self.chunk_size,
                                chunksize=self.chunk_size,
                                names=self.header))
        key = data_chunk[self.header[0]].values.tolist()
        body = data_chunk[self.header[-1]].values.tolist()
        return key, body
    
    def __len__(self):
        return self.length // self.chunk_size
