#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

echo "==> Step 1: Building Frontend Assets"
cd frontend
npm install --no-package-lock
npm run build
cd ..

echo "==> Step 2: Installing Backend Dependencies"
pip install -r requirements.txt
pip install -e .

echo "==> Build completed successfully!"
