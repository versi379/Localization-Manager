# iOS/macOS Localization QA Tool

A powerful Python-based tool for testing and validating iOS/macOS app localizations in `.xcstrings` files. Analyzes translations, identifies potential issues, and generates comprehensive QA reports to ensure your app's localization quality.

## 🚀 Features

- 🔍 Smart `.xcstrings` file detection and parsing
- 📏 Translation length analysis and UI impact prediction
- 🔄 RTL language support and bidirectional text validation
- 🚨 Missing translation detection across all languages
- 🎯 Format specifier matching and validation
- 📊 Multi-format reporting (Console, Markdown, JSON)
- ⚡️ Real-time file watching for continuous QA
- 🔠 Swift-powered text analysis for iOS/macOS

## 📋 Prerequisites

- Python 3.8+
- Xcode project with `.xcstrings` files
- Swift toolchain (for the helper tool)

## 🛠 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/localization-testing-tool.git
cd localization-testing-tool
```

2. Run the setup script:
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

This will:
- Create necessary directories
- Set up Python virtual environment
- Install dependencies
- Build Swift helper tool
- Create sample files
- Make utility scripts executable

## 📚 Project Structure

```
localization-testing-tool/
├── src/                        # Source code
│   ├── localization_tester.py  # Main script
│   └── utils/                  # Utility modules
├── samples/                    # Sample projects
│   └── xcstrings/             # Sample .xcstrings files
├── reports/                    # Generated reports
├── scripts/                    # Utility scripts
├── tests/                      # Test suite
└── config.json                 # Configuration
```

## 🎯 Usage

### Running Complete QA Analysis

To analyze all sample projects and generate comprehensive reports:

```bash
./scripts/run_all_qa.sh
```

This will:
1. Process all `.xcstrings` files in `samples/xcstrings/`
2. Generate reports for each project
3. Create a summary report
4. Store everything in the `reports/` directory

### Testing Single Project/File

```bash
# Test entire project
./scripts/run_qa.sh /path/to/your/xcode/project

# Test single file
./scripts/run_qa.sh -s /path/to/Localizable.xcstrings

# Custom output directory and specific formats
./scripts/run_qa.sh -o custom_reports -f markdown,json /path/to/project

# Watch mode for continuous testing
./scripts/run_qa.sh -w /path/to/project
```

### Available Report Formats

- `console`: Terminal-friendly output
- `markdown`: Detailed report in Markdown format
- `json`: Machine-readable JSON format

### Report Structure

Reports are organized by project:
```
reports/
├── project_name/
│   ├── report_console.txt      # Console-friendly format
│   ├── report_markdown.md      # Detailed markdown report
│   └── report_json.json        # Machine-readable format
└── summary.md                  # Overview of all projects
```

## 🔍 Issue Detection

The tool identifies several categories of localization issues:

### Missing Translations 🚫
- Untranslated strings
- Incomplete language coverage

### Length Issues 📏
- Excessive text length
- UI overflow risks
- Truncation potential

### Format Issues ⚙️
- Mismatched placeholders
- Invalid format specifiers
- Parameter order problems

### RTL Considerations 🔄
- Bidirectional text issues
- Layout mirroring needs
- RTL-specific formatting

## ⚙️ Configuration

Create or modify `config.json` in your project root:

```json
{
  "ignored_keys": ["debug_text", "test_strings"],
  "length_threshold": 1.5,
  "rtl_languages": ["ar", "he", "fa"],
  "default_report_format": "console"
}
```

## 🔄 Sample Projects

The `samples/` directory includes example `.xcstrings` files:

- `basic_app.xcstrings`: Simple app UI translations
- `e_commerce.xcstrings`: Product catalog and checkout flows
- `social_app.xcstrings`: Social networking interface

## 🛠 Available Scripts

- `scripts/setup.sh`: Initial project setup and configuration
- `scripts/run_qa.sh`: Single project/file analysis
- `scripts/run_all_qa.sh`: Complete analysis of all samples

## 💡 Common Commands

```bash
# Initial setup
./scripts/setup.sh

# Full QA analysis
./scripts/run_all_qa.sh

# View summary report
cat reports/summary.md

# Test specific project
./scripts/run_qa.sh path/to/project

# Watch mode
./scripts/run_qa.sh -w path/to/project
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Swift text analysis engine
- iOS/macOS localization best practices
- Community contributors

## ❓ Support

For issues and questions:
1. Check existing GitHub issues
2. Create a new issue if needed
3. Include sample files and reports when reporting bugs

