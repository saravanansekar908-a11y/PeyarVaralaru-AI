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
  npm install
  npm run build
  cd ../backend
fi

echo "==> Build completed successfully!"
