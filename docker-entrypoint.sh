#!/bin/bash
cd /app/toposoid-language-detector-web
uvicorn api:app --reload --host 0.0.0.0 --port 9017
