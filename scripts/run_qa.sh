#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
DEFAULT_OUTPUT_DIR="reports"
DEFAULT_REPORT_FORMATS=("console" "markdown" "json")

# Help function
show_help() {
    echo -e "${BLUE}iOS/macOS Localization QA Tool${NC}"
    echo
    echo "Usage: ./run_qa.sh [options] <project_path>"
    echo
    echo "Options:"
    echo "  -o, --output-dir <dir>    Specify output directory for reports (default: reports)"
    echo "  -f, --formats <formats>    Comma-separated list of report formats (default: console,markdown,json)"
    echo "  -w, --watch               Enable watch mode"
    echo "  -s, --single <file>       Test single .xcstrings file instead of project directory"
    echo "  -h, --help                Show this help message"
    echo
    echo "Example:"
    echo "  ./run_qa.sh -o custom_reports -f markdown,json /path/to/project"
    echo "  ./run_qa.sh -s /path/to/Localizable.xcstrings"
    echo
}

# Function to create directory if it doesn't exist
create_dir_if_missing() {
    if [ ! -d "$1" ]; then
        mkdir -p "$1"
        echo -e "${GREEN}Created directory: $1${NC}"
    fi
}

# Function to validate project path
validate_project() {
    if [ ! -d "$1" ] && [ ! -f "$1" ]; then
        echo -e "${RED}Error: Project path does not exist: $1${NC}"
        exit 1
    fi

    if [ -f "$1" ] && [[ "$1" != *.xcstrings ]]; then
        echo -e "${RED}Error: Single file mode requires an .xcstrings file${NC}"
        exit 1
    fi
}

# Function to run QA for a single file or project
run_qa() {
    local project_path="$1"
    local output_dir="$2"
    local formats="$3"
    local watch_mode="$4"
    local project_name=$(basename "${project_path%.*}")

    # Create project-specific output directory
    local project_output_dir="${output_dir}/${project_name}"
    create_dir_if_missing "$project_output_dir"

    # Run QA for each format
    IFS=',' read -ra FORMAT_ARRAY <<< "$formats"
    for format in "${FORMAT_ARRAY[@]}"; do
        echo -e "${BLUE}Generating ${format} report for ${project_name}...${NC}"
        
        local output_file=""
        case "$format" in
            "console")
                output_file="${project_output_dir}/report_console.txt"
                ;;
            "markdown")
                output_file="${project_output_dir}/report_markdown.md"
                ;;
            "json")
                output_file="${project_output_dir}/report_json.json"
                ;;
            *)
                echo -e "${YELLOW}Warning: Unsupported format ${format}, skipping...${NC}"
                continue
                ;;
        esac

        # Run the QA tool
        if [ "$watch_mode" = true ]; then
            python localization_tester.py "$project_path" --report "$format" --watch > "$output_file" &
            echo -e "${GREEN}Started watch mode for ${format} report${NC}"
        else
            python localization_tester.py "$project_path" --report "$format" > "$output_file"
            echo -e "${GREEN}Generated ${format} report: ${output_file}${NC}"
        fi
    done
}

# Parse command line arguments
OUTPUT_DIR="$DEFAULT_OUTPUT_DIR"
FORMATS=$(IFS=,; echo "${DEFAULT_REPORT_FORMATS[*]}")
WATCH_MODE=false
SINGLE_FILE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -o|--output-dir)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -f|--formats)
            FORMATS="$2"
            shift 2
            ;;
        -w|--watch)
            WATCH_MODE=true
            shift
            ;;
        -s|--single)
            SINGLE_FILE=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            PROJECT_PATH="$1"
            shift
            ;;
    esac
done

# Validate input
if [ -z "$PROJECT_PATH" ]; then
    echo -e "${RED}Error: Project path is required${NC}"
    show_help
    exit 1
fi

validate_project "$PROJECT_PATH"

# Create main output directory
create_dir_if_missing "$OUTPUT_DIR"

# Run QA
if [ "$SINGLE_FILE" = true ]; then
    run_qa "$PROJECT_PATH" "$OUTPUT_DIR" "$FORMATS" "$WATCH_MODE"
else
    # If it's a project directory, find all .xcstrings files
    echo -e "${BLUE}Searching for .xcstrings files in project...${NC}"
    while IFS= read -r -d '' file; do
        echo -e "${GREEN}Found .xcstrings file: $file${NC}"
        run_qa "$file" "$OUTPUT_DIR" "$FORMATS" "$WATCH_MODE"
    done < <(find "$PROJECT_PATH" -name "*.xcstrings" -print0)
fi

# If watch mode is enabled, keep script running
if [ "$WATCH_MODE" = true ]; then
    echo -e "${BLUE}Watch mode enabled. Press Ctrl+C to stop...${NC}"
    wait
else
    echo -e "${GREEN}QA testing completed!${NC}"
fi
