"""
We stream text here
"""
import numpy as np
import torch
from pytorch_stream_dataloader.stream_dataloader import StreamDataLoader
from pytorch_stream_dataloader.stream_dataset import StreamDataset
from pytorch_stream_dataloader.utils import split_batch_size, split_dataset_sizes


class TextStream(object):
    def __init__(self, text, tbins):
        self.text = np.fromstring(text, dtype=np.uint8)
        self.iter = 0
        self.tbins = tbins

    def __iter__(self):
        for i in range(0, len(self.text), self.tbins):
            data = self.text[i:i+self.tbins]
            #pad to tbins
            frame = np.zeros((1, self.tbins), dtype=np.float32)
            frame[0,:len(data)] = data
            yield (torch.from_numpy(frame), 0)



def collate_fn(data_list):
    texts, _ = zip(*data_list)
    texts = torch.cat(texts)
    return texts


class TextLoader(StreamDataLoader):
    def __init__(self, texts, batch_size, num_workers, tbins=5):
        def iterator_fun(text):
            return TextStream(text, tbins)
        dataset = StreamDataset(texts, iterator_fun, batch_size, "data", None)
        super().__init__(dataset, num_workers, collate_fn)


