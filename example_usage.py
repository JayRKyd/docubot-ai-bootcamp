"""
Example Usage - Multi-Source Documentation Ingester

This shows different ways to use the ingestion system
"""

from data_ingestion import (
    ReadTheDocsIngester,
    GitHubIngester,
    WebsiteIngester,
    save_documents
)


def example_1_readthedocs_only():
    """Example: Ingest only from ReadTheDocs"""
    print("\n" + "="*60)
    print("EXAMPLE 1: ReadTheDocs Only")
    print("="*60)
    
    ingester = ReadTheDocsIngester(
        base_url='https://fastapi.tiangolo.com',
        max_pages=10  # Small number for quick demo
    )
    
    documents = ingester.get_all_docs()
    save_documents(documents, 'example1_rtd_only.json')
    
    return documents


def example_2_github_only():
    """Example: Ingest only from GitHub"""
    print("\n" + "="*60)
    print("EXAMPLE 2: GitHub Only")
    print("="*60)
    
    ingester = GitHubIngester(
        repo_owner='tiangolo',
        repo_name='fastapi'
    )
    
    documents = ingester.get_all_docs()
    save_documents(documents, 'example2_github_only.json')
    
    return documents


def example_3_multiple_sources():
    """Example: Ingest from multiple documentation sites"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Multiple Sources")
    print("="*60)
    
    all_docs = []
    
    # Source 1: FastAPI docs
    print("\n📚 Source 1: FastAPI Documentation")
    fastapi_ingester = ReadTheDocsIngester(
        base_url='https://fastapi.tiangolo.com',
        max_pages=10
    )
    all_docs.extend(fastapi_ingester.get_all_docs())
    
    # Source 2: Requests docs
    print("\n📚 Source 2: Requests Documentation")
    requests_ingester = ReadTheDocsIngester(
        base_url='https://requests.readthedocs.io',
        max_pages=10
    )
    all_docs.extend(requests_ingester.get_all_docs())
    
    # Source 3: FastAPI GitHub
    print("\n📚 Source 3: FastAPI GitHub")
    github_ingester = GitHubIngester(
        repo_owner='tiangolo',
        repo_name='fastapi'
    )
    all_docs.extend(github_ingester.get_all_docs())
    
    save_documents(all_docs, 'example3_multi_source.json')
    
    # Print summary
    print("\n" + "="*60)
    print("📊 Summary")
    print("="*60)
    print(f"Total documents: {len(all_docs)}")
    
    by_source = {}
    for doc in all_docs:
        by_source[doc.source] = by_source.get(doc.source, 0) + 1
    
    for source, count in by_source.items():
        print(f"  - {source}: {count} documents")
    
    return all_docs


def example_4_custom_website():
    """Example: Ingest from a custom website"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Custom Website")
    print("="*60)
    
    # Example: Python.org documentation
    ingester = WebsiteIngester(
        start_url='https://docs.python.org/3/tutorial/',
        allowed_domains=['docs.python.org'],
        max_pages=10
    )
    
    documents = ingester.get_all_docs()
    save_documents(documents, 'example4_custom_website.json')
    
    return documents


def main():
    """Run examples"""
    print("\n" + "="*60)
    print("Multi-Source Documentation Ingester - Examples")
    print("="*60)
    
    # Uncomment the example you want to run:
    
    # example_1_readthedocs_only()
    # example_2_github_only()
    example_3_multiple_sources()  # Recommended for SaaS demo
    # example_4_custom_website()
    
    print("\n✅ Done! Check the generated JSON files.")


if __name__ == '__main__':
    main()