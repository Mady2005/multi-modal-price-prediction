"""
Configuration module for environment variable management.
Centralizes environment variable reading with fallback values.
"""
import os
from urllib.parse import urlparse


def get_api_url() -> str:
    """
    Get the API URL from environment variable or fallback to localhost.
    
    Returns:
        str: The API URL for the FastAPI backend
    """
    return os.getenv("API_URL", "http://127.0.0.1:8000/predict")


def get_database_url() -> str:
    """
    Get the database URL from environment variable or fallback to localhost.
    
    Returns:
        str: The PostgreSQL database connection string
    """
    return os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/pricing_data")


def validate_database_url(url: str) -> bool:
    """
    Validate that a database URL has the correct format.
    
    Args:
        url: The database connection string to validate
        
    Returns:
        bool: True if the URL is valid, False otherwise
    """
    try:
        parsed = urlparse(url)
        # Check that it has the required components
        if not parsed.scheme:
            return False
        if parsed.scheme not in ['postgresql', 'postgres']:
            return False
        if not parsed.netloc:
            return False
        return True
    except Exception:
        return False


def parse_database_url(url: str) -> dict:
    """
    Parse a database URL into its components.
    
    Args:
        url: The database connection string to parse
        
    Returns:
        dict: Dictionary with host, port, username, password, database
        
    Raises:
        ValueError: If the URL is invalid
    """
    if not validate_database_url(url):
        raise ValueError(f"Invalid database URL format: {url}")
    
    parsed = urlparse(url)
    
    return {
        'scheme': parsed.scheme,
        'username': parsed.username,
        'password': parsed.password,
        'host': parsed.hostname,
        'port': parsed.port or 5432,
        'database': parsed.path.lstrip('/') if parsed.path else None
    }
