#!/bin/bash
echo "🚀 Wazuh AI Specialist - Setup Script"
echo "======================================"

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

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install -r requirements.txt

# Install Playwright for web scraping
echo "🌐 Installing browser tools for documentation download..."
playwright install

echo "✅ Setup complete!"
echo ""
echo "🎯 To start your Wazuh AI Specialist:"
echo "   python main.py"
echo ""
echo "📚 On first run, it will download all Wazuh documentation."
echo "   This may take a few minutes depending on your internet speed."
