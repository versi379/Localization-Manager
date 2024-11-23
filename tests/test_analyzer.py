import unittest
from src.utils.text_analyzer import TextAnalyzer
from src.utils.swift_bridge import SwiftBridge

class TestTextAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = TextAnalyzer()
        self.sample_translations = {
            "welcome_message": {
                "en": {"value": "Welcome", "state": "translated"},
                "fr": {"value": "Bienvenue", "state": "translated"},
                "ar": {"value": "مرحبا", "state": "translated"}
            },
            "error_message": {
                "en": {"value": "Error: %@", "state": "translated"},
                "fr": {"value": "Erreur: %d", "state": "translated"}
            }
        }

    def test_analyze_xcstrings(self):
        issues = self.analyzer.analyze_xcstrings(self.sample_translations, "en")
        
        # Check for format specifier mismatch
        self.assertTrue(any(
            "format specifier" in issue.lower() 
            for issue in issues['format_issues']
        ))
        
        # Check for RTL considerations
        self.assertTrue(any(
            "rtl" in issue.lower() 
            for issue in issues['rtl_issues']
        ))

    def test_analyze_translation(self):
        result = self.analyzer.analyze_translation(
            "Welcome", 
            "Bienvenue très longue traduction"
        )
        
        self.assertIn('lengthRatio', result)
        self.assertTrue(result['lengthRatio'] > 1)

    def test_analyze_layout(self):
        result = self.analyzer.analyze_layout("ar", "مرحبا")
        
        self.assertTrue(result.get('isRTL', False))
        self.assertIn('textAnalysis', result)

if __name__ == '__main__':
    unittest.main()