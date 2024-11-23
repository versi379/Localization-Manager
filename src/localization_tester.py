import os
import argparse
from typing import Dict, List
from utils.string_parser import StringParser
from utils.text_analyzer import TextAnalyzer
from utils.report_generator import ReportGenerator

class LocalizationTester:
    def __init__(self, project_path: str):
        self.project_path = "/Users/giovanni/GV/Projects/Localization-Manager-QA/testLocalizations/Localizable.xcstrings"
        self.string_parser = StringParser()
        self.text_analyzer = TextAnalyzer()
        self.strings_file = None
        self.issues = {}
        self.stats = {
            "total_strings": 0,
            "languages": [],
            "missing_translations": 0,
            "issues_found": 0
        }

    def find_xcstrings_file(self) -> bool:
        """Find .xcstrings file in the project."""
        for root, _, files in os.walk(self.project_path):
            for file in files:
                if file.endswith('.xcstrings'):
                    self.strings_file = os.path.join(root, file)
                    return True
        return False

    def analyze_project(self) -> None:
        """Run all localization tests on the project."""
        if not self.find_xcstrings_file():
            print("No .xcstrings file found!")
            return

        # Parse strings file
        xcstrings_data = self.string_parser.parse_xcstrings_file(self.strings_file)
        if not xcstrings_data:
            print("Failed to parse .xcstrings file!")
            return

        # Extract translations
        translations, source_language = self.string_parser.extract_translations(xcstrings_data)

        # Update stats
        self.stats["total_strings"] = len(translations)
        self.stats["languages"] = list(set(
            lang for trans in translations.values() 
            for lang in trans.keys()
        ))

        # Analyze translations
        self.issues = self.text_analyzer.analyze_xcstrings(translations, source_language)
        
        # Update issue stats
        self.stats["issues_found"] = sum(len(issues) for issues in self.issues.values())
        self.stats["missing_translations"] = len(self.issues["missing_translations"])

    def generate_report(self, format: str = 'console') -> str:
        """Generate test report in specified format."""
        generator = ReportGenerator(self.issues, self.stats)
        
        if format == 'markdown':
            return generator.generate_markdown_report()
        elif format == 'json':
            return generator.generate_json_report()
        else:
            return generator.generate_console_report()

def main():
    parser = argparse.ArgumentParser(description='Test iOS/macOS app localizations')
    parser.add_argument('project_path', help='Path to your Xcode project')
    parser.add_argument('--report', choices=['console', 'markdown', 'json'], 
                       default='console', help='Report format')
    parser.add_argument('--watch', action='store_true', 
                       help='Watch for file changes')
    
    args = parser.parse_args()
    
    tester = LocalizationTester(args.project_path)
    tester.analyze_project()
    print(tester.generate_report(args.report))

if __name__ == '__main__':
    main()