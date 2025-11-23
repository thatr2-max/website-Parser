#!/bin/bash

#############################################################################
# Complete Website Conversion Tool
# 1. Migrates website with wget
# 2. Parses and converts to standardized templates
# 3. Outputs clean, standardized website
#############################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

print_banner() {
    echo -e "${PURPLE}"
    echo "╔═══════════════════════════════════════════════════════╗"
    echo "║     Complete Website Conversion Tool                  ║"
    echo "║     Migrate → Parse → Convert → Standardize           ║"
    echo "╚═══════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

show_usage() {
    cat << EOF
Usage: $0 [OPTIONS] <URL>

Complete website conversion: Download, parse, and convert to templates.

OPTIONS:
    -m, --mode <mode>        Migration mode: fast, balanced, complete (default: balanced)
    -o, --output <dir>       Final output directory (default: ./converted_sites/<domain>)
    --keep-migrated          Keep the raw migrated files (default: delete after conversion)
    -h, --help               Show this help message

WORKFLOW:
    Step 1: Download website with wget (uses migrate.sh)
    Step 2: Parse HTML and extract content intelligently
    Step 3: Map content to standardized templates
    Step 4: Generate clean, professional website
    Step 5: Copy assets (images, documents, etc.)

EXAMPLES:
    # Convert a website (balanced mode - recommended)
    $0 https://www.example.com

    # Fast conversion (quick download, good for small sites)
    $0 -m fast https://www.smallbusiness.com

    # Complete conversion (deep crawl, best accuracy)
    $0 -m complete https://www.citygovernment.gov

WHAT YOU GET:
    - 15 standardized, professionally designed pages
    - Clean, modern, responsive design
    - Accessible and SEO-friendly
    - Easy to customize and deploy
    - All assets (images, docs) copied over

TIME ESTIMATES:
    fast     : 5-15 minutes  (quick sites, basic content)
    balanced : 15-25 minutes (recommended, good coverage)
    complete : 30-45 minutes (thorough, best accuracy)

EOF
}

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

check_dependencies() {
    log_info "Checking dependencies..."

    # Check wget
    if ! command -v wget &> /dev/null; then
        log_error "wget is not installed. Please install it first."
        exit 1
    fi

    # Check Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is not installed. Please install it first."
        exit 1
    fi

    # Check Python packages
    if ! python3 -c "import bs4" 2>/dev/null; then
        log_warn "BeautifulSoup4 not installed. Installing..."
        pip3 install beautifulsoup4 lxml html2text
    fi

    log_info "All dependencies satisfied"
}

get_domain_from_url() {
    echo "$1" | awk -F/ '{print $3}'
}

main() {
    print_banner

    # Default settings
    MIGRATION_MODE="balanced"
    OUTPUT_DIR=""
    KEEP_MIGRATED=false
    URL=""

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -m|--mode)
                MIGRATION_MODE="$2"
                shift 2
                ;;
            -o|--output)
                OUTPUT_DIR="$2"
                shift 2
                ;;
            --keep-migrated)
                KEEP_MIGRATED=true
                shift
                ;;
            -h|--help)
                show_usage
                exit 0
                ;;
            *)
                URL="$1"
                shift
                ;;
        esac
    done

    # Validate URL
    if [ -z "$URL" ]; then
        log_error "No URL provided"
        show_usage
        exit 1
    fi

    # Get domain
    DOMAIN=$(get_domain_from_url "$URL")

    # Set output directory if not specified
    if [ -z "$OUTPUT_DIR" ]; then
        OUTPUT_DIR="./converted_sites/$DOMAIN"
    fi

    # Show what we're doing
    echo -e "${GREEN}Configuration:${NC}"
    echo "  URL: $URL"
    echo "  Domain: $DOMAIN"
    echo "  Mode: $MIGRATION_MODE"
    echo "  Output: $OUTPUT_DIR"
    echo ""

    # Check dependencies
    check_dependencies
    echo ""

    START_TIME=$(date +%s)

    # ============================================================
    # STEP 1: MIGRATE WEBSITE WITH WGET
    # ============================================================
    log_step "STEP 1/5: Migrating Website with wget"

    MIGRATED_DIR="./migrated_sites/$DOMAIN"

    log_info "Downloading website..."
    log_info "This may take 5-45 minutes depending on site size and mode"
    echo ""

    if ! ./migrate.sh -m "$MIGRATION_MODE" "$URL"; then
        log_error "Migration failed. Check logs in ./migration_logs/"
        exit 1
    fi

    log_info "Website downloaded to: $MIGRATED_DIR"

    # ============================================================
    # STEP 2: PARSE AND CONVERT TO TEMPLATES
    # ============================================================
    log_step "STEP 2/5: Parsing HTML Content"

    log_info "Analyzing HTML files and extracting content..."
    echo ""

    if ! python3 parse_and_convert.py "$MIGRATED_DIR" "$OUTPUT_DIR"; then
        log_error "Parsing failed"
        exit 1
    fi

    # ============================================================
    # STEP 3: VERIFY OUTPUT
    # ============================================================
    log_step "STEP 3/5: Verifying Output"

    if [ -d "$OUTPUT_DIR" ]; then
        FILE_COUNT=$(find "$OUTPUT_DIR" -type f -name "*.html" | wc -l)
        ASSET_COUNT=$(find "$OUTPUT_DIR/assets" -type f 2>/dev/null | wc -l)

        log_info "Generated $FILE_COUNT HTML pages"
        log_info "Copied $ASSET_COUNT assets"
    else
        log_error "Output directory not created"
        exit 1
    fi

    # ============================================================
    # STEP 4: CLEANUP
    # ============================================================
    log_step "STEP 4/5: Cleanup"

    if [ "$KEEP_MIGRATED" = false ]; then
        log_info "Removing raw migrated files..."
        rm -rf "$MIGRATED_DIR"
        log_info "Cleaned up temporary files"
    else
        log_info "Keeping migrated files at: $MIGRATED_DIR"
    fi

    # ============================================================
    # STEP 5: SUMMARY
    # ============================================================
    log_step "STEP 5/5: Conversion Complete!"

    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))
    MINUTES=$((DURATION / 60))
    SECONDS=$((DURATION % 60))

    echo -e "${GREEN}"
    echo "╔═══════════════════════════════════════════════════════╗"
    echo "║              Conversion Summary                       ║"
    echo "╠═══════════════════════════════════════════════════════╣"
    printf "║ %-35s ${BLUE}%-18s${GREEN}║${NC}\n" "Total Duration:" "${MINUTES}m ${SECONDS}s"
    printf "${GREEN}║${NC} %-35s ${BLUE}%-18s${GREEN}║${NC}\n" "Source URL:" "$URL"
    printf "${GREEN}║${NC} %-35s ${BLUE}%-18s${GREEN}║${NC}\n" "Mode:" "$MIGRATION_MODE"
    printf "${GREEN}║${NC} %-35s ${BLUE}%-18s${GREEN}║${NC}\n" "Pages Generated:" "$FILE_COUNT"
    printf "${GREEN}║${NC} %-35s ${BLUE}%-18s${GREEN}║${NC}\n" "Assets Copied:" "$ASSET_COUNT"
    printf "${GREEN}║${NC} %-35s ${BLUE}%-18s${GREEN}║${NC}\n" "Output Location:" "$(basename $OUTPUT_DIR)"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════╝${NC}"
    echo ""

    # ============================================================
    # NEXT STEPS
    # ============================================================
    echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${PURPLE}Next Steps:${NC}"
    echo ""
    echo "1. Preview the website locally:"
    echo -e "   ${YELLOW}cd $OUTPUT_DIR${NC}"
    echo -e "   ${YELLOW}python3 -m http.server 8000${NC}"
    echo -e "   ${YELLOW}# Open http://localhost:8000 in your browser${NC}"
    echo ""
    echo "2. Customize the content:"
    echo -e "   ${YELLOW}# Edit HTML files directly, or${NC}"
    echo -e "   ${YELLOW}# Modify templates and re-run parser${NC}"
    echo ""
    echo "3. Deploy to production:"
    echo -e "   ${YELLOW}# Upload $OUTPUT_DIR to your web server${NC}"
    echo -e "   ${YELLOW}# Or use rsync, FTP, GitHub Pages, etc.${NC}"
    echo ""
    echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    if [ $DURATION -lt 1800 ]; then
        echo -e "${GREEN}✨ Conversion completed in under 30 minutes!${NC}"
    fi
    echo ""

    log_info "All done! Your standardized website is ready."
}

main "$@"
