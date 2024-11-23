import subprocess
import json
import os
from typing import Dict, Any

class SwiftBridge:
    def __init__(self):
        self.helper_path = '/Users/giovanni/GV/Projects/Localization-Manager-QA/src/swift/LocalizationHelper/LocalizationHelper/LocalizationHelper'

        if not os.path.exists(self.helper_path):
            raise FileNotFoundError(
                "LocalizationHelper binary not found. Please build the Swift helper first."
            )

    def analyze_text(self, text: str, width: float = 375.0) -> Dict[str, Any]:
        """Analyze text using Swift helper."""
        try:
            result = subprocess.run(
                [self.helper_path, "analyze", text, str(width)],
                capture_output=True,
                text=True
            )
            return json.loads(result.stdout)
        except Exception as e:
            print(f"Error analyzing text: {e}")
            return {}

    def validate_translation(self, source: str, translation: str) -> Dict[str, Any]:
        """Validate translation using Swift helper."""
        try:
            result = subprocess.run(
                [self.helper_path, "validate", source, translation],
                capture_output=True,
                text=True
            )
            return json.loads(result.stdout)
        except Exception as e:
            print(f"Error validating translation: {e}")
            return {}

    def check_layout(self, language: str, text: str) -> Dict[str, Any]:
        """Check layout considerations using Swift helper."""
        try:
            result = subprocess.run(
                [self.helper_path, "layout", language, text],
                capture_output=True,
                text=True
            )
            return json.loads(result.stdout)
        except Exception as e:
            print(f"Error checking layout: {e}")
            return {}