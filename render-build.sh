#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

echo "==> Step 1: Building Frontend Assets"
cd frontend
npm install
npm run build
cd ..

echo "==> Step 2: Installing Backend Dependencies"
cd backend
pip install -r requirements.txt
cd ..

echo "==> Build completed successfully!"
