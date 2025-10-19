from fastapi import FastAPI

def get_app_config() -> dict:
    return {
        "title": "ContextIQ",
        "description": "ContextIQ - Knowledge Q&A System",
        "version": "1.0.0",
        "openapi_url": "/api/v1/openapi.json",
        "docs_url": "/api/v1/docs",
        "redoc_url": "/api/v1/redoc",
        "contact": {
            "name": "ContextIQ",
            "url": "https://s-nishad.github.io",
            "email": "shohanurnishad@gmail.com"
        },
        "license_info": {
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
        }
    }
