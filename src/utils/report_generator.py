import json
import markdown
from datetime import datetime
from typing import Dict, List

class ReportGenerator:
    def __init__(self, issues: Dict[str, List[str]], stats: Dict[str, any]):
        self.issues = issues
        self.stats = stats
        self.timestamp = datetime.now()

    def generate_console_report(self) -> str:
        """Generate a console-friendly report."""
        report = [f"=== Localization Test Report ({self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}) ===\n"]
        
        # Add statistics
        report.append("Statistics:")
        for key, value in self.stats.items():
            report.append(f"  {key}: {value}")
        report.append("")

        # Add issues
        for category, category_issues in self.issues.items():
            if category_issues:
                report.append(f"\n{category.replace('_', ' ').title()}:")
                for issue in category_issues:
                    report.append(f"  ⚠️  {issue}")
        
        return "\n".join(report)

    def generate_markdown_report(self) -> str:
        """Generate a detailed markdown report."""
        report = [
            "# Localization QA Report",
            f"Generated: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n",
            "## Summary",
        ]

        # Add statistics
        for key, value in self.stats.items():
            report.append(f"- **{key}**: {value}")
        
        # Add issues
        report.append("\n## Issues by Category\n")
        for category, category_issues in self.issues.items():
            if category_issues:
                report.append(f"### {category.replace('_', ' ').title()}")
                for issue in category_issues:
                    report.append(f"- ⚠️  {issue}")
                report.append("")

        return "\n".join(report)

    def generate_json_report(self) -> str:
        """Generate a JSON report."""
        report_data = {
            "timestamp": self.timestamp.isoformat(),
            "stats": self.stats,
            "issues": self.issues
        }
        return json.dumps(report_data, indent=2)
