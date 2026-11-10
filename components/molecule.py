from typing import Optional
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem.Draw import rdMolDraw2D
import base64

def smiles_to_svg(smiles: str, width: int = 340, height: int = 180) -> Optional[str]:
    """
    Generate an SVG chemical structure depiction using RDKit with luxury dark theme styling.
    """
    try:
        mol = Chem.MolFromSmiles(smiles)
        if not mol:
            return None
            
        d2d = rdMolDraw2D.MolDraw2DSVG(width, height)
        opts = d2d.drawOptions()
        opts.clearBackground = True
        opts.bondLineWidth = 2.0
        
        d2d.DrawMolecule(mol)
        d2d.FinishDrawing()
        svg_text = d2d.GetDrawingText()
        
        # Modify colors in SVG for dark luxury styling (white/gold bonds)
        svg_text = svg_text.replace("stroke:#000000", "stroke:#F3EFE5")
        svg_text = svg_text.replace("fill:#000000", "fill:#F3EFE5")
        return svg_text
    except Exception:
        return None

def smiles_to_base64_png(smiles: str, width: int = 340, height: int = 180) -> Optional[str]:
    """Fallback to PNG if needed."""
    try:
        mol = Chem.MolFromSmiles(smiles)
        if not mol:
            return None
        img = Draw.MolToImage(mol, size=(width, height))
        import io
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        return f"data:image/png;base64,{b64}"
    except Exception:
        return None
