#!/usr/bin/env bash
cd "$(dirname "$0")"
source .venv/bin/activate
exec streamlit run app.py
chmod +x start.sh
