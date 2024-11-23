import os
import argparse
from typing import Dict, List
from utils.string_parser import StringParser
from utils.text_analyzer import TextAnalyzer
from utils.report_generator import ReportGenerator

class LocalizationTester:
    def __init__(self):
        self.project_path = "/Users/giovanni/GV/Projects/Localization-Manager-QA/testLocalizations"
        self.strings_file = os.path.join(self.project_path, "Localizable.xcstrings")
        self.string_parser = StringParser()
        self.text_analyzer = TextAnalyzer()
        self.issues = {}
        self.stats = {
            "total_strings": 0,
            "languages": [],
            "missing_translations": 0,
            "issues_found": 0
        }

    def analyze_project(self) -> None:
        """Run all localization tests on the project."""
        if not os.path.isfile(self.strings_file):
            print(f"No .xcstrings file found at {self.strings_file}!")
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
    parser.add_argument('--report', choices=['console', 'markdown', 'json'],
                        default='console', help='Report format')
    args = parser.parse_args()

    tester = LocalizationTester()
    tester.analyze_project()
    print(tester.generate_report(args.report))

if __name__ == '__main__':
    main()