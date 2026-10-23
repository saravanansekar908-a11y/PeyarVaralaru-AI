#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

echo "==> Step 1: Building Frontend Assets"
if [ -d "frontend" ]; then
  cd frontend
  if [ ! -f "dist/index.html" ]; then
    npm install --legacy-peer-deps
    npm run build
  else
    echo "Frontend dist already present. Attempting fresh build..."
    (npm install --legacy-peer-deps && npm run build) || echo "Build warning: continuing with existing dist assets"
  fi
  cd ..
fi

echo "==> Step 2: Installing Backend Dependencies"
pip install -r requirements.txt
pip install -e .

echo "==> Build completed successfully!"
