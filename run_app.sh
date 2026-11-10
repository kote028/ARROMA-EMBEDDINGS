#!/usr/bin/env bash
# ==============================================================================
# AROMMA SCENTLAB LAUNCHER
# AI-Powered Molecular Fragrance Intelligence
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Locate conda / miniforge
if [ -f "/home/kote/miniforge3/etc/profile.d/conda.sh" ]; then
    source "/home/kote/miniforge3/etc/profile.d/conda.sh"
elif command -v conda &> /dev/null; then
    source "$(conda info --base)/etc/profile.d/conda.sh"
fi

echo "🧪 Activating aromma_agent_env..."
conda activate aromma_agent_env

# Check Ollama service
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️ Ollama daemon not running. Starting in background..."
    ollama serve &
    sleep 3
fi

echo "🚀 Launching AROMMA ScentLab on http://localhost:8501 ..."
python -m streamlit run app.py --server.port 8501
