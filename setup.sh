#!/bin/bash
# Setup script for Name Pronunciation Analyser

echo "🚀 Setting up Name Pronunciation Analyser..."

# Setup backend
echo ""
echo "📦 Setting up backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file from template if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.template .env
    echo "⚠️  Please edit backend/.env and add your ANTHROPIC_API_KEY"
fi

cd ..

# Setup frontend
echo ""
echo "📦 Setting up frontend..."
cd frontend

# Install dependencies
echo "Installing Node dependencies..."
npm install

# Create .env file from template if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.template .env
fi

cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit backend/.env and add your Anthropic API key (for Phase 2)"
echo "2. Start the backend: ./start-backend.sh"
echo "3. Start the frontend: ./start-frontend.sh"
echo "4. Open http://localhost:3000 in your browser"
