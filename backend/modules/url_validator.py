"""URL validation for GitHub repository URLs."""

import re
from urllib.parse import urlparse


class URLValidator:
    """Validates GitHub repository URLs."""
    
    GITHUB_PATTERNS = [
        r'^https?://github\.com/[\w\-]+/[\w\-\.]+/?$',
        r'^git@github\.com:[\w\-]+/[\w\-\.]+\.git$',
    ]
    
    @staticmethod
    def is_valid_github_url(url: str) -> bool:
        """
        Validate if the URL is a valid GitHub repository URL.
        
        Args:
            url: The URL to validate
            
        Returns:
            True if valid GitHub URL, False otherwise
        """
        if not url or not isinstance(url, str):
            return False
        
        url = url.strip()
        
        # Check against patterns
        for pattern in URLValidator.GITHUB_PATTERNS:
            if re.match(pattern, url):
                return True
        
        # Also accept URLs with .git suffix
        if url.endswith('.git'):
            url_without_git = url[:-4]
            for pattern in URLValidator.GITHUB_PATTERNS:
                if re.match(pattern, url_without_git):
                    return True
        
        return False
    
    @staticmethod
    def normalize_url(url: str) -> str:
        """
        Normalize GitHub URL to HTTPS format.
        
        Args:
            url: The URL to normalize
            
        Returns:
            Normalized HTTPS URL
        """
        url = url.strip()
        
        # Convert SSH to HTTPS
        if url.startswith('git@github.com:'):
            url = url.replace('git@github.com:', 'https://github.com/')
        
        # Remove .git suffix if present
        if url.endswith('.git'):
            url = url[:-4]
        
        # Remove trailing slash
        url = url.rstrip('/')
        
        return url
