import unittest
import json
from src.utils.string_parser import StringParser

class TestStringParser(unittest.TestCase):
    def setUp(self):
        self.parser = StringParser()
        self.sample_xcstrings = {
            "sourceLanguage": "en",
            "strings": {
                "hello_world": {
                    "localizations": {
                        "en": {
                            "stringUnit": {
                                "state": "translated",
                                "value": "Hello World"
                            }
                        },
                        "fr": {
                            "stringUnit": {
                                "state": "translated",
                                "value": "Bonjour le monde"
                            }
                        }
                    }
                }
            }
        }

    def test_parse_xcstrings_file(self):
        # Create a temporary xcstrings file
        with open('test.xcstrings', 'w') as f:
            json.dump(self.sample_xcstrings, f)

        result = self.parser.parse_xcstrings_file('test.xcstrings')
        self.assertIsNotNone(result)
        self.assertEqual(result['sourceLanguage'], 'en')
        
        # Cleanup
        import os
        os.remove('test.xcstrings')

    def test_extract_translations(self):
        translations, source_language = self.parser.extract_translations(self.sample_xcstrings)
        
        self.assertEqual(source_language, 'en')
        self.assertIn('hello_world', translations)
        self.assertEqual(
            translations['hello_world']['en']['value'],
            'Hello World'
        )
        self.assertEqual(
            translations['hello_world']['fr']['value'],
            'Bonjour le monde'
        )

if __name__ == '__main__':
    unittest.main()