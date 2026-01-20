import time
from aromma.model import AROMMA
from agent.paths import DATA_DIR
from langchain.tools import BaseTool
from langchain.tools import BaseTool
from typing import List, Optional
from rdkit import Chem

def canonical_smiles(smiles):
    return Chem.MolToSmiles(Chem.MolFromSmiles(smiles), isomericSmiles = True)

def remove_stereo(smiles):
    smiles = smiles.replace('@','')
    smiles = smiles.replace('/','')
    smiles = smiles.replace('\\','')
    return canonical_smiles(smiles)

class OdorPrediction(BaseTool):
    name: str = "OdorPrediction"
    description: str = (
        "Predict the odor descriptors for a given SMILES string using the POM model. "
        "Input: SMILES string. Output: list of odor descriptors."
    )
    return_direct: bool = False
    
    threshold: float = 0.5
    model: Optional[AROMMA] = None
    labels: Optional[List[str]] = None

    def __init__(self, threshold: float = 0.5, **kwargs):
        super().__init__(**kwargs)
        self.threshold = threshold
        self.model = AROMMA()
        with open(DATA_DIR / "labels_152.txt", "r") as f:
            self.labels = f.read().splitlines() # 152
         

    def _run(self, smiles: str) -> str:
        print(f"[TOOL] OdorPrediction called with input: {smiles}")

        if ";" in smiles:
            parts = smiles.split(";")
            smiles = [canonical_smiles(part.strip()) for part in parts]
            smiles = ";".join(smiles)
        else:
            smiles = canonical_smiles(smiles)
        prob = self.model.forward([smiles]) # [1 152]
        mask = prob[0] >= self.threshold
        indices = mask.nonzero(as_tuple=True)[0].cpu().tolist()
        pred = [self.labels[i] for i in indices]

        return pred

if __name__ == "__main__":
    time_start = time.time()

    tool = OdorPrediction()
    results = tool._run("CC(O)CN")
    
    time_end = time.time()
    print(f"Time taken: {time_end - time_start:.4f} sec")
    print(results)
