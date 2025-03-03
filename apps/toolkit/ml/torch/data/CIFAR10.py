import torch
from torch.utils.data import Dataset
from datasets import load_dataset
from torchvision import transforms
import numpy as np
from torch.utils.data import DataLoader

class CIFAR10Dataset(Dataset):
    def __init__(self, split='train', transform=None):
        self.dataset = load_dataset('cifar10', split=split)
        self.transform = transform or self._default_transform()

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        image = self.dataset[idx]['img']
        label = self.dataset[idx]['label']
        if self.transform:
            image = self.transform(image)
        return image, label

    def _default_transform(self):
        return transforms.Compose([
            transforms.ToTensor(),
            transforms.Resize((224, 224)),  # MobileNetV3 typically expects 224x224 input
            transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))  # CIFAR-10 mean and std
        ])

# Usage example
train_dataset = CIFAR10Dataset(split='train')
test_dataset = CIFAR10Dataset(split='test')

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

"""
# Get the first batch
images, labels = next(iter(train_loader))

# Print information about the batch
print(f"Batch shape: {images.shape}")
print(f"Labels shape: {labels.shape}")
"""