import torch.nn as nn
import torch
class HetConv2d(nn.Module):
    def __init__(self, in_feats, out_feats, p=2):
        super(HetConv2d_v2, self).__init__()
        self.in_feats = in_feats
        self.out_feats = out_feats
        self.blocks = nn.ModuleList()
        for i in range(out_feats):
            self.blocks.append(self.make_HetConv2d(i, p))

    def make_HetConv2d(self, n, p):
        layers = nn.ModuleList()
        for i in range(self.in_feats):
            if ((i - n) % (p)) == 0:
                layers.append(nn.Conv2d(1, 1, 3, 1, 1))

            else:
                layers.append(nn.Conv2d(1, 1, 1, 1, 0))
        return layers

    def forward(self, x):
        out = []
        for i in range(0, self.out_feats):
            out_ = self.blocks[i][0](x[:, 0: 1, :, :])
            for j in range(1, self.in_feats):
               out_ += self.blocks[i][j](x[:, j:j + 1, :, :])
            out.append(out_)
        return torch.cat(out, 1)

