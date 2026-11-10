# AROMMA SCENTLAB
### AI-Powered Molecular Fragrance Intelligence

AROMMA ScentLab is an interactive, full-stack scientific fragrance intelligence platform built on top of [AROMMA (Aggregated Representations of Olfaction via Molecule and Mixture Alignment)](https://github.com/DGIST-Distributed-AI-Lab/aromma).

It enables perfumers, cosmetic chemists, and fragrance researchers to:
- **Predict Odor Profiles** of single molecules from SMILES representations.
- **Analyze Binary Fragrance Mixtures** to understand notes harmonization.
- **Design Scent Formulations** through natural language querying using local LLaMA-3 (via Ollama) mapped to curated ingredient databases.

---

## 🚀 Quick Launch (Web Application)

```bash
# 1. Activate the Conda environment
conda activate aromma_agent_env

# 2. Navigate to project root
cd "/home/kote/Downloads/AROMMA EMBEEDINGS/aromma-agent"

# 3. Launch the web application
python -m streamlit run app.py
```
Or simply run the one-click launcher:
```bash
./run_app.sh
```

The application will be accessible in your web browser at:
👉 **`http://localhost:8501`**

---

## 🧪 System Architecture & Tech Stack

- **Frontend & Web Server**: Streamlit 1.50 with bespoke luxury laboratory dark UI theme.
- **Inference Engine**: PyTorch 2.3.0 running `aromma_best_fold.pt` (SPMM with LoRA).
- **Cheminformatics**: RDKit 2023.3.1 for SMILES validation, canonicalization, and 2D topology SVG rendering.
- **Language Model**: LLaMA 3 8B running locally through Ollama.
- **Orchestration**: LangChain & RMRKL agent for natural-language scent design.

---

## 🛠️ Original CLI Setup Reference

1. **Environment setup**:
   - `conda env create -f environment.yml`
   - `conda activate aromma_agent_env`
2. **Ollama & Model**:
   - `curl -fsSL https://ollama.com/install.sh | sh`
   - `ollama run llama3:8b`
3. **Model Checkpoint**:
   - Checkpoint stored at `aromma/aromma_best_fold.pt`.
4. **Original CLI Agent**:
   - `python run.py`
