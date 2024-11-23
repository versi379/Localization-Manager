import unittest
import os
from src.utils.swift_bridge import SwiftBridge

class TestSwiftBridge(unittest.TestCase):
    def setUp(self):
        """Set up SwiftBridge instance and verify binary exists."""
        try:
            self.bridge = SwiftBridge()
        except FileNotFoundError as e:
            self.skipTest(
                "Swift helper binary not found. Please build the Swift tool first."
            )

    def test_analyze_text(self):
        """Test basic text analysis."""
        result = self.bridge.analyze_text("Hello World", 375.0)
        
        self.assertIsInstance(result, dict)
        self.assertIn('length', result)
        self.assertIn('words', result)
        self.assertIn('lines', result)
        self.assertEqual(result['length'], 11)  # "Hello World" length
        self.assertEqual(result['words'], 2)    # Two words
        self.assertEqual(result['lines'], 1)    # Single line

    def test_validate_translation(self):
        """Test translation validation."""
        result = self.bridge.validate_translation(
            "Hello World",
            "Bonjour le monde"
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn('lengthRatio', result)
        self.assertIn('specifiersMatch', result)
        self.assertIn('recommendation', result)

    def test_format_specifiers(self):
        """Test format specifier detection."""
        result = self.bridge.validate_translation(
            "Hello %@",
            "Bonjour %d"
        )
        
        self.assertIsInstance(result, dict)
        self.assertFalse(result['specifiersMatch'])
        self.assertTrue(any('format' in result['recommendation'].lower()))

    def test_rtl_layout(self):
        """Test RTL layout analysis."""
        result = self.bridge.check_layout("ar", "مرحبا بكم")
        
        self.assertIsInstance(result, dict)
        self.assertIn('isRTL', result)
        self.assertTrue(result['isRTL'])
        self.assertIn('textAnalysis', result)

    def test_long_text(self):
        """Test handling of longer text."""
        source = "This is a short text"
        translation = "This is a much longer text that should trigger a length warning in the analysis"
        
        result = self.bridge.validate_translation(source, translation)
        
        self.assertIsInstance(result, dict)
        self.assertGreater(result['lengthRatio'], 1.5)
        self.assertTrue(any('longer' in result['recommendation'].lower()))

    def test_error_handling(self):
        """Test error handling with invalid inputs."""
        try:
            self.bridge.analyze_text("")
        except Exception as e:
            self.fail("Empty string should not raise an exception")

        try:
            self.bridge.validate_translation("", "")
        except Exception as e:
            self.fail("Empty strings should not raise an exception")

    def test_special_characters(self):
        """Test handling of special characters."""
        text_with_special = "Hello\n世界\t🌍"
        result = self.bridge.analyze_text(text_with_special)
        
        self.assertIsInstance(result, dict)
        self.assertGreater(result['length'], 0)
        self.assertEqual(result['lines'], 2)  # Due to \n

    def test_multiple_format_specifiers(self):
        """Test handling multiple format specifiers."""
        source = "Hello %@ with %d items"
        translation = "Bonjour %@ avec %d éléments"
        
        result = self.bridge.validate_translation(source, translation)
        
        self.assertIsInstance(result, dict)
        self.assertTrue(result['specifiersMatch'])
        self.assertIn('No issues found', result['recommendation'])

if __name__ == '__main__':
    unittest.main()
