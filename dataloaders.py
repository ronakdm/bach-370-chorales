from torch.utils.data import Dataset, DataLoader, RandomSampler
import pickle


class MusicDataset(Dataset):
    def __init__(self, file_path="chorales_tensor.p", seq_len=16):

        self.seq_len = seq_len
        self.data = pickle.load(open(file_path, "rb"))
        self.num_parts, self.num_pitches, total_len = self.data.shape
        self.len = total_len // seq_len

    def __len__(self):
        return self.len

    def __getitem__(self, item):
        return self.data[:, :, item * self.seq_len : (item + 1) * self.seq_len]


# TODO: Make train, validation, and test splits.
def make_dataloaders(batch_size):
    dataset = MusicDataset()
    dataloader = DataLoader(
        dataset, sampler=RandomSampler(dataset), batch_size=batch_size
    )

    return dataloader
