from aromma import SPMM, EndToEndModel
from aromma.paths import AROMMA_DIR
import torch
import torch.nn as nn

class AROMMA(nn.Module):
    def __init__(self):
        super().__init__()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.load_model()

    def load_model(self):
        self.embedder = SPMM(r=4, lora_alpha=8)
        self.model = EndToEndModel(
            embedder=self.embedder,
            sattn_hidden_dim=196,
            cattn_hidden_dim=384,
            num_heads=4,
            num_labels=152,
        ).to(self.device)
        self.model.load_state_dict(
            torch.load(AROMMA_DIR / "aromma_best_fold.pt", map_location=self.device)
        )
        self.model.eval()
    
    def forward(self, smiles):
        with torch.no_grad():
            logit = self.model.forward(smiles)
        return logit
