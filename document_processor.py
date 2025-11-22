# document_processor.py
import os
import glob
import requests
from bs4 import BeautifulSoup
from langchain.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredHTMLLoader,
    WebBaseLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from urllib.parse import urljoin, urlparse
import time
import re

class WazuhDocumentProcessor:
    def __init__(self, docs_folder="./wazuh_docs"):
        self.docs_folder = docs_folder
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        
        # Wazuh documentation URLs from your file
        self.wazuh_urls = self.load_wazuh_urls()
    
    def load_wazuh_urls(self):
        """Load all Wazuh URLs from the provided list"""
        urls = [
            # Getting started
            "https://documentation.wazuh.com/current/quickstart.html",
            "https://documentation.wazuh.com/current/getting-started/index.html",
            "https://documentation.wazuh.com/current/getting-started/components.html",
            "https://documentation.wazuh.com/current/getting-started/architecture.html",
            "https://documentation.wazuh.com/current/getting-started/use-cases.html",
            
            # Installation guide
            "https://documentation.wazuh.com/current/installation-guide/wazuh-indexer/index.html",
            "https://documentation.wazuh.com/current/installation-guide/wazuh-server/index.html",
            "https://documentation.wazuh.com/current/installation-guide/wazuh-dashboard/index.html",
            "https://documentation.wazuh.com/current/installation-guide/packages-list.html",
            "https://documentation.wazuh.com/current/installation-guide/uninstall.html",
            "https://documentation.wazuh.com/current/installation-guide/alternatives/index.html",
            
            # User manual
            "https://documentation.wazuh.com/current/user-manual/wazuh-server/index.html",
            "https://documentation.wazuh.com/current/user-manual/wazuh-indexer/index.html",
            "https://documentation.wazuh.com/current/user-manual/data-analysis/index.html",
            "https://documentation.wazuh.com/current/user-manual/user-administration/index.html",
            "https://documentation.wazuh.com/current/user-manual/capabilities/index.html",
            
            # Reference
            "https://documentation.wazuh.com/current/reference/ossec-conf/index.html",
            "https://documentation.wazuh.com/current/reference/daemons/index.html",
            "https://documentation.wazuh.com/current/reference/tools/index.html",
            "https://documentation.wazuh.com/current/reference/api/index.html",
            "https://documentation.wazuh.com/current/reference/unattended-installation.html",
            "https://documentation.wazuh.com/current/reference/statistics/index.html",
            
            # Cloud security
            "https://documentation.wazuh.com/current/cloud-security/aws/index.html",
            "https://documentation.wazuh.com/current/cloud-security/azure/index.html",
            "https://documentation.wazuh.com/current/cloud-security/github/index.html",
            "https://documentation.wazuh.com/current/cloud-security/gcp/index.html",
            "https://documentation.wazuh.com/current/cloud-security/o365/index.html",
            
            # Regulatory compliance
            "https://documentation.wazuh.com/current/compliance/pci-dss/index.html",
            "https://documentation.wazuh.com/current/compliance/gdpr/index.html",
            "https://documentation.wazuh.com/current/compliance/hipaa/index.html",
            "https://documentation.wazuh.com/current/compliance/nist-800-53/index.html",
            "https://documentation.wazuh.com/current/compliance/tsc/index.html",
            
            # Proof of Concept guide
            "https://documentation.wazuh.com/current/proof-of-concept/block-malicious-actor.html",
            "https://documentation.wazuh.com/current/proof-of-concept/file-integrity-monitoring.html",
            "https://documentation.wazuh.com/current/proof-of-concept/brute-force-attack.html",
            "https://documentation.wazuh.com/current/proof-of-concept/docker-events.html",
            "https://documentation.wazuh.com/current/proof-of-concept/aws-infrastructure.html",
            "https://documentation.wazuh.com/current/proof-of-concept/unauthorized-processes.html",
            "https://documentation.wazuh.com/current/proof-of-concept/network-ids.html",
            "https://documentation.wazuh.com/current/proof-of-concept/sql-injection.html",
            "https://documentation.wazuh.com/current/proof-of-concept/suspicious-binaries.html",
            "https://documentation.wazuh.com/current/proof-of-concept/malware-virustotal.html",
            "https://documentation.wazuh.com/current/proof-of-concept/vulnerability-detection.html",
            "https://documentation.wazuh.com/current/proof-of-concept/malware-yara.html",
            "https://documentation.wazuh.com/current/proof-of-concept/hidden-processes.html",
            "https://documentation.wazuh.com/current/proof-of-concept/malicious-commands.html",
            "https://documentation.wazuh.com/current/proof-of-concept/shellshock.html",
            "https://documentation.wazuh.com/current/proof-of-concept/llm-alert-enrichment.html",
            
            # Upgrade guide
            "https://documentation.wazuh.com/current/upgrade-guide/wazuh-central-components.html",
            "https://documentation.wazuh.com/current/upgrade-guide/wazuh-agent.html",
            "https://documentation.wazuh.com/current/upgrade-guide/troubleshooting.html",
            
            # Integrations guide
            "https://documentation.wazuh.com/current/integrations/elastic-stack.html",
            "https://documentation.wazuh.com/current/integrations/opensearch.html",
            "https://documentation.wazuh.com/current/integrations/splunk.html",
            "https://documentation.wazuh.com/current/integrations/security-lake.html",
            
            # Backup guide
            "https://documentation.wazuh.com/current/backup-guide/create-backup.html",
            "https://documentation.wazuh.com/current/backup-guide/restore-backup.html",
            
            # Wazuh Cloud service
            "https://documentation.wazuh.com/current/wazuh-cloud/getting-started.html",
            "https://documentation.wazuh.com/current/wazuh-cloud/environment.html",
            "https://documentation.wazuh.com/current/wazuh-cloud/ai-analyst.html",
            "https://documentation.wazuh.com/current/wazuh-cloud/account-billing.html",
            "https://documentation.wazuh.com/current/wazuh-cloud/archive-data.html",
            "https://documentation.wazuh.com/current/wazuh-cloud/api.html",
            "https://documentation.wazuh.com/current/wazuh-cloud/cli.html",
            
            # Glossary
            "https://documentation.wazuh.com/current/glossary.html",
            
            # Development
            "https://documentation.wazuh.com/current/development/client-keys.html",
            "https://documentation.wazuh.com/current/development/message-format.html",
            "https://documentation.wazuh.com/current/development/makefile-options.html",
            "https://documentation.wazuh.com/current/development/server-cluster.html",
            "https://documentation.wazuh.com/current/development/package-generation.html",
            "https://documentation.wazuh.com/current/development/virtual-machine.html",
            "https://documentation.wazuh.com/current/development/wazuh-server.html",
            "https://documentation.wazuh.com/current/development/wazuh-indexer.html",
            "https://documentation.wazuh.com/current/development/wazuh-dashboard.html",
            "https://documentation.wazuh.com/current/development/wazuh-agent.html",
            "https://documentation.wazuh.com/current/development/wazuh-logtest.html",
            "https://documentation.wazuh.com/current/development/rbac-integrity.html",
            "https://documentation.wazuh.com/current/development/core-dump.html",
            
            # Release notes
            "https://documentation.wazuh.com/current/release-notes/index.html"
        ]
        return urls
    
    def download_wazuh_documentation(self):
        """Download all Wazuh documentation from the provided URLs"""
        print("🚀 Starting Wazuh documentation download...")
        print(f"📁 Saving to: {self.docs_folder}")
        
        os.makedirs(self.docs_folder, exist_ok=True)
        
        successful_downloads = 0
        failed_downloads = []
        
        for url in self.wazuh_urls:
            try:
                print(f"📥 Downloading: {url}")
                
                # Use WebBaseLoader from LangChain
                loader = WebBaseLoader(url)
                documents = loader.load()
                
                if documents and documents[0].page_content.strip():
                    # Create filename from URL
                    parsed_url = urlparse(url)
                    path = parsed_url.path.strip('/')
                    if not path:
                        path = "index"
                    
                    # Clean filename
                    filename = re.sub(r'[^\w\-_.]', '_', path) + ".txt"
                    filepath = os.path.join(self.docs_folder, filename)
                    
                    # Save content
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(f"SOURCE: {url}\n")
                        f.write("=" * 80 + "\n")
                        f.write(documents[0].page_content)
                    
                    successful_downloads += 1
                    print(f"✅ Saved: {filename}")
                
                # Be polite to the server
                time.sleep(1)
                
            except Exception as e:
                error_msg = f"Failed to download {url}: {str(e)}"
                print(f"❌ {error_msg}")
                failed_downloads.append(error_msg)
                continue
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 DOWNLOAD SUMMARY")
        print("=" * 60)
        print(f"✅ Successful downloads: {successful_downloads}/{len(self.wazuh_urls)}")
        if failed_downloads:
            print(f"❌ Failed downloads: {len(failed_downloads)}")
            for failure in failed_downloads:
                print(f"   - {failure}")
        
        return successful_downloads > 0
    
    def load_documents(self):
        """Load all downloaded Wazuh documents"""
        all_documents = []
        
        # Load text files
        text_files = glob.glob(os.path.join(self.docs_folder, "**/*.txt"), recursive=True)
        text_files.extend(glob.glob(os.path.join(self.docs_folder, "**/*.html"), recursive=True))
        
        for text_file in text_files:
            try:
                loader = TextLoader(text_file, encoding='utf-8')
                documents = loader.load()
                all_documents.extend(documents)
                print(f"📖 Loaded: {os.path.basename(text_file)}")
            except Exception as e:
                print(f"❌ Error loading {text_file}: {e}")
        
        print(f"📚 Total documents loaded: {len(all_documents)}")
        return all_documents
    
    def chunk_documents(self, documents):
        """Split documents into manageable chunks"""
        print("✂️  Splitting documents into chunks...")
        chunks = self.text_splitter.split_documents(documents)
        print(f"📄 Created {len(chunks)} document chunks")
        return chunks

if __name__ == "__main__":
    processor = WazuhDocumentProcessor()
    
    # Download documentation
    success = processor.download_wazuh_documentation()
    
    if success:
        # Load and process documents
        documents = processor.load_documents()
        chunks = processor.chunk_documents(documents)
        
        print(f"🎉 Successfully processed {len(documents)} documents into {len(chunks)} chunks")
    else:
        print("❌ Documentation download failed. Please check your internet connection.")
