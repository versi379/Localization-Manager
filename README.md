# iOS/macOS Localization QA Tool
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

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

Clone the repository:
```bash
git clone https://github.com/yourusername/localization-testing-tool.git
cd localization-testing-tool
```

## 📚 Project Structure

```
├── LICENSE                 # License file for the project
├── README.md               # Project documentation and instructions
├── src
│   ├── localization_tester.py  # Main script to test localization functionality
│   ├── swift
│   │   └── LocalizationHelper  # Swift code for localization functionality
│   └── utils
│       ├── report_generator.py  # Script to generate reports
│       ├── string_parser.py  # Script to parse strings
│       └── swift_bridge.py  # Bridges Python and Swift code
└── tests
    ├── test_analyzer.py    # Unit tests for text_analyzer.py
    ├── test_parser.py      # Unit tests for string_parser.py
    └── test_swift_bridge.py  # Unit tests for swift_bridge.py

```

## 🎯 Usage

To test a single .xcstrings file, simply run the main script:

```bash
python localization_tester.py
```

This will:
1. Open a file dialog that allows the user to select the `.xcstrings` file.
2. Analyze the localization in the selected file.
3. Generate a Markdown report and save it to a `reports` folder in the same directory as the `.xcstrings` file, with a filename that includes the current date and time.
4. Print the report to the terminal.

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

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
