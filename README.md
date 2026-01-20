# AROMMA Agent

## Overview
AROMMA Agent is an LLM-powered odor prediction and recommendation system built on top of [AROMMA (Aggregated Representations of Olfaction via Molecule and Mixture Alignment)](https://github.com/DGIST-Distributed-AI-Lab/aromma)

It supports the following capabilities:
- Odor prediction from a molecule or a binary mixture given SMILES strings
- Molecule recommendation for composing a target scent described in natural language

## Setup
1. Create and activate the conda environment:
    - `conda env create -f environment.yml`
    - `conda activate aromma_agent_env`
2. Install and run LLaMA via Ollama
    - `curl -fsSL https://ollama.com/install.sh | sh`
    - `ollama run llama3:8b`

## Download trained checkpoints
Download the trained AROMMA model checkpoint [aromma_best_fold.pt](https://huggingface.co/riverallzero/aromma/blob/main/aromma_best_fold.pt) and place under the `aromma` directory.

## Running the Agent
`python run.py`

### Required Source Code modification
Due to a compatibility issue between rmrkl and Pydantic v2, the following error may occur:
```
pydantic.errors.PydanticUserError: Field 'name' defined on a base class was overridden by a non-annotated attribute. All field definitions, including overrides, require a type annotation.
```

Edit the file `<conda_env_path>/lib/python3.9/site-packages/rmrkl/executor.py` as follows:

```python
class ExceptionTool(BaseTool):
    # name = "_Exception"
    # description = "Exception tool"
    name: str = "ExceptionTool"
    description: str = "Handles exceptions gracefully."
```

### Basic Usage Example
#### Task 1. Odor Prediction
Given a SMILES string (single molecule or binary mixture), the agent predicts odor descriptors using AROMMA and produces a natural-language description.

- Single molecule
  ```
  Q. How does the molecule CCC1=C(O)C(=O)CC1 smell like?

  Action: OdorPrediction
  Action Input: CCC1=C(O)C(=O)CC1
  Observation: ['caramellic']

  A. The given SMILES smells caramellic.
  ```

- Binary Mixture
  ```
  Q. How does the mixture blend with CC(C)COC(=O)Cc1ccccc1 and CCCCCOC(=O)Cc1ccccc1 smell like?

  Action: OdorPrediction
  Action Input: CC(C)COC(=O)Cc1ccccc1;CCCCOC(=O)Cc1ccccc1
  Observation: ['floral', 'fruity', 'honey', 'sweet']

  A. The mixture blends with a sweet, floral, and fruity scent, reminiscent of honey.
  ```

- Over two molecules
  ```
  Q. How does the mixture blend with CC(C)COC(=O)Cc1ccccc1, CCCCCOC(=O)Cc1ccccc1 and CCC1=C(O)C(=O)CC1 smell like?

  Action: OdorPrediction
  Action Input: CC(C)COC(=O)Cc1ccccc1;CCCCOC(=O)Cc1ccccc1;CCC1=C(O)C(=O)CC1
  Observation: []

  A. Sorry, we can only process up to 2 SMILES at a time.
  ```

#### Task 2. Molecule Recommendation

Given a natural-language description of a desired scent:
- The agent selects 2–6 odor descriptors from a fixed vocabulary of 152 descriptors.
- These descriptors are used to retrieve and recommend suitable molecular ingredients.

```
Q. I want to make a scent that captures the feeling of running through a grassy field.

Action: MolRecommendation
Action Input: ["fresh", "green", "herbal", "grass"]
Observation: The scent may resemble ['fresh', 'green', 'herbal', 'grass'].
Here are some ingredients you can use to create this fragrance:
- SMILES: CCC=CCCOC(=O)C=Cc1ccccc1, descriptors: green;fresh;balsamic;herbal, matched(3): ['fresh', 'green', 'herbal']
- SMILES: C=C(C)CCO, descriptors: green;fruity;sweet;herbal;fresh, matched(3): ['fresh', 'green', 'herbal']
- SMILES: CCCCCCC1OCC(C)O1, descriptors: green;fruity;fatty;herbal;fresh, matched(3): ['fresh', 'green', 'herbal']
```
