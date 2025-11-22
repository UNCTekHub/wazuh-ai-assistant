# main.py
from wazuh_specialist import WazuhSpecialist
from vector_store import WazuhVectorStore
import sys

def setup_application():
    """Setup the application - run this first time"""
    print("🚀 Setting up Wazuh AI Specialist...")
    print("This will download all Wazuh documentation and create a knowledge base.")
    
    # Create vector store
    vector_store = WazuhVectorStore()
    if not vector_store.load_vector_store():
        print("🆕 Creating knowledge base from Wazuh documentation...")
        try:
            chunk_count = vector_store.create_vector_store()
            print(f"✅ Knowledge base created with {chunk_count} document chunks!")
        except Exception as e:
            print(f"❌ Failed to create knowledge base: {e}")
            sys.exit(1)
    else:
        print("✅ Knowledge base already exists and loaded!")
    
    # Test the specialist
    specialist = WazuhSpecialist()
    return specialist

def main():
    print("🎯 Wazuh AI Specialist Application")
    print("==========================================")
    print("Enterprise-grade Wazuh deployment, configuration, and support")
    print("==========================================")
    
    try:
        specialist = setup_application()
        
        # Example questions to help users get started
        print("\n💡 Example questions you can ask:")
        print("  - 'How do I set up a high availability Wazuh cluster?'")
        print("  - 'What are the steps to install Wazuh indexer on Ubuntu?'")
        print("  - 'How to create custom rules for detecting brute force attacks?'")
        print("  - 'Best practices for Wazuh performance tuning?'")
        print("  - 'How to monitor AWS CloudTrail with Wazuh?'")
        print()
        
        # Start interactive chat
        specialist.start_chat()
        
    except KeyboardInterrupt:
        print("\n\n👋 Thank you for using Wazuh AI Specialist!")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        print("💡 Please make sure:")
        print("   - Ollama is running (run 'ollama serve')")
        print("   - You have internet connection for first-time setup")
        print("   - You have enough disk space for documentation")

if __name__ == "__main__":
    main()
