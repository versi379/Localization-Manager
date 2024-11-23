#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print section header
print_section() {
    echo -e "\n${BLUE}=== $1 ===${NC}"
}

# Function to check command existence
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}Error: $1 is not installed${NC}"
        echo -e "${YELLOW}Please install $1 and try again${NC}"
        exit 1
    fi
}

# Print welcome message
print_section "Setting up iOS/macOS Localization QA Tool"

# Check prerequisites
print_section "Checking Prerequisites"
echo -e "${GREEN}Checking required tools...${NC}"

# Check Python
check_command python3
PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✓ Found $PYTHON_VERSION${NC}"

# Check pip
check_command pip3
echo -e "${GREEN}✓ Found pip3${NC}"

# Check Swift
check_command swift
SWIFT_VERSION=$(swift --version | head -n1)
echo -e "${GREEN}✓ Found Swift${NC}"

# Create project structure
print_section "Creating Project Structure"

# Array of directories to create
directories=(
    "src/utils"
    "samples/xcstrings"
    "reports"
    "tests/test_files"
    "scripts"
)

for dir in "${directories[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        echo -e "${GREEN}✓ Created directory: $dir${NC}"
    else
        echo -e "${YELLOW}Directory already exists: $dir${NC}"
    fi
done

# Setup Python virtual environment
print_section "Setting up Python Environment"

if [ ! -d "venv" ]; then
    echo -e "${GREEN}Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${YELLOW}Virtual environment already exists${NC}"
fi

# Activate virtual environment
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Install Python dependencies
print_section "Installing Python Dependencies"

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo -e "${GREEN}✓ Installed Python dependencies${NC}"
else
    echo -e "${YELLOW}Creating requirements.txt with basic dependencies${NC}"
    cat > requirements.txt << EOF
markdown==3.4.3
pytest==7.3.1
PyYAML==6.0.1
EOF
    pip install -r requirements.txt
    echo -e "${GREEN}✓ Created and installed basic requirements${NC}"
fi

# Build Swift helper
print_section "Building Swift Helper Tool"

SWIFT_PROJECT_DIR="src/swift/LocalizationHelper"
if [ ! -d "$SWIFT_PROJECT_DIR" ]; then
    mkdir -p "$SWIFT_PROJECT_DIR"
    echo -e "${GREEN}Created Swift project directory${NC}"
    
    # Create basic Swift package
    (cd "$SWIFT_PROJECT_DIR" && swift package init)
    echo -e "${GREEN}✓ Initialized Swift package${NC}"
else
    echo -e "${YELLOW}Swift project directory already exists${NC}"
fi

# Build Swift package
(cd "$SWIFT_PROJECT_DIR" && swift build -c release)
echo -e "${GREEN}✓ Built Swift helper tool${NC}"

# Make scripts executable
print_section "Setting up Scripts"

# Make run_qa.sh executable if it exists
if [ -f "scripts/run_qa.sh" ]; then
    chmod +x scripts/run_qa.sh
    echo -e "${GREEN}✓ Made run_qa.sh executable${NC}"
else
    echo -e "${RED}Warning: run_qa.sh not found in scripts directory${NC}"
fi

# Create config file
print_section "Creating Configuration"

if [ ! -f "config.json" ]; then
    cat > config.json << EOF
{
    "ignored_keys": ["debug_text", "test_strings"],
    "length_threshold": 1.5,
    "rtl_languages": ["ar", "he", "fa"],
    "default_report_format": "console"
}
EOF
    echo -e "${GREEN}✓ Created default config.json${NC}"
else
    echo -e "${YELLOW}Configuration file already exists${NC}"
fi

# Create sample .xcstrings file if samples directory is empty
if [ ! "$(ls -A samples/xcstrings)" ]; then
    echo -e "${YELLOW}Creating sample .xcstrings file...${NC}"
    cat > samples/xcstrings/sample.xcstrings << EOF
{
    "sourceLanguage": "en",
    "strings": {
        "welcome_message": {
            "localizations": {
                "en": {
                    "stringUnit": {
                        "state": "translated",
                        "value": "Welcome"
                    }
                }
            }
        }
    }
}
EOF
    echo -e "${GREEN}✓ Created sample .xcstrings file${NC}"
fi

# Setup complete
print_section "Setup Complete!"
echo -e "${GREEN}The Localization QA Tool has been successfully set up!${NC}"
echo
echo -e "You can now:"
echo -e "1. Run QA tests with: ${YELLOW}./scripts/run_qa.sh /path/to/project${NC}"
echo -e "2. Generate reports with: ${YELLOW}./scripts/run_qa.sh -o reports -f markdown,json /path/to/project${NC}"
echo -e "3. Watch for changes with: ${YELLOW}./scripts/run_qa.sh -w /path/to/project${NC}"
echo
echo -e "${BLUE}For more information, check the README.md file or run:${NC}"
echo -e "${YELLOW}./scripts/run_qa.sh --help${NC}"

# Deactivate virtual environment
deactivate
