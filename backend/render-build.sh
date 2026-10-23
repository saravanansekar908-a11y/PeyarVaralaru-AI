#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

echo "==> Step 1: Installing Backend Dependencies"
pip install -r requirements.txt
if [ -f "../setup.py" ]; then
  pip install -e ..
fi

# If frontend exists in parent directory, build frontend assets
if [ -d "../frontend" ]; then
  echo "==> Step 2: Building Frontend Assets (../frontend)"
  cd ../frontend
  if [ ! -f "dist/index.html" ]; then
    npm install --legacy-peer-deps
    npm run build
  else
    echo "Frontend dist already present. Attempting fresh build..."
    (npm install --legacy-peer-deps && npm run build) || echo "Build warning: continuing with existing dist assets"
  fi
  cd ../backend
fi

echo "==> Build completed successfully!"
