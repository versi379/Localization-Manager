from setuptools import setup, find_packages
import subprocess
import os

def build_swift_helper():
    """Build the Swift helper tool."""
    swift_project_path = 'src/swift/LocalizationHelper'
    try:
        subprocess.run([
            'xcodebuild',
            '-project', f'{swift_project_path}/LocalizationHelper.xcodeproj',
            '-scheme', 'LocalizationHelper',
            '-configuration', 'Release',
            'BUILD_DIR=build'
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error building Swift helper: {e}")
        raise

# Build Swift helper during installation
build_swift_helper()

setup(
    name="localization-qa-tool",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pyyaml>=5.1",
        "watchdog>=2.1.6",
        "markdown>=3.3",
        "rich>=10.0.0",
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "localization-qa=src.localization_tester:main",
        ],
    },
    include_package_data=True,
    package_data={
        'localization_qa': ['swift/LocalizationHelper/build/LocalizationHelper'],
    },
)