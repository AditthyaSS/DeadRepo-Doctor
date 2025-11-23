"""Main repo fetcher module integrating all components."""

from typing import Dict
from .url_validator import URLValidator
from .repo_cloner import RepoCloner
from .storage_manager import StorageManager


class RepoFetcher:
    """Main class for fetching GitHub repositories."""
    
    def __init__(self):
        """Initialize the repo fetcher with required components."""
        self.validator = URLValidator()
        self.cloner = RepoCloner()
        self.storage = StorageManager()
    
    def fetch_repository(self, repo_url: str) -> Dict[str, str]:
        """
        Fetch a GitHub repository and return its local path.
        
        Args:
            repo_url: GitHub repository URL
            
        Returns:
            Dictionary containing the local_path
            
        Raises:
            ValueError: If URL is invalid
            Exception: If cloning fails
        """
        # Validate URL
        if not self.validator.is_valid_github_url(repo_url):
            raise ValueError(f"Invalid GitHub URL: {repo_url}")
        
        # Normalize URL
        normalized_url = self.validator.normalize_url(repo_url)
        
        # Create temporary directory
        temp_dir = self.storage.create_temp_directory()
        
        try:
            # Clone repository
            self.cloner.clone(normalized_url, temp_dir)
            
            return {
                "local_path": temp_dir
            }
        except Exception as e:
            # Cleanup on failure
            self.storage.cleanup_directory(temp_dir)
            raise e
