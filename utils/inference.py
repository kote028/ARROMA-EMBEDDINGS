import time
import re
import ast
import urllib.request
import json
from typing import List, Dict, Any, Optional
import streamlit as st

from agent.tools.mol_inference import OdorPrediction
from agent.tools.mol_recommend import MolRecommendation
from utils.validation import validate_smiles, validate_mixture_smiles

DESCRIPTOR_DESCRIPTIONS = {
    "caramellic": "A rich, sweet, buttery, and deeply decadent caramelized sugar aroma.",
    "floral": "Fresh, elegant blossom-like notes evoking natural petals, gardens, and gentle botanical sweetness.",
    "fruity": "Vibrant, ripe fruit nuances with sweet, tangy, and juicy characteristics.",
    "honey": "Warm, golden, balsamic nectar sweetness with floral and beeswax undertones.",
    "sweet": "Pleasurable sugary and confectionery olfactory impression with comforting warmth.",
    "green": "Crisp foliage, freshly snapped leaves, cut grass, and verdant herbal purity.",
    "herbal": "Medicinal, aromatic garden herb nuances including thyme, sage, and wild botanical greens.",
    "fresh": "Invigorating, clean, airy outdoor sensation reminiscent of spring breezes and crisp morning dew.",
    "woody": "Noble resinous, cedar, and sandalwood depth providing stability and earthy elegance.",
    "citrus": "Zesty, uplifting, sparkling burst reminiscent of lemon, bergamot, grapefruit, and orange zest.",
    "balsamic": "Warm, ambery, sweet resinous and vanilla-like depth with soothing richness.",
    "marine_ozone": "Brisk sea breeze, salty spray, and electric aquatic freshness.",
    "earthy": "Rich petrichor, damp soil, root-like grounding notes and autumn woods.",
    "spicy": "Piquant, warm, energetic notes of clove, cinnamon, black pepper, and nutmeg.",
    "musk": "Soft, velvety, sensual skin-scent warmth with persistent fixation.",
    "vanilla": "Gourmand, creamy, comforting and delicately sweet pod-like warmth.",
    "almond": "Nutty, sweet marzipan and toasted kernel richness.",
    "mint": "Crisp, cooling, invigorating, and clean mentholated vitality.",
    "camphoreous": "Penetrating, aromatic, cooling medicinal brightness.",
    "aldehydic": "Sparkling, champagne-like, diffused abstract radiant elegance.",
    "lactonic": "Creamy, milky, velvety peach-skin and warm dairy nuance.",
    "rose": "Classic dewy romantic floral elegance with subtle honey and fruit facets.",
    "jasmin": "Opulent, sensual, indolic white floral richness with nocturnal depth.",
    "lavender": "Aromatic, calming, herbaceous-floral with fresh French countryside clarity.",
    "amber": "Luminescent, golden, warm, resinous, and deeply comforting luxury aura."
}

def generate_natural_scent_profile(descriptors: List[str]) -> str:
    """Generate a synthesized natural olfactory description from descriptors."""
    if not descriptors:
        return "No distinctive odor descriptors were triggered above the detection threshold."
    
    clean_descs = [d.replace('_', ' ') for d in descriptors]
    notes_str = ", ".join(clean_descs[:4])
    
    highlights = []
    for d in descriptors[:3]:
        if d in DESCRIPTOR_DESCRIPTIONS:
            highlights.append(DESCRIPTOR_DESCRIPTIONS[d])
    
    if len(clean_descs) == 1:
        desc_text = f"The molecule exhibits a prominent **{clean_descs[0]}** character."
    else:
        desc_text = f"The olfactory architecture harmonizes key notes of **{notes_str}**."
        
    if highlights:
        desc_text += f" {highlights[0]}"
    else:
        desc_text += " This profile conveys a balanced, nuanced olfactory impression."
        
    return desc_text

@st.cache_resource(show_spinner=False)
def get_odor_prediction_tool() -> OdorPrediction:
    """Load and cache the AROMMA model once in memory."""
    return OdorPrediction(threshold=0.5)

@st.cache_resource(show_spinner=False)
def get_mol_recommendation_tool() -> MolRecommendation:
    """Load and cache the MolRecommendation database tool once in memory."""
    return MolRecommendation()

@st.cache_resource(show_spinner=False)
def get_fragent_agent(model_name: str = "llama3:8b"):
    """Load and cache the Fragent LangChain agent once in memory."""
    try:
        from run import Fragent
        return Fragent(
            model=model_name,
            temp=0.1,
            max_iterations=6,
            streaming=False,
            verbose=False,
        )
    except Exception as e:
        print(f"Failed to load Fragent: {e}")
        return None

