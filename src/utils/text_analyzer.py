from typing import Dict, List
from .swift_bridge import SwiftBridge

class TextAnalyzer:
    def __init__(self):
        self.swift_helper = SwiftBridge()

    def analyze_translation(self, source_text: str, translated_text: str) -> Dict:
        """Analyze translation using Swift helper."""
        return self.swift_helper.validate_translation(source_text, translated_text)

    def analyze_layout(self, language: str, text: str) -> Dict:
        """Analyze layout considerations for a given language."""
        return self.swift_helper.check_layout(language, text)

    def analyze_xcstrings(self, translations: Dict, source_language: str) -> Dict:
        """Analyze all translations in an xcstrings file."""
        issues = {
            'missing_translations': [],
            'length_issues': [],
            'format_issues': [],
            'rtl_issues': [],
            'state_issues': []
        }

        for key, translations_data in translations.items():
            source_text = translations_data.get(source_language, {}).get('value', '')
            
            for lang, trans_data in translations_data.items():
                if lang == source_language:
                    continue

                translated_text = trans_data.get('value', '')
                if not translated_text:
                    issues['missing_translations'].append(f"Missing translation for '{key}' in {lang}")
                    continue

                # Analyze using Swift helper
                analysis = self.analyze_translation(source_text, translated_text)
                
                # Check length issues
                if analysis.get('lengthRatio', 1) > 1.5:
                    issues['length_issues'].append(
                        f"Text length issue in '{key}' for {lang}: "
                        f"ratio {analysis['lengthRatio']:.2f}"
                    )

                # Check format specifiers
                if not analysis.get('specifiersMatch', True):
                    issues['format_issues'].append(
                        f"Format specifier mismatch in '{key}' for {lang}"
                    )

                # Check RTL considerations
                if lang.startswith(('ar', 'he', 'fa')):
                    layout_analysis = self.analyze_layout(lang, translated_text)
                    if layout_analysis.get('isRTL'):
                        issues['rtl_issues'].append(
                            f"RTL considerations needed for '{key}' in {lang}"
                        )

        return issues