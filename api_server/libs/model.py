# import timm

# import torch.nn as nn

from typing import Any


# class BuildModel(nn.Module):
#     def __init__(self):
#         super().__init__()
#         self.model = timm.create_model("resnet18d", pretrained = None)
#         n_features = self.model.fc.in_features
#         self.model.fc = nn.Linear(n_features, 1, bias = True)
            
#     def forward(self, x) -> Any:
#         x = self.model(x)
#         return x