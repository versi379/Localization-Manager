# iOS/macOS Localization QA Tool

A comprehensive tool for testing and validating localizations in iOS and macOS projects. This tool helps identify common localization issues, generates QA reports, and ensures consistency across different languages.

## Features

- 🔍 Automatic detection of localization files
- 📏 Text length and overflow analysis
- 🔄 RTL layout validation
- 🚨 Missing translation detection
- 📊 Detailed QA report generation
- ⚡️ Real-time monitoring capabilities
- 🔠 Format specifier validation

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/localization-qa-tool.git
cd localization-qa-tool

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install .
```

## Quick Start

```bash
# Basic usage
localization-qa /path/to/your/xcode/project

# Generate detailed report
localization-qa /path/to/your/xcode/project --report detailed

# Watch for changes
localization-qa /path/to/your/xcode/project --watch
```

## Configuration

Create a `config.yml` in your project root (optional):

```yaml
ignore_keys:
  - debug_text
  - test_string

max_length_multiplier: 1.5
rtl_languages:
  - ar
  - he
  - fa

report_format: markdown
```

## Report Examples

The tool generates reports in multiple formats:

### Console Output
```
=== Localization Test Report ===

fr.lproj:
  ⚠️  Possible overflow in 'welcome_message': 45 chars (base: 25)
  
ar.lproj:
  ⚠️  RTL issue in 'format_string'
  ⚠️  Missing keys: help_text, about_section
```

### Markdown Report
Generates a detailed markdown report with:
- Summary statistics
- Issue breakdown by language
- Recommendations for fixes
- Visual length comparisons

