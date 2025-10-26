"""
Multi-Source Documentation Ingester
Supports: ReadTheDocs, GitHub, and custom websites
For AI Bootcamp - RAG to Agents Project
"""

import requests
from bs4 import BeautifulSoup
import json
from typing import List, Dict, Any
from urllib.parse import urljoin, urlparse
import time
from dataclasses import dataclass, asdict
import re


@dataclass
class Document:
    """Standardized document structure"""
    source: str  # 'readthedocs', 'github', 'website'
    url: str
    title: str
    content: str
    metadata: Dict[str, Any]
    
    def to_dict(self):
        return asdict(self)


class ReadTheDocsIngester:
    """Ingest documentation from ReadTheDocs sites"""
    
    def __init__(self, base_url: str, max_pages: int = 50):
        self.base_url = base_url.rstrip('/')
        self.max_pages = max_pages
        self.visited_urls = set()
        
    def get_all_docs(self) -> List[Document]:
        """Scrape all documentation pages"""
        documents = []
        to_visit = [self.base_url]
        
        print(f"🔍 Scraping ReadTheDocs: {self.base_url}")
        
        while to_visit and len(documents) < self.max_pages:
            url = to_visit.pop(0)
            
            if url in self.visited_urls:
                continue
                
            self.visited_urls.add(url)
            
            try:
                doc = self._scrape_page(url)
                if doc:
                    documents.append(doc)
                    print(f"  ✓ Scraped: {doc.title[:50]}...")
                    
                    # Find more pages to visit
                    new_urls = self._find_doc_links(url)
                    to_visit.extend([u for u in new_urls if u not in self.visited_urls])
                    
                time.sleep(0.5)  # Be polite
                
            except Exception as e:
                print(f"  ✗ Error scraping {url}: {e}")
                
        print(f"✅ ReadTheDocs: Collected {len(documents)} documents\n")
        return documents
    
    def _scrape_page(self, url: str) -> Document:
        """Scrape a single documentation page"""
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove navigation, footer, and script elements
        for element in soup.find_all(['nav', 'footer', 'script', 'style', 'aside']):
            element.decompose()
        
        # Try to find main content area (common ReadTheDocs selectors)
        main_content = (
            soup.find('div', role='main') or
            soup.find('main') or
            soup.find('article') or
            soup.find('div', class_=re.compile('content|document|body'))
        )
        
        if not main_content:
            main_content = soup.body
        
        # Extract title
        title = (
            soup.find('h1').get_text(strip=True) if soup.find('h1') else
            soup.title.get_text(strip=True) if soup.title else
            url.split('/')[-1]
        )
        
        # Extract text content
        content = main_content.get_text(separator='\n', strip=True)
        
        # Clean up content
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        return Document(
            source='readthedocs',
            url=url,
            title=title,
            content=content,
            metadata={
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'content_length': len(content)
            }
        )
    
    def _find_doc_links(self, current_url: str) -> List[str]:
        """Find links to other documentation pages"""
        try:
            response = requests.get(current_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(current_url, href)
                
                # Only include links from the same domain
                if urlparse(full_url).netloc == urlparse(self.base_url).netloc:
                    # Exclude anchors and special pages
                    if '#' not in full_url and not any(x in full_url for x in ['search', 'genindex', '_static']):
                        links.append(full_url)
            
            return list(set(links))
        except:
            return []


class GitHubIngester:
    """Ingest documentation from GitHub repositories"""
    
    def __init__(self, repo_owner: str, repo_name: str, github_token: str = None):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.api_base = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        self.headers = {'Authorization': f'token {github_token}'} if github_token else {}
        
    def get_all_docs(self) -> List[Document]:
        """Get README and Wiki pages"""
        documents = []
        
        print(f"🔍 Scraping GitHub: {self.repo_owner}/{self.repo_name}")
        
        # Get README
        readme = self._get_readme()
        if readme:
            documents.append(readme)
            print(f"  ✓ Got README")
        
        # Get Wiki pages
        wiki_pages = self._get_wiki_pages()
        documents.extend(wiki_pages)
        if wiki_pages:
            print(f"  ✓ Got {len(wiki_pages)} Wiki pages")
        
        # Get docs/ directory if exists
        docs_files = self._get_docs_directory()
        documents.extend(docs_files)
        if docs_files:
            print(f"  ✓ Got {len(docs_files)} files from docs/")
        
        print(f"✅ GitHub: Collected {len(documents)} documents\n")
        return documents
    
    def _get_readme(self) -> Document:
        """Get repository README"""
        try:
            url = f"{self.api_base}/readme"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            content = requests.get(data['download_url']).text
            
            return Document(
                source='github',
                url=data['html_url'],
                title=f"{self.repo_name} - README",
                content=content,
                metadata={
                    'type': 'readme',
                    'repo': f"{self.repo_owner}/{self.repo_name}",
                    'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
                }
            )
        except Exception as e:
            print(f"  ✗ Error getting README: {e}")
            return None
    
    def _get_wiki_pages(self) -> List[Document]:
        """Get Wiki pages (requires wiki to be enabled)"""
        documents = []
        
        try:
            # GitHub Wiki is actually a separate git repo
            wiki_url = f"https://github.com/{self.repo_owner}/{self.repo_name}.wiki.git"
            # For simplicity, we'll skip wiki cloning in this version
            # In production, you'd use GitPython to clone and parse
            pass
        except Exception as e:
            print(f"  ℹ Wiki not available or error: {e}")
        
        return documents
    
    def _get_docs_directory(self, path: str = "docs") -> List[Document]:
        """Get markdown files from docs/ directory"""
        documents = []
        
        try:
            url = f"{self.api_base}/contents/{path}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 404:
                return documents
            
            response.raise_for_status()
            items = response.json()
            
            for item in items:
                if item['type'] == 'file' and item['name'].endswith(('.md', '.markdown', '.rst')):
                    content = requests.get(item['download_url']).text
                    
                    documents.append(Document(
                        source='github',
                        url=item['html_url'],
                        title=item['name'],
                        content=content,
                        metadata={
                            'type': 'docs_file',
                            'repo': f"{self.repo_owner}/{self.repo_name}",
                            'path': item['path'],
                            'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
                        }
                    ))
                elif item['type'] == 'dir':
                    # Recursively get subdirectories
                    documents.extend(self._get_docs_directory(item['path']))
            
        except Exception as e:
            print(f"  ℹ Docs directory not available: {e}")
        
        return documents


class WebsiteIngester:
    """Ingest documentation from custom websites"""
    
    def __init__(self, start_url: str, allowed_domains: List[str] = None, max_pages: int = 50):
        self.start_url = start_url
        self.allowed_domains = allowed_domains or [urlparse(start_url).netloc]
        self.max_pages = max_pages
        self.visited_urls = set()
        
    def get_all_docs(self) -> List[Document]:
        """Crawl and scrape website documentation"""
        documents = []
        to_visit = [self.start_url]
        
        print(f"🔍 Scraping Website: {self.start_url}")
        
        while to_visit and len(documents) < self.max_pages:
            url = to_visit.pop(0)
            
            if url in self.visited_urls:
                continue
            
            # Check if domain is allowed
            if urlparse(url).netloc not in self.allowed_domains:
                continue
                
            self.visited_urls.add(url)
            
            try:
                doc = self._scrape_page(url)
                if doc:
                    documents.append(doc)
                    print(f"  ✓ Scraped: {doc.title[:50]}...")
                    
                    # Find more pages
                    new_urls = self._find_links(url)
                    to_visit.extend([u for u in new_urls if u not in self.visited_urls])
                    
                time.sleep(0.5)
                
            except Exception as e:
                print(f"  ✗ Error scraping {url}: {e}")
        
        print(f"✅ Website: Collected {len(documents)} documents\n")
        return documents
    
    def _scrape_page(self, url: str) -> Document:
        """Scrape a single page"""
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove unwanted elements
        for element in soup.find_all(['nav', 'footer', 'script', 'style', 'aside', 'header']):
            element.decompose()
        
        # Try to find main content
        main_content = (
            soup.find('main') or
            soup.find('article') or
            soup.find('div', class_=re.compile('content|main|article|body'))
        )
        
        if not main_content:
            main_content = soup.body
        
        # Extract title
        title = (
            soup.find('h1').get_text(strip=True) if soup.find('h1') else
            soup.title.get_text(strip=True) if soup.title else
            url.split('/')[-1]
        )
        
        # Extract content
        content = main_content.get_text(separator='\n', strip=True) if main_content else ''
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        return Document(
            source='website',
            url=url,
            title=title,
            content=content,
            metadata={
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'content_length': len(content)
            }
        )
    
    def _find_links(self, current_url: str) -> List[str]:
        """Find links on the page"""
        try:
            response = requests.get(current_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(current_url, href)
                
                # Only include allowed domains
                if urlparse(full_url).netloc in self.allowed_domains:
                    if '#' not in full_url:
                        links.append(full_url)
            
            return list(set(links))
        except:
            return []


def save_documents(documents: List[Document], output_file: str = 'documents.json'):
    """Save documents to JSON file"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump([doc.to_dict() for doc in documents], f, indent=2, ensure_ascii=False)
    print(f"💾 Saved {len(documents)} documents to {output_file}")


def main():
    """Main ingestion pipeline"""
    all_documents = []
    
    print("=" * 60)
    print("Multi-Source Documentation Ingester")
    print("=" * 60 + "\n")
    
    # Example 1: ReadTheDocs - FastAPI
    rtd_ingester = ReadTheDocsIngester(
        base_url='https://fastapi.tiangolo.com',
        max_pages=30
    )
    rtd_docs = rtd_ingester.get_all_docs()
    all_documents.extend(rtd_docs)
    
    # Example 2: GitHub - FastAPI repo
    github_ingester = GitHubIngester(
        repo_owner='tiangolo',
        repo_name='fastapi',
        github_token=None  # Add your token here for higher rate limits
    )
    github_docs = github_ingester.get_all_docs()
    all_documents.extend(github_docs)
    
    # Example 3: Custom website (if needed)
    website_ingester = WebsiteIngester(
        start_url='https://docs.python.org/3/tutorial/index.html',
        allowed_domains=['docs.python.org'],
        max_pages=10
    )
    website_docs = website_ingester.get_all_docs()
    all_documents.extend(website_docs)

    # Save all documents
    print("\n" + "=" * 60)
    print(f"📊 Total documents collected: {len(all_documents)}")
    print(f"   - ReadTheDocs: {len(rtd_docs)}")
    print(f"   - GitHub: {len(github_docs)}")
    print(f"   - Custom Website: {len(website_docs)}")
    print("=" * 60 + "\n")
    
    save_documents(all_documents, 'documents.json')
    
    # Print sample document
    if all_documents:
        print("\n📄 Sample document:")
        print(f"Title: {all_documents[0].title}")
        print(f"Source: {all_documents[0].source}")
        print(f"URL: {all_documents[0].url}")
        print(f"Content preview: {all_documents[0].content[:200]}...")
        print(f"   - Custom Website: {len(website_docs)}")


if __name__ == '__main__':
    main()