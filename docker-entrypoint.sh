#!/bin/bash
cd /app/toposoid-language-detector-web
source /root/.local/bin/env
uv run uvicorn api:app --reload --host 0.0.0.0 --port 9017
