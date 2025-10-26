DocuBot - Multi-Source Documentation Ingester
AI Bootcamp Project: RAG to Agents
SaaS Vision: Intelligent documentation assistant for companies
🎯 Project Overview
This project ingests documentation from multiple sources to build an intelligent Q&A system. Perfect foundation for a SaaS product that helps companies search and understand their scattered documentation.
Supported Sources

✅ ReadTheDocs - Structured documentation sites
✅ GitHub - READMEs, docs/ folders, and wikis
✅ Custom Websites - Any documentation website

🚀 Quick Start
Installation
bash# Clone the repository
git clone https://github.com/YOUR_USERNAME/docubot-ai-bootcamp.git
cd docubot-ai-bootcamp

# Install dependencies
pip install -r requirements.txt
Run Data Ingestion
bashpython data_ingestion.py
This will:

Scrape FastAPI documentation from ReadTheDocs (~30 pages)
Get FastAPI README and docs from GitHub
Save everything to documents.json

Customize Sources
Edit config.py to add your own documentation sources:
pythonREADTHEDOCS_SOURCES = [
    {
        'name': 'Your Docs',
        'url': 'https://your-docs.readthedocs.io',
        'max_pages': 50
    }
]

GITHUB_SOURCES = [
    {
        'name': 'Your Repo',
        'owner': 'your-github',
        'repo': 'your-repo',
        'token': 'ghp_your_token_here'  # Optional, for higher rate limits
    }
]
📊 Output Format
Documents are saved in JSON format:
json[
  {
    "source": "readthedocs",
    "url": "https://fastapi.tiangolo.com/tutorial/",
    "title": "Tutorial - User Guide",
    "content": "Full text content...",
    "metadata": {
      "scraped_at": "2025-10-25 10:30:00",
      "content_length": 15420
    }
  }
]