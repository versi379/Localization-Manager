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

# Function to print status
print_status() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Function to run QA for a single file
run_single_qa() {
    local file="$1"
    local basename=$(basename "$file" .xcstrings)
    print_section "Processing $basename"
    
    # Create report directories if they don't exist
    mkdir -p "reports/$basename"
    
    # Generate console report
    echo -e "${YELLOW}Generating console report...${NC}"
    python src/localization_tester.py "$file" --report console > "reports/$basename/report_console.txt"
    print_status "Console report generated"
    
    # Generate markdown report
    echo -e "${YELLOW}Generating markdown report...${NC}"
    python src/localization_tester.py "$file" --report markdown > "reports/$basename/report_markdown.md"
    print_status "Markdown report generated"
    
    # Generate JSON report
    echo -e "${YELLOW}Generating JSON report...${NC}"
    python src/localization_tester.py "$file" --report json > "reports/$basename/report_json.json"
    print_status "JSON report generated"
}

# Main script
print_section "Starting Full QA Analysis"

# Check if samples directory exists
if [ ! -d "samples/xcstrings" ]; then
    echo -e "${RED}Error: samples/xcstrings directory not found!${NC}"
    exit 1
fi

# Clean previous reports
print_section "Cleaning Previous Reports"
if [ -d "reports" ]; then
    rm -rf reports/*
    print_status "Cleaned previous reports"
else
    mkdir -p reports
    print_status "Created reports directory"
fi

# Process all .xcstrings files
print_section "Processing All Sample Projects"

# Find all .xcstrings files and process them
find samples/xcstrings -name "*.xcstrings" | while read -r file; do
    run_single_qa "$file"
done

# Generate summary report
print_section "Generating Summary Report"

# Create summary in markdown format
cat > reports/summary.md << EOF
# Localization QA Summary Report
Generated on: $(date)

## Projects Analyzed
EOF

# Add list of analyzed projects and their stats
for dir in reports/*/; do
    if [ -d "$dir" ] && [ "$(basename "$dir")" != "summary" ]; then
        project_name=$(basename "$dir")
        echo -e "\n### $project_name" >> reports/summary.md
        echo -e "\nStats:" >> reports/summary.md
        
        # Extract stats from JSON report
        if [ -f "${dir}report_json.json" ]; then
            # Parse JSON and extract relevant information
            python3 -c "
import json
with open('${dir}report_json.json', 'r') as f:
    data = json.load(f)
    stats = data.get('stats', {})
    print(f\"- Total Strings: {stats.get('total_strings', 'N/A')}\")
    print(f\"- Languages: {', '.join(stats.get('languages', []))}\")
    print(f\"- Issues Found: {stats.get('issues_found', 'N/A')}\")
    print(f\"- Missing Translations: {stats.get('missing_translations', 'N/A')}\")
" >> reports/summary.md
        fi
    fi
done

print_status "Summary report generated"

# Print completion message
print_section "QA Analysis Complete!"
echo -e "Reports have been generated in the ${GREEN}reports/${NC} directory:"
echo -e "  - Individual reports for each sample project"
echo -e "  - Summary report: ${GREEN}reports/summary.md${NC}"
echo
echo -e "To view the results:"
echo -e "1. Check individual project reports in ${YELLOW}reports/<project_name>/${NC}"
echo -e "2. View the summary report: ${YELLOW}reports/summary.md${NC}"
