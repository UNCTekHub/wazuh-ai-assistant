#!/bin/bash
echo "🚀 Wazuh AI Specialist - Fixed Setup Script"
echo "============================================"

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed. Please install it from https://ollama.ai/"
    exit 1
fi

# Check if Ollama is running
if ! ollama list &> /dev/null; then
    echo "⚠️  Starting Ollama service..."
    ollama serve &
    sleep 5
fi

# Pull the AI model
echo "📥 Downloading AI model (llama3)..."
ollama pull llama3

# Check for Python and pip
echo "🐍 Checking Python environment..."

# Try different Python/pip commands
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
    echo "✅ Using pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
    echo "✅ Using pip"
else
    echo "❌ pip not found. Installing pip..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
    PIP_CMD="pip3"
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
$PIP_CMD install -r requirements.txt

# Install Playwright if pip succeeded
if command -v playwright &> /dev/null; then
    echo "✅ Playwright already installed"
else
    echo "🌐 Installing browser tools for documentation download..."
    $PIP_CMD install playwright
    python3 -m playwright install
fi

echo "✅ Setup complete!"
echo ""
echo "🎯 To start your Wazuh AI Specialist:"
echo "   python3 main.py"
echo ""
echo "📚 On first run, it will download all Wazuh documentation."
echo "   This may take a few minutes depending on your internet speed."
