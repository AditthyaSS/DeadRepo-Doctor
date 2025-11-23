"""Main dependency analyzer module integrating all components."""

from typing import Dict
from .dependency_scanner import DependencyScanner
from .version_checker import VersionChecker
from .report_builder import ReportBuilder


class DependencyAnalyzer:
    """Main class for analyzing repository dependencies."""
    
    def __init__(self):
        """Initialize the dependency analyzer."""
        self.version_checker = VersionChecker()
        self.report_builder = ReportBuilder()
    
    def analyze(self, local_path: str) -> Dict:
        """
        Analyze dependencies in a local repository.
        
        Args:
            local_path: Path to the cloned repository
            
        Returns:
            Structured analysis report
            
        Raises:
            ValueError: If path is invalid
            Exception: If analysis fails
        """
        # Initialize scanner with the repo path
        scanner = DependencyScanner(local_path)
        
        # Scan for dependency files and extract packages
        scan_results = scanner.scan()
        
        if not scan_results.get("dependencies"):
            return self.report_builder.build_report(scan_results, [])
        
        # Check versions for all found packages
        version_results = self.version_checker.check_multiple_packages(
            scan_results["dependencies"]
        )
        
        # Build comprehensive report
        report = self.report_builder.build_report(scan_results, version_results)
        
        return report
