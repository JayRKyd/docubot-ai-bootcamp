"""
Configuration for multi-source documentation ingestion
Customize these settings for your SaaS demo
"""

# ReadTheDocs sources
READTHEDOCS_SOURCES = [
    {
        'name': 'FastAPI',
        'url': 'https://fastapi.tiangolo.com',
        'max_pages': 30
    },
    # Add more ReadTheDocs sites here
    # {
    #     'name': 'Django',
    #     'url': 'https://docs.djangoproject.com/en/stable/',
    #     'max_pages': 50
    # },
]

# GitHub repositories
GITHUB_SOURCES = [
    {
        'name': 'FastAPI',
        'owner': 'tiangolo',
        'repo': 'fastapi',
        'token': None  # Add GitHub token for higher rate limits
    },
    # Add more repos here
    # {
    #     'name': 'Requests',
    #     'owner': 'psf',
    #     'repo': 'requests',
    #     'token': None
    # },
]

# Custom websites
WEBSITE_SOURCES = [
   {
        'name': 'Python Official Docs',
        'url': 'https://docs.python.org/3/tutorial/index.html',
        'allowed_domains': ['docs.python.org'],
        'max_pages': 10
    },
]

# Output settings
OUTPUT_FILE = 'documents.json'