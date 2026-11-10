import streamlit as st
from typing import Dict, Any, List
from components.molecule import smiles_to_svg

def render_tag_cloud(tags: List[str], tag_class: str = "scent-tag"):
    """Render an array of tags with custom styling."""
    if not tags:
        st.markdown("<span style='color: #A5A9B0; font-size: 0.85rem;'>None detected</span>", unsafe_allow_html=True)
        return
        
    html = f"<div class='tag-container'>"
    for t in tags:
        label = t.replace('_', ' ')
        html += f"<span class='{tag_class}'>{label}</span>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

def display_single_result(result: Dict[str, Any]):
    """Render single-molecule prediction card."""
    if not result.get("success"):
        st.error(f"⚠️ {result.get('error', 'Prediction failed.')}")
        return

    duration = result.get("duration", 0.0)
    descriptors = result.get("descriptors", [])
    natural_desc = result.get("natural_description", "")
    input_smiles = result.get("input_smiles", "")
    canonical_smiles = result.get("canonical_smiles", "")

    st.markdown(f"""
    <div class="result-container">
        <div class="result-header">
            <span class="result-title">Molecular Olfactory Profile</span>
            <span class="result-meta">Inference: {duration:.3f}s | Status: Active</span>
        </div>
        <div style="font-size: 0.95rem; line-height: 1.6; color: #F3EFE5; margin-bottom: 1rem;">
            {natural_desc}
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("<div style='font-size: 0.82rem; color: #C7A56B; text-transform: uppercase; font-weight: 600; margin-bottom: 0.3rem;'>Predicted Odor Descriptors</div>", unsafe_allow_html=True)
        render_tag_cloud(descriptors, "scent-tag")
        
        st.markdown("<div style='margin-top: 1rem;'>", unsafe_allow_html=True)
        st.markdown("<span style='font-size: 0.78rem; color: #A5A9B0;'>INPUT SMILES</span>", unsafe_allow_html=True)
        st.markdown(f"<div class='smiles-box'>{input_smiles}</div>", unsafe_allow_html=True)
        
        if canonical_smiles and canonical_smiles != input_smiles:
            st.markdown("<span style='font-size: 0.78rem; color: #A5A9B0; margin-top: 0.5rem; display: block;'>CANONICAL SMILES</span>", unsafe_allow_html=True)
            st.markdown(f"<div class='smiles-box'>{canonical_smiles}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div style='font-size: 0.82rem; color: #C7A56B; text-transform: uppercase; font-weight: 600; margin-bottom: 0.3rem;'>2D Molecular Topology</div>", unsafe_allow_html=True)
        svg = smiles_to_svg(canonical_smiles or input_smiles)
        if svg:
            st.markdown(f"<div style='background: #15181F; padding: 1rem; border-radius: 8px; border: 1px solid #2D333F; display: flex; justify-content: center;'>{svg}</div>", unsafe_allow_html=True)
        else:
            st.info("2D topology rendering unavailable.")

    st.markdown("</div>", unsafe_allow_html=True)

def display_mixture_result(result: Dict[str, Any]):
    """Render binary-mixture prediction card."""
    if not result.get("success"):
        st.error(f"⚠️ {result.get('error', 'Mixture analysis failed.')}")
        return

    duration = result.get("duration", 0.0)
    descriptors = result.get("descriptors", [])
    natural_desc = result.get("natural_description", "")
    smi_a = result.get("smiles_a", "")
    smi_b = result.get("smiles_b", "")
    canon_a = result.get("canonical_a", "")
    canon_b = result.get("canonical_b", "")

    st.markdown(f"""
    <div class="result-container">
        <div class="result-header">
            <span class="result-title">Binary Mixture Harmonization</span>
            <span class="result-meta">Inference: {duration:.3f}s | Blend: 2 Components</span>
        </div>
        <div style="font-size: 0.95rem; line-height: 1.6; color: #F3EFE5; margin-bottom: 1.2rem;">
            {natural_desc}
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size: 0.82rem; color: #C7A56B; text-transform: uppercase; font-weight: 600; margin-bottom: 0.3rem;'>Combined Odor Signature</div>", unsafe_allow_html=True)
    render_tag_cloud(descriptors, "scent-tag")

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div style='background: #15181F; padding: 1rem; border-radius: 8px; border: 1px solid #2D333F;'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size: 0.8rem; color: #C7A56B; font-weight: 600;'>COMPONENT A</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='smiles-box' style='margin: 0.4rem 0;'>{smi_a}</div>", unsafe_allow_html=True)
        svg_a = smiles_to_svg(canon_a or smi_a, width=280, height=140)
        if svg_a:
            st.markdown(f"<div style='display:flex; justify-content:center;'>{svg_a}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div style='background: #15181F; padding: 1rem; border-radius: 8px; border: 1px solid #2D333F;'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size: 0.8rem; color: #C7A56B; font-weight: 600;'>COMPONENT B</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='smiles-box' style='margin: 0.4rem 0;'>{smi_b}</div>", unsafe_allow_html=True)
        svg_b = smiles_to_svg(canon_b or smi_b, width=280, height=140)
        if svg_b:
            st.markdown(f"<div style='display:flex; justify-content:center;'>{svg_b}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

def display_recommendation_result(result: Dict[str, Any]):
    """Render recommended molecular ingredients card."""
    if not result.get("success"):
        st.error(f"⚠️ {result.get('error', 'Recommendation failed.')}")
        return

    concept = result.get("concept", "")
    duration = result.get("duration", 0.0)
    selected_descriptors = result.get("selected_descriptors", [])
    ingredients = result.get("ingredients", [])

    st.markdown(f"""
    <div class="result-container">
        <div class="result-header">
            <span class="result-title">Formulation Architecture</span>
            <span class="result-meta">Exploration: {duration:.2f}s | Match Count: {len(ingredients)}</span>
        </div>
        <div style="font-size: 0.95rem; color: #A5A9B0; margin-bottom: 1rem;">
            Target Concept: <em style="color: #F3EFE5;">"{concept}"</em>
        </div>
    """, unsafe_allow_html=True)

    if selected_descriptors:
        st.markdown("<div style='font-size: 0.82rem; color: #C7A56B; text-transform: uppercase; font-weight: 600; margin-bottom: 0.3rem;'>Selected Target Descriptors</div>", unsafe_allow_html=True)
        render_tag_cloud(selected_descriptors, "scent-tag")

    st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 0.95rem; font-family: Cinzel, serif; color: #F3EFE5; font-weight: 600; margin-bottom: 0.8rem;'>Recommended Molecular Candidates</div>", unsafe_allow_html=True)

    if not ingredients:
        st.info("No candidates directly matched the selected descriptor profile in the olfactory registry.")
    else:
        for idx, ing in enumerate(ingredients, 1):
            st.markdown(f"""
            <div style="background: #15181F; border: 1px solid #2D333F; border-radius: 10px; padding: 1.2rem; margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;">
                    <span style="font-family: 'Cinzel', serif; font-size: 0.95rem; color: #C7A56B; font-weight: 600;">Candidate {idx:02d}</span>
                    <span style="font-size: 0.78rem; color: #4ADE80; background: rgba(74, 222, 128, 0.1); padding: 0.2rem 0.6rem; border-radius: 9999px;">{ing['match_count']} Targeted Note Matches</span>
                </div>
                <div style="margin-bottom: 0.8rem;">
                    <span style="font-size: 0.75rem; color: #A5A9B0; display: block; margin-bottom: 0.2rem;">SMILES NOTATION</span>
                    <div class="smiles-box">{ing['smiles']}</div>
                </div>
            """, unsafe_allow_html=True)

            col_a, col_b = st.columns([1.2, 1])
            with col_a:
                st.markdown("<div style='font-size: 0.75rem; color: #A5A9B0; margin-bottom: 0.2rem;'>ALL ASSOCIATED DESCRIPTORS</div>", unsafe_allow_html=True)
                render_tag_cloud(ing.get("all_descriptors", []), "scent-tag")
                
                st.markdown("<div style='font-size: 0.75rem; color: #4ADE80; margin-top: 0.6rem; margin-bottom: 0.2rem;'>DIRECT TARGET MATCHES</div>", unsafe_allow_html=True)
                render_tag_cloud(ing.get("matched_descriptors", []), "match-tag")

            with col_b:
                svg = smiles_to_svg(ing['smiles'], width=240, height=110)
                if svg:
                    st.markdown(f"<div style='display:flex; justify-content:center;'>{svg}</div>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
