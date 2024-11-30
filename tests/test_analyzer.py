import unittest
from unittest.mock import MagicMock
from src.utils.text_analyzer import TextAnalyzer

class TestTextAnalyzer(unittest.TestCase):
    def setUp(self):
        """Set up the TextAnalyzer instance and mock the SwiftBridge."""
        self.analyzer = TextAnalyzer()
        self.analyzer.swift_helper = MagicMock()

    def test_analyze_translation(self):
        """Test the analyze_translation method."""
        self.analyzer.swift_helper.validate_translation.return_value = {
            'lengthRatio': 1.0,
            'specifiersMatch': True
        }
        
        result = self.analyzer.analyze_translation("Hello %@", "Bonjour %@")
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result['lengthRatio'], 1.0)
        self.assertTrue(result['specifiersMatch'])

    def test_analyze_layout(self):
        """Test the analyze_layout method."""
        self.analyzer.swift_helper.check_layout.return_value = {
            'isRTL': False,
            'textAnalysis': {'length': 11, 'lines': 1}
        }
        
        result = self.analyzer.analyze_layout("en", "Hello World")
        
        self.assertIsInstance(result, dict)
        self.assertFalse(result['isRTL'])
        self.assertIn('textAnalysis', result)

    def test_analyze_xcstrings_missing_translation(self):
        """Test xcstrings analysis for missing translations."""
        translations = {
            "greeting": {
                "en": {"value": "Hello"},
                "fr": {"value": ""},
                "es": {"value": "Hola"}
            }
        }

        self.analyzer.swift_helper.validate_translation.return_value = {
            'lengthRatio': 1.0,
            'specifiersMatch': True
        }

        issues = self.analyze_xcstrings(translations, "en")
        
        self.assertIn("Missing translation for 'greeting' in fr", issues['missing_translations'])
        self.assertEqual(len(issues['length_issues']), 0)
        self.assertEqual(len(issues['format_issues']), 0)
        self.assertEqual(len(issues['rtl_issues']), 0)

    def test_analyze_xcstrings_length_issue(self):
        """Test xcstrings analysis for length issues."""
        translations = {
            "greeting": {
                "en": {"value": "Hello"},
                "fr": {"value": "Bonjour tout le monde"}
            }
        }

        self.analyzer.swift_helper.validate_translation.return_value = {
            'lengthRatio': 2.0,
            'specifiersMatch': True
        }

        issues = self.analyze_xcstrings(translations, "en")
        
        self.assertIn("Text length issue in 'greeting' for fr: ratio 2.00", issues['length_issues'])
        self.assertEqual(len(issues['missing_translations']), 0)
        self.assertEqual(len(issues['format_issues']), 0)
        self.assertEqual(len(issues['rtl_issues']), 0)

    def test_analyze_xcstrings_format_issue(self):
        """Test xcstrings analysis for format specifier mismatch."""
        translations = {
            "welcome_message": {
                "en": {"value": "Welcome %@ to %d"},
                "fr": {"value": "Bienvenue %d à %@"}
            }
        }

        self.analyzer.swift_helper.validate_translation.return_value = {
            'lengthRatio': 1.0,
            'specifiersMatch': False
        }

        issues = self.analyze_xcstrings(translations, "en")
        
        self.assertIn("Format specifier mismatch in 'welcome_message' for fr", issues['format_issues'])
        self.assertEqual(len(issues['missing_translations']), 0)
        self.assertEqual(len(issues['length_issues']), 0)
        self.assertEqual(len(issues['rtl_issues']), 0)

    def test_analyze_xcstrings_rtl_issue(self):
        """Test xcstrings analysis for RTL issues."""
        translations = {
            "welcome_message": {
                "en": {"value": "Welcome"},
                "ar": {"value": "مرحبا"}
            }
        }

        self.analyzer.swift_helper.validate_translation.return_value = {
            'lengthRatio': 1.0,
            'specifiersMatch': True
        }
        self.analyzer.swift_helper.check_layout.return_value = {
            'isRTL': True
        }

        issues = self.analyze_xcstrings(translations, "en")
        
        self.assertIn("RTL considerations needed for 'welcome_message' in ar", issues['rtl_issues'])
        self.assertEqual(len(issues['missing_translations']), 0)
        self.assertEqual(len(issues['length_issues']), 0)
        self.assertEqual(len(issues['format_issues']), 0)

if __name__ == '__main__':
    unittest.main()
