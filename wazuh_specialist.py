# wazuh_specialist.py
import ollama
from vector_store import WazuhVectorStore
import json

class WazuhSpecialist:
    def __init__(self):
        self.vector_store = WazuhVectorStore()
        self.vector_store.load_vector_store()
        self.model = "llama3"  # or "mistral" or "codellama"
        
        # Enhanced system prompt for Wazuh expertise
        self.system_prompt = """You are a Senior Wazuh Specialist with extensive experience in:
- Wazuh architecture designs
- Wazuh deployment, configuration, and high availability setups
- Wazuh indexer, server, and dashboard management
- Security monitoring, alerting, and incident response
- Rule and decoder creation for custom use cases
- Performance tuning and troubleshooting complex issues
- Integration with Elastic Stack, OpenSearch, and Splunk
- Cloud security monitoring (AWS, Azure, GCP, Office 365)
- Regulatory compliance (PCI DSS, GDPR, HIPAA, NIST)
- Vulnerability detection and file integrity monitoring
- Agent management across diverse environments

You provide accurate, detailed, and practical advice based on the official Wazuh documentation. 
Always include specific configuration examples, command line instructions, and best practices.

CRITICAL: If the information is not found in the provided context, explicitly state that you cannot find it in the documentation and suggest checking the official Wazuh documentation or community forums."""

    def get_relevant_context(self, question):
        """Get relevant documentation for the question"""
        relevant_docs = self.vector_store.search_documents(question, k=5)
        context = "\n\n--- DOCUMENTATION EXCERPT ---\n".join([
            f"SOURCE: {doc.metadata.get('source', 'Unknown')}\nCONTENT:\n{doc.page_content}" 
            for doc in relevant_docs
        ])
        return context

    def ask_question(self, question):
        """Ask a question to the Wazuh specialist"""
        print(f"🔍 Searching Wazuh documentation for: '{question}'")
        
        # Get relevant context
        context = self.get_relevant_context(question)
        
        # Create the prompt with context
        prompt = f"""Based on the following Wazuh documentation context, please answer the user's question thoroughly and professionally.

DOCUMENTATION CONTEXT:
{context}

USER QUESTION: {question}

Please provide a comprehensive answer as a Wazuh specialist. Include:
1. Clear explanation of the concept or solution
2. Step-by-step instructions if applicable
3. Configuration examples or code snippets
4. Best practices and considerations
5. References to relevant Wazuh components

Wazuh Specialist Answer:"""
        
        try:
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                system=self.system_prompt,
                options={
                    'temperature': 0.2,  # Lower temperature for more factual responses
                    'top_k': 40,
                    'top_p': 0.9,
                    'num_ctx': 4096  # Larger context window
                }
            )
            
            return response['response']
        
        except Exception as e:
            return f"❌ Error communicating with AI model: {e}"

    def start_chat(self):
        """Start an interactive chat session"""
        print("=" * 70)
        print("🤖 Wazuh AI Specialist Assistant")
        print("💡 Expert on Wazuh deployment, configuration, and enterprise support")
        print("📚 Knowledge: Full Wazuh documentation + Best practices")
        print("=" * 70)
        print("Commands: 'quit' to exit, 'clear' to start over, 'sources' to show doc sources")
        print("=" * 70)
        
        while True:
            user_input = input("\n🎯 Your Wazuh Question: ").strip()
            
            if user_input.lower() == 'quit':
                print("👋 Thank you for using Wazuh AI Specialist!")
                break
            elif user_input.lower() == 'clear':
                print("🔄 Conversation context cleared.")
                continue
            elif user_input.lower() == 'sources':
                print("📖 Documentation sources: Official Wazuh documentation (all URLs provided)")
                continue
            elif not user_input:
                continue
            
            print("⏳ Researching Wazuh documentation...")
            answer = self.ask_question(user_input)
            
            print(f"\n💡 Wazuh Specialist Answer:")
            print("=" * 60)
            print(answer)
            print("=" * 60)

if __name__ == "__main__":
    specialist = WazuhSpecialist()
    specialist.start_chat()
