# tests/__init__.py
"""
Test suite for the Localization QA Tool.
Includes unit tests and integration tests for all components.
"""

import os

# Helper function for test data paths
def get_test_data_path(filename: str) -> str:
    """Returns the full path to a test data file."""
    return os.path.join(
        os.path.dirname(__file__),
        'test_data',
        filename
    )

__all__ = ['get_test_data_path']