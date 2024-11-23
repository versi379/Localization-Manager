import json
from typing import Dict, Optional

class StringParser:
    @staticmethod
    def parse_xcstrings_file(file_path: str) -> Optional[Dict]:
        """Parse an .xcstrings file and return its content."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except Exception as e:
            print(f"Error parsing {file_path}: {str(e)}")
            return None

    @staticmethod
    def extract_translations(xcstrings_data: Dict) -> tuple[dict, str]:
        """Extract translations from xcstrings data into a more manageable format."""
        translations = {}
        source_language = xcstrings_data.get('sourceLanguage', 'en')
        
        for key, string_data in xcstrings_data.get('strings', {}).items():
            translations[key] = {}
            localizations = string_data.get('localizations', {})
            
            for lang, lang_data in localizations.items():
                if 'stringUnit' in lang_data:
                    translations[key][lang] = {
                        'value': lang_data['stringUnit'].get('value', ''),
                        'state': lang_data['stringUnit'].get('state', ''),
                    }
                    
        return translations, source_language
