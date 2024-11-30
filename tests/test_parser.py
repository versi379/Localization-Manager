import unittest
import json
import os
from unittest.mock import mock_open, patch
from src.utils.string_parser import StringParser

class TestStringParser(unittest.TestCase):
    def setUp(self):
        """Set up sample .xcstrings data for testing."""
        self.sample_xcstrings_data = {
            "sourceLanguage": "en",
            "strings": {
                "greeting": {
                    "localizations": {
                        "en": {"stringUnit": {"value": "Hello", "state": "approved"}},
                        "fr": {"stringUnit": {"value": "Bonjour", "state": "approved"}},
                    }
                },
                "farewell": {
                    "localizations": {
                        "en": {"stringUnit": {"value": "Goodbye", "state": "approved"}},
                        "es": {"stringUnit": {"value": "Adiós", "state": "approved"}},
                    }
                }
            }
        }

        self.sample_xcstrings_json = json.dumps(self.sample_xcstrings_data)

    @patch("builtins.open", new_callable=mock_open, read_data="{}")
    def test_parse_xcstrings_file_success(self, mock_file):
        """Test successful parsing of an .xcstrings file."""
        mock_file.return_value.read.return_value = self.sample_xcstrings_json
        result = StringParser.parse_xcstrings_file("mock_file_path.xcstrings")

        self.assertIsInstance(result, dict)
        self.assertIn("sourceLanguage", result)
        self.assertEqual(result["sourceLanguage"], "en")
        self.assertIn("strings", result)

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_parse_xcstrings_file_file_not_found(self, mock_file):
        """Test handling of a missing .xcstrings file."""
        result = StringParser.parse_xcstrings_file("nonexistent_file.xcstrings")
        self.assertIsNone(result)

    @patch("builtins.open", new_callable=mock_open, read_data="invalid_json")
    def test_parse_xcstrings_file_invalid_json(self, mock_file):
        """Test handling of invalid JSON content in the file."""
        result = StringParser.parse_xcstrings_file("mock_file_path.xcstrings")
        self.assertIsNone(result)

    def test_extract_translations(self):
        """Test extraction of translations from xcstrings data."""
        translations, source_language = StringParser.extract_translations(
            self.sample_xcstrings_data
        )

        self.assertIsInstance(translations, dict)
        self.assertEqual(source_language, "en")
        self.assertIn("greeting", translations)
        self.assertIn("farewell", translations)

        # Check translations for "greeting"
        self.assertIn("en", translations["greeting"])
        self.assertIn("fr", translations["greeting"])
        self.assertEqual(translations["greeting"]["en"]["value"], "Hello")
        self.assertEqual(translations["greeting"]["fr"]["value"], "Bonjour")

        # Check translations for "farewell"
        self.assertIn("en", translations["farewell"])
        self.assertIn("es", translations["farewell"])
        self.assertEqual(translations["farewell"]["en"]["value"], "Goodbye")
        self.assertEqual(translations["farewell"]["es"]["value"], "Adiós")

    def test_extract_translations_missing_localizations(self):
        """Test extraction of translations with missing localizations."""
        incomplete_xcstrings_data = {
            "sourceLanguage": "en",
            "strings": {
                "greeting": {
                    "localizations": {
                        "en": {"stringUnit": {"value": "Hello", "state": "approved"}}
                        # Missing "fr" localization
                    }
                }
            }
        }
        
        translations, source_language = StringParser.extract_translations(
            incomplete_xcstrings_data
        )

        self.assertIn("greeting", translations)
        self.assertIn("en", translations["greeting"])
        self.assertNotIn("fr", translations["greeting"])
        self.assertEqual(translations["greeting"]["en"]["value"], "Hello")

if __name__ == "__main__":
    unittest.main()
