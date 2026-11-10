from typing import Tuple, Optional
from rdkit import Chem

def validate_smiles(smiles: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Validate a single SMILES string using RDKit.
    Returns: (is_valid, canonical_smiles, error_message)
    """
    if not smiles or not smiles.strip():
        return False, None, "SMILES string cannot be empty."
    
    clean_smiles = smiles.strip()
    try:
        mol = Chem.MolFromSmiles(clean_smiles)
        if mol is None:
            return False, None, f"Invalid chemical structure: '{clean_smiles}' could not be parsed by RDKit."
        
        canon = Chem.MolToSmiles(mol, isomericSmiles=True)
        return True, canon, None
    except Exception as e:
        return False, None, f"SMILES validation error: {str(e)}"

def validate_mixture_smiles(smiles_a: str, smiles_b: str) -> Tuple[bool, Optional[str], Optional[str], Optional[str]]:
    """
    Validate two SMILES strings for binary mixture prediction.
    Returns: (is_valid, canon_a, canon_b, error_message)
    """
    valid_a, canon_a, err_a = validate_smiles(smiles_a)
    if not valid_a:
        return False, None, None, f"Ingredient A: {err_a}"
    
    valid_b, canon_b, err_b = validate_smiles(smiles_b)
    if not valid_b:
        return False, None, None, f"Ingredient B: {err_b}"
    
    return True, canon_a, canon_b, None