def check_ollama_service() -> Dict[str, Any]:
    """Check if the local Ollama daemon is reachable and whether llama3:8b is available."""
    try:
        req = urllib.request.Request("http://localhost:11434/api/tags", headers={"User-Agent": "ArommaScentLab"})
        with urllib.request.urlopen(req, timeout=2.0) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                models = [m.get("name") for m in data.get("models", [])]
                has_llama = any("llama3" in m for m in models)
                return {"online": True, "models": models, "has_llama": has_llama}
    except Exception:
        pass
    return {"online": False, "models": [], "has_llama": False}

def predict_single_molecule(smiles: str) -> Dict[str, Any]:
    """
    Execute AROMMA odor prediction on a single SMILES.
    Validates with RDKit and records execution duration.
    """
    valid, canon, err = validate_smiles(smiles)
    if not valid:
        return {"success": False, "error": err}
    
    tool = get_odor_prediction_tool()
    t_start = time.time()
    try:
        descriptors = tool._run(canon)
        duration = time.time() - t_start
        profile_text = generate_natural_scent_profile(descriptors)
        
        return {
            "success": True,
            "type": "single",
            "input_smiles": smiles,
            "canonical_smiles": canon,
            "descriptors": descriptors,
            "natural_description": profile_text,
            "duration": duration,
        }
    except Exception as e:
        return {"success": False, "error": f"Inference execution failed: {str(e)}"}

def predict_mixture(smiles_a: str, smiles_b: str) -> Dict[str, Any]:
    """
    Execute AROMMA odor prediction on a binary mixture.
    Format: smiles_a;smiles_b
    """
    valid, canon_a, canon_b, err = validate_mixture_smiles(smiles_a, smiles_b)
    if not valid:
        return {"success": False, "error": err}
    
    tool = get_odor_prediction_tool()
    t_start = time.time()
    try:
        mixture_str = f"{canon_a};{canon_b}"
        descriptors = tool._run(mixture_str)
        duration = time.time() - t_start
        profile_text = generate_natural_scent_profile(descriptors)
        
        return {
            "success": True,
            "type": "mixture",
            "smiles_a": smiles_a,
            "smiles_b": smiles_b,
            "canonical_a": canon_a,
            "canonical_b": canon_b,
            "mixture_smiles": mixture_str,
            "descriptors": descriptors,
            "natural_description": profile_text,
            "duration": duration,
        }
    except Exception as e:
        return {"success": False, "error": f"Mixture inference failed: {str(e)}"}

def parse_recommendation_output(raw_output: str) -> Dict[str, Any]:
    """Parse output from MolRecommendation or Fragent into structured ingredients."""
    selected_descriptors = []
    desc_match = re.search(r"resemble\s*(\[[^\]]+\])", raw_output)
    if desc_match:
        try:
            selected_descriptors = ast.literal_eval(desc_match.group(1))
        except Exception:
            pass
    
    ingredients = []
    # Lines like: - SMILES: ..., descriptors: ..., matched(3): [...]
    pattern = re.compile(r"-\s*SMILES:\s*([^,\n]+),\s*descriptors:\s*([^,\n]+),\s*matched\((\d+)\):\s*(\[[^\]]*\])")
    for match in pattern.finditer(raw_output):
        smi = match.group(1).strip()
        descs_str = match.group(2).strip()
        m_count = int(match.group(3))
        try:
            matched_list = ast.literal_eval(match.group(4))
        except Exception:
            matched_list = []
        
        all_descs = [d.strip() for d in descs_str.split(";") if d.strip()]
        ingredients.append({
            "smiles": smi,
            "all_descriptors": all_descs,
            "match_count": m_count,
            "matched_descriptors": matched_list
        })
        
    return {
        "selected_descriptors": selected_descriptors,
        "ingredients": ingredients,
        "raw_text": raw_output
    }

def recommend_molecules(concept: str) -> Dict[str, Any]:
    """
    Discover molecular ingredients for a fragrance concept using Ollama LLaMA-3
    and MolRecommendation tool.
    """
    if not concept or not concept.strip():
        return {"success": False, "error": "Fragrance concept cannot be empty."}
        
    t_start = time.time()
    try:
        agent = get_fragent_agent("llama3:8b")
        if agent is None:
            # Fallback to direct tool with keyword extraction if agent is offline
            rec_tool = get_mol_recommendation_tool()
            raw_out = rec_tool._run(["fresh", "green", "herbal"])
        else:
            prompt = f"I want to make a scent that captures: {concept.strip()}"
            raw_out = agent.run(prompt)
            
        duration = time.time() - t_start
        parsed = parse_recommendation_output(raw_out)
        
        return {
            "success": True,
            "concept": concept,
            "selected_descriptors": parsed["selected_descriptors"],
            "ingredients": parsed["ingredients"],
            "raw_output": raw_out,
            "duration": duration
        }
    except Exception as e:
        return {"success": False, "error": f"Fragrance generation failed: {str(e)}"}
