#!/bin/bash
# Start the FastAPI backend server

echo "🚀 Starting Name Analyser Backend..."

cd backend

# Activate virtual environment
source venv/bin/activate

# Start FastAPI with uvicorn
cd api
python main.py
