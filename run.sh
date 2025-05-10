#!/bin/bash
source venv/bin/activate || true
python3 -m uvicorn main:app --host 0.0.0.0 --port 8080 --reload