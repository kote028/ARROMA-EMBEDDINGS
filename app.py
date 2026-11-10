import time
import streamlit as st

# Configure page settings
st.set_page_config(
    page_title="AROMMA SCENTLAB — Molecular Fragrance Intelligence",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

from components.styles import apply_custom_styles
from components.results import (
    display_single_result,
    display_mixture_result,
    display_recommendation_result,
)
from utils.inference import (
    predict_single_molecule,
    predict_mixture,
    recommend_molecules,
    check_ollama_service,
)
from utils.validation import validate_smiles

# Apply custom CSS
apply_custom_styles()

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

if "nav_selection" not in st.session_state:
    st.session_state.nav_selection = "Overview"

if "single_input" not in st.session_state:
    st.session_state.single_input = "CCC1=C(O)C(=O)CC1"

if "mix_input_a" not in st.session_state:
    st.session_state.mix_input_a = "CC(C)COC(=O)Cc1ccccc1"

if "mix_input_b" not in st.session_state:
    st.session_state.mix_input_b = "CCCCOC(=O)Cc1ccccc1"

if "concept_input" not in st.session_state:
    st.session_state.concept_input = "I want to create a scent that captures the feeling of running through a grassy field."

# Service health check
ollama_info = check_ollama_service()

# --- TOP NAVIGATION & BRANDING ---
st.markdown("""
<div class="scentlab-header">
    <div class="brand-container">
        <div style="font-size: 2.2rem; color: #C7A56B;">⚗️</div>
        <div>
            <div class="brand-mark">AROMMA SCENTLAB</div>
            <div class="brand-tagline">AI-Powered Molecular Fragrance Intelligence</div>
        </div>
    </div>
    <div style="display: flex; gap: 0.8rem; align-items: center;">
        <div class="status-badge">
            <span class="status-dot"></span>
            AROMMA Engine: Online
        </div>
        <div class="status-badge">
            <span class="status-dot" style="background-color: """ + ("#4ADE80" if ollama_info["online"] else "#E11D48") + """; box-shadow: 0 0 8px """ + ("#4ADE80" if ollama_info["online"] else "#E11D48") + """;"></span>
            LLM (Ollama): """ + ("Online" if ollama_info["online"] else "Offline") + """
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION & SYSTEM SPECS ---
with st.sidebar:
    st.markdown("<div style='font-family: Cinzel, serif; font-size: 1.1rem; color: #C7A56B; font-weight: 600; margin-bottom: 0.8rem;'>Navigation</div>", unsafe_allow_html=True)
    
    pages = [
        "Overview",
        "Molecular Analysis",
        "Mixture Analysis",
        "Scent Designer",
        "About AROMMA"
    ]
    
    # Handle page selection
    selected_page = st.radio(
        "Navigate",
        pages,
        index=pages.index(st.session_state.nav_selection) if st.session_state.nav_selection in pages else 0,
        label_visibility="collapsed"
    )
    st.session_state.nav_selection = selected_page

    st.markdown("---")
    st.markdown("<div style='font-family: Cinzel, serif; font-size: 0.95rem; color: #F3EFE5; font-weight: 600; margin-bottom: 0.6rem;'>System Architecture</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size: 0.82rem; color: #A5A9B0; line-height: 1.7;">
        <div>• <strong>AROMMA:</strong> SPMM + LoRA Alignment</div>
        <div>• <strong>Cheminformatics:</strong> RDKit 2023.03</div>
        <div>• <strong>Inference Engine:</strong> PyTorch 2.3.0</div>
        <div>• <strong>Language Model:</strong> LLaMA 3 8B (Ollama)</div>
        <div>• <strong>Descriptors:</strong> 152 Sensory Classes</div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.history:
        st.markdown("---")
        st.markdown(f"<div style='font-family: Cinzel, serif; font-size: 0.95rem; color: #F3EFE5; font-weight: 600;'>Session History ({len(st.session_state.history)})</div>", unsafe_allow_html=True)
        for idx, item in enumerate(reversed(st.session_state.history[-5:]), 1):
            st.markdown(f"<div style='font-size: 0.78rem; color: #C7A56B; margin-top: 0.4rem;'>#{idx} {item.get('title', 'Analysis')}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 0.72rem; color: #A5A9B0;'>{item.get('summary', '')}</div>", unsafe_allow_html=True)
        
        if st.button("Clear Session History", use_container_width=True):
            st.session_state.history = []
            st.rerun()

# ==========================================
# PAGE 1: OVERVIEW
# ==========================================
if selected_page == "Overview":
    st.markdown("""
    <div class="hero-container">
        <div class="hero-heading">Discover the Science Behind Every Scent.</div>
        <div class="hero-sub">
            Transform molecular structures into meaningful olfactory intelligence with AROMMA. Decode pure chemical compounds, predict complex binary fragrance mixtures, and create bespoke fragrance formulations using AI.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="scent-card">
            <div>
                <div class="card-icon">🔬</div>
                <div class="card-title">Molecular Intelligence</div>
                <div class="card-desc">
                    Predict the odor profile of an individual molecule from its SMILES chemical notation with multi-label deep learning.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch Single Analysis", key="btn_nav_single", use_container_width=True):
            st.session_state.nav_selection = "Molecular Analysis"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="scent-card">
            <div>
                <div class="card-icon">⚖️</div>
                <div class="card-title">Mixture Intelligence</div>
                <div class="card-desc">
                    Understand how two distinct molecular ingredients interact, blend, and harmonize to yield a unified sensory signature.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch Mixture Blend", key="btn_nav_mix", use_container_width=True):
            st.session_state.nav_selection = "Mixture Analysis"
            st.rerun()

    with col3:
        st.markdown("""
        <div class="scent-card">
            <div>
                <div class="card-icon">✨</div>
                <div class="card-title">AI Scent Designer</div>
                <div class="card-desc">
                    Describe a mood, natural scene, or sensory memory in plain English. Let LLaMA-3 formulate the molecular candidates.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Design Signature Fragrance", key="btn_nav_rec", use_container_width=True):
            st.session_state.nav_selection = "Scent Designer"
            st.rerun()

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background: #15181F; border: 1px solid #2D333F; border-radius: 12px; padding: 1.5rem;">
        <div style="font-family: Cinzel, serif; font-size: 1.1rem; color: #C7A56B; margin-bottom: 0.6rem;">Operational Status & Live Systems</div>
        <div style="font-size: 0.88rem; color: #A5A9B0; line-height: 1.6;">
            • <strong>AROMMA Model Checkpoint:</strong> Verified loaded (<code>aromma/aromma_best_fold.pt</code>, 170 MB)<br>
            • <strong>Sensory Vocabulary:</strong> 152 Curated Odor Descriptors initialized<br>
            • <strong>Chemical Validation:</strong> RDKit Isomeric & Stereochemical engine active<br>
            • <strong>Local LLM Backend:</strong> Ollama LLaMA-3 (8B Parameters) verified running locally
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# PAGE 2: MOLECULAR ANALYSIS
# ==========================================
elif selected_page == "Molecular Analysis":
    st.markdown("<h2 style='margin-bottom: 0.2rem;'>Molecular Odor Analysis</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color: #A5A9B0; margin-bottom: 1.5rem;'>Enter a molecular SMILES representation to discover its predicted odor characteristics.</div>", unsafe_allow_html=True)

    # Preset examples
    st.markdown("<span style='font-size: 0.8rem; color: #C7A56B; font-weight: 600;'>TRY A KNOWN REFERENCE MOLECULE:</span>", unsafe_allow_html=True)
    exp_col1, exp_col2, exp_col3, exp_col4 = st.columns(4)
    with exp_col1:
        if st.button("CCC1=C(O)C(=O)CC1 (Caramel)", key="ex_caramel", use_container_width=True):
            st.session_state.single_input = "CCC1=C(O)C(=O)CC1"
            st.rerun()
    with exp_col2:
        if st.button("CC(O)CN (Amine/Nutty)", key="ex_amine", use_container_width=True):
            st.session_state.single_input = "CC(O)CN"
            st.rerun()
    with exp_col3:
        if st.button("O=Cc1ccccc1 (Benzaldehyde/Almond)", key="ex_benz", use_container_width=True):
            st.session_state.single_input = "O=Cc1ccccc1"
            st.rerun()
    with exp_col4:
        if st.button("CC1=CC(C)C(CO)CC1 (Floral/Green)", key="ex_floral", use_container_width=True):
            st.session_state.single_input = "CC1=CC(C)C(CO)CC1"
            st.rerun()

    smiles_input = st.text_input(
        "Molecular SMILES Representation",
        value=st.session_state.single_input,
        placeholder="e.g. CCC1=C(O)C(=O)CC1",
        help="Input a valid SMILES string representing the molecular structure."
    )
    st.session_state.single_input = smiles_input

    # Real-time RDKit format check
    if smiles_input.strip():
        is_valid, canon, err = validate_smiles(smiles_input)
        if not is_valid:
            st.warning(f"⚠️ {err}")
        else:
            st.markdown(f"<div style='font-size: 0.78rem; color: #4ADE80;'>✓ Valid Chemical Structure &nbsp;|&nbsp; Canonical: <code>{canon}</code></div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
    if st.button("ANALYZE MOLECULE", key="btn_run_single"):
        with st.spinner("Decoding molecular olfactory descriptors via AROMMA..."):
            result = predict_single_molecule(smiles_input)
            st.session_state.last_single_result = result
            
            if result.get("success"):
                st.session_state.history.append({
                    "title": f"Single: {smiles_input[:15]}...",
                    "summary": ", ".join(result.get("descriptors", [])) or "No descriptors"
                })

    if "last_single_result" in st.session_state:
        display_single_result(st.session_state.last_single_result)


# ==========================================
# PAGE 3: MIXTURE ANALYSIS
# ==========================================
elif selected_page == "Mixture Analysis":
    st.markdown("<h2 style='margin-bottom: 0.2rem;'>Fragrance Mixture Intelligence</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color: #A5A9B0; margin-bottom: 1.5rem;'>Explore the combined olfactory characteristics of two molecular ingredients blended in a binary mixture.</div>", unsafe_allow_html=True)

    # Preset examples
    st.markdown("<span style='font-size: 0.8rem; color: #C7A56B; font-weight: 600;'>TRY A VERIFIED BINARY COMBINATION:</span>", unsafe_allow_html=True)
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        if st.button("CC(C)COC(=O)Cc1ccccc1 + CCCCOC(=O)Cc1ccccc1 (Floral/Honey)", key="ex_mix1", use_container_width=True):
            st.session_state.mix_input_a = "CC(C)COC(=O)Cc1ccccc1"
            st.session_state.mix_input_b = "CCCCOC(=O)Cc1ccccc1"
            st.rerun()
    with m_col2:
        if st.button("CCC1=C(O)C(=O)CC1 + O=Cc1ccccc1 (Caramel + Almond)", key="ex_mix2", use_container_width=True):
            st.session_state.mix_input_a = "CCC1=C(O)C(=O)CC1"
            st.session_state.mix_input_b = "O=Cc1ccccc1"
            st.rerun()

    st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)
    col_a, col_icon, col_b = st.columns([10, 2, 10])

    with col_a:
        st.markdown("<div style='font-family: Cinzel, serif; font-size: 0.95rem; color: #C7A56B; font-weight: 600;'>Ingredient A</div>", unsafe_allow_html=True)
        smiles_a = st.text_input(
            "Ingredient A SMILES",
            value=st.session_state.mix_input_a,
            key="input_mix_a",
            label_visibility="collapsed"
        )
        st.session_state.mix_input_a = smiles_a
        if smiles_a.strip():
            val_a, can_a, err_a = validate_smiles(smiles_a)
            if not val_a:
                st.warning(f"⚠️ {err_a}")
            else:
                st.markdown(f"<div style='font-size: 0.75rem; color: #4ADE80;'>✓ Valid SMILES</div>", unsafe_allow_html=True)

    with col_icon:
        st.markdown("<div style='display:flex; justify-content:center; align-items:center; height:100%; font-size: 2rem; color: #C7A56B; padding-top: 1.5rem;'>⚗️</div>", unsafe_allow_html=True)

    with col_b:
        st.markdown("<div style='font-family: Cinzel, serif; font-size: 0.95rem; color: #C7A56B; font-weight: 600;'>Ingredient B</div>", unsafe_allow_html=True)
        smiles_b = st.text_input(
            "Ingredient B SMILES",
            value=st.session_state.mix_input_b,
            key="input_mix_b",
            label_visibility="collapsed"
        )
        st.session_state.mix_input_b = smiles_b
        if smiles_b.strip():
            val_b, can_b, err_b = validate_smiles(smiles_b)
            if not val_b:
                st.warning(f"⚠️ {err_b}")
            else:
                st.markdown(f"<div style='font-size: 0.75rem; color: #4ADE80;'>✓ Valid SMILES</div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    if st.button("ANALYZE MIXTURE", key="btn_run_mix"):
        with st.spinner("Analyzing binary mixture interaction in AROMMA latent space..."):
            result = predict_mixture(smiles_a, smiles_b)
            st.session_state.last_mix_result = result
            
            if result.get("success"):
                st.session_state.history.append({
                    "title": f"Mixture Blend",
                    "summary": ", ".join(result.get("descriptors", [])) or "No descriptors"
                })

    if "last_mix_result" in st.session_state:
        display_mixture_result(st.session_state.last_mix_result)


# ==========================================
# PAGE 4: SCENT DESIGNER
# ==========================================
elif selected_page == "Scent Designer":
    st.markdown("<h2 style='margin-bottom: 0.2rem;'>Create Your Signature Scent</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color: #A5A9B0; margin-bottom: 1.5rem;'>Describe a feeling, memory, environment, or fragrance concept. Let AI discover suitable molecular ingredients.</div>", unsafe_allow_html=True)

    st.markdown("<span style='font-size: 0.8rem; color: #C7A56B; font-weight: 600;'>CURATED OLFACTORY CONCEPTS:</span>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("🌿 Fresh grassy morning", use_container_width=True):
            st.session_state.concept_input = "Fresh morning in a grassy field with morning dew"
            st.rerun()
    with c2:
        if st.button("🌊 Coastal ocean breeze", use_container_width=True):
            st.session_state.concept_input = "Ocean breeze and coastal freshness with marine ozone"
            st.rerun()
    with c3:
        if st.button("🍮 Warm vanilla & caramel", use_container_width=True):
            st.session_state.concept_input = "Warm vanilla and rich buttery sweet caramel"
            st.rerun()
    with c4:
        if st.button("🌲 Rain-soaked pine woods", use_container_width=True):
            st.session_state.concept_input = "Woody forest and cedar after heavy autumn rainfall"
            st.rerun()

    concept_text = st.text_area(
        "Describe your desired scent profile in natural language:",
        value=st.session_state.concept_input,
        height=100,
        placeholder="e.g. I want to make a scent that captures the feeling of running through a grassy field."
    )
    st.session_state.concept_input = concept_text

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
    if st.button("GENERATE SCENT RECOMMENDATIONS", key="btn_run_rec"):
        with st.spinner("Synthesizing fragrance notes via LLaMA-3 and querying molecular database..."):
            result = recommend_molecules(concept_text)
            st.session_state.last_rec_result = result
            
            if result.get("success"):
                st.session_state.history.append({
                    "title": f"Designer: {concept_text[:18]}...",
                    "summary": f"{len(result.get('ingredients', []))} candidates found"
                })

    if "last_rec_result" in st.session_state:
        display_recommendation_result(st.session_state.last_rec_result)


# ==========================================
# PAGE 5: ABOUT AROMMA
# ==========================================
elif selected_page == "About AROMMA":
    st.markdown("<h2 style='margin-bottom: 0.2rem;'>About AROMMA ScentLab</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color: #A5A9B0; margin-bottom: 1.5rem;'>Scientific Olfactory Intelligence & Architecture Overview</div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="background: #191D24; border: 1px solid #2D333F; border-radius: 14px; padding: 1.8rem; margin-bottom: 1.5rem;">
        <div style="font-family: Cinzel, serif; font-size: 1.25rem; color: #C7A56B; margin-bottom: 0.8rem;">AROMMA (Aggregated Representations of Olfaction via Molecule and Mixture Alignment)</div>
        <p style="color: #F3EFE5; line-height: 1.7; font-size: 0.95rem;">
            AROMMA is a state-of-the-art predictive olfactory model engineered to bridge the gap between chemical space and human sensory perception. Rather than treating scent as simple keyword categorization, AROMMA projects molecules and complex multi-component mixtures into a continuous Principal Odor Map (POM) learned across thousands of verified organoleptic evaluations.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style="background: #15181F; border: 1px solid #2D333F; border-radius: 12px; padding: 1.4rem; height: 100%;">
            <div style="font-family: Cinzel, serif; font-size: 1.05rem; color: #C7A56B; margin-bottom: 0.6rem;">Key Chemical & AI Foundations</div>
            <ul style="color: #A5A9B0; line-height: 1.8; font-size: 0.88rem; padding-left: 1.2rem;">
                <li><strong>SMILES (Simplified Molecular Input Line Entry System):</strong> Textual encoding of chemical topology and stereochemistry.</li>
                <li><strong>RDKit Cheminformatics:</strong> Validates chemical valence, computes stereochemical configurations, and generates canonical forms.</li>
                <li><strong>PyTorch Deep Learning:</strong> Runs the SPMM transformer with low-rank adaptation (LoRA) layers for fast, deterministic odor inference.</li>
                <li><strong>LLaMA 3 (8B) via Ollama:</strong> Semantic reasoning engine mapping abstract emotional and natural descriptions into structured sensory descriptors.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: #15181F; border: 1px solid #2D333F; border-radius: 12px; padding: 1.4rem; height: 100%;">
            <div style="font-family: Cinzel, serif; font-size: 1.05rem; color: #C7A56B; margin-bottom: 0.6rem;">End-to-End Pipeline</div>
            <div style="background: #111318; padding: 1rem; border-radius: 8px; border: 1px solid #2D333F; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #F3EFE5; line-height: 1.8;">
                [User Query / SMILES]<br>
                &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
                [Streamlit Interface & RDKit Validator]<br>
                &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
                [LangChain Reasoning Agent]<br>
                &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
                [AROMMA Inference Model & LoRA Embedder]<br>
                &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
                [152 Multilabel Sensory Descriptors]<br>
                &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
                [Natural Olfactory Profile & 2D Topologies]
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background: rgba(199, 165, 107, 0.08); border: 1px solid rgba(199, 165, 107, 0.3); border-radius: 10px; padding: 1.2rem;">
        <div style="font-size: 0.85rem; color: #C7A56B; font-weight: 600; margin-bottom: 0.3rem;">Scientific & Safety Notice</div>
        <div style="font-size: 0.82rem; color: #A5A9B0; line-height: 1.6;">
            Descriptors generated by AROMMA are computational model predictions derived from molecular representations and statistical alignments. They represent predicted organoleptic characteristics and do not constitute clinical sensory testing, toxicological screening, or safety determinations for human consumption or topical application.
        </div>
    </div>
    """, unsafe_allow_html=True)
