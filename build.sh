#!/usr/bin/env bash
# Build script for Render — builds frontend then installs backend deps

set -e  # Exit on error

echo ">>> Installing frontend dependencies..."
cd frontend
npm install

echo ">>> Building frontend..."
npm run build

echo ">>> Installing backend dependencies..."
cd ../backend
pip install -r requirements.txt

echo ">>> Build complete!"
