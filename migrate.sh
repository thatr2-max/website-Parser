#!/bin/bash

#############################################################################
# Website Migration Tool - Fast Customer Website Migrations with wget
# Target: Sub 30-minute migrations
# Author: Automated Migration System
# Version: 1.0.0
#############################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default configuration
MIGRATION_MODE="fast"
OUTPUT_DIR="./migrated_sites"
LOG_DIR="./migration_logs"
MAX_RETRIES=2
TIMEOUT=10
RATE_LIMIT="2m"  # 2MB/s default rate limit for fast downloads
USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# Migration profiles
declare -A FAST_MODE=(
    [level]=1
    [retries]=2
    [timeout]=10
    [rate_limit]="5m"
    [convert_links]="yes"
    [page_requisites]="yes"
    [adjust_extension]="yes"
    [max_redirect]=3
)

declare -A BALANCED_MODE=(
    [level]=3
    [retries]=3
    [timeout]=15
    [rate_limit]="3m"
    [convert_links]="yes"
    [page_requisites]="yes"
    [adjust_extension]="yes"
    [max_redirect]=5
)

declare -A COMPLETE_MODE=(
    [level]=inf
    [retries]=5
    [timeout]=30
    [rate_limit]="2m"
    [convert_links]="yes"
    [page_requisites]="yes"
    [adjust_extension]="yes"
    [max_redirect]=10
)

#############################################################################
# Helper Functions
#############################################################################

print_banner() {
    echo -e "${BLUE}"
    echo "╔═══════════════════════════════════════════════════════╗"
    echo "║     Website Migration Tool - Sub 30-Min Migrations   ║"
    echo "║                 Powered by wget                       ║"
    echo "╚═══════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] $1" >> "$LOG_FILE"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [WARN] $1" >> "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [ERROR] $1" >> "$LOG_FILE"
}

show_usage() {
    cat << EOF
Usage: $0 [OPTIONS] <URL>

Fast website migration tool optimized for sub-30-minute migrations.

OPTIONS:
    -m, --mode <mode>          Migration mode: fast, balanced, complete (default: fast)
    -o, --output <dir>         Output directory (default: ./migrated_sites)
    -l, --log <dir>            Log directory (default: ./migration_logs)
    -r, --rate-limit <rate>    Download rate limit (e.g., 2m, 500k) (default: 2m)
    -d, --depth <level>        Maximum recursion depth (default: based on mode)
    -e, --exclude <pattern>    Exclude URLs matching pattern (can be used multiple times)
    -i, --include <pattern>    Include only URLs matching pattern
    --no-parent                Don't ascend to parent directory
    --mirror-images-only       Only download images (jpg, png, gif, svg)
    --mirror-assets-only       Only download assets (css, js, images, fonts)
    -h, --help                 Show this help message

MIGRATION MODES:
    fast       - Quick migration (depth 1, optimized for speed) ~5-15 min
    balanced   - Moderate migration (depth 3, good coverage) ~15-25 min
    complete   - Full site migration (unlimited depth) ~30+ min

EXAMPLES:
    # Fast migration (recommended for most sites)
    $0 https://example.com

    # Balanced migration with custom output
    $0 -m balanced -o /backup/sites https://example.com

    # Complete migration excluding admin pages
    $0 -m complete -e "*/admin/*" https://example.com

    # Only migrate images
    $0 --mirror-images-only https://example.com/gallery

EOF
}

validate_url() {
    local url=$1
    if [[ ! $url =~ ^https?:// ]]; then
        log_error "Invalid URL: $url (must start with http:// or https://)"
        return 1
    fi
    return 0
}

create_directories() {
    mkdir -p "$OUTPUT_DIR"
    mkdir -p "$LOG_DIR"
    log_info "Created directories: $OUTPUT_DIR, $LOG_DIR"
}

get_domain_from_url() {
    echo "$1" | awk -F/ '{print $3}'
}

estimate_time() {
    local mode=$1
    case $mode in
        fast)
            echo "5-15 minutes"
            ;;
        balanced)
            echo "15-25 minutes"
            ;;
        complete)
            echo "30+ minutes"
            ;;
        *)
            echo "Unknown"
            ;;
    esac
}

#############################################################################
# Migration Functions
#############################################################################

migrate_website() {
    local url=$1
    local domain=$(get_domain_from_url "$url")
    local site_dir="$OUTPUT_DIR/$domain"
    local start_time=$(date +%s)

    log_info "Starting migration of: $url"
    log_info "Migration mode: $MIGRATION_MODE"
    log_info "Estimated time: $(estimate_time $MIGRATION_MODE)"
    log_info "Output directory: $site_dir"

    # Build wget command based on mode
    local wget_cmd="wget"
    local wget_opts=""

    case $MIGRATION_MODE in
        fast)
            wget_opts=$(build_wget_opts_fast "$url")
            ;;
        balanced)
            wget_opts=$(build_wget_opts_balanced "$url")
            ;;
        complete)
            wget_opts=$(build_wget_opts_complete "$url")
            ;;
    esac

    # Add custom options
    if [ -n "$CUSTOM_DEPTH" ]; then
        wget_opts="$wget_opts -l $CUSTOM_DEPTH"
    fi

    if [ -n "$EXCLUDE_PATTERNS" ]; then
        for pattern in "${EXCLUDE_PATTERNS[@]}"; do
            wget_opts="$wget_opts --exclude-domains=$pattern"
        done
    fi

    if [ "$NO_PARENT" = true ]; then
        wget_opts="$wget_opts --no-parent"
    fi

    if [ "$IMAGES_ONLY" = true ]; then
        wget_opts="$wget_opts -A jpg,jpeg,png,gif,svg,webp,bmp,ico"
    fi

    if [ "$ASSETS_ONLY" = true ]; then
        wget_opts="$wget_opts -A css,js,jpg,jpeg,png,gif,svg,webp,woff,woff2,ttf,eot"
    fi

    # Execute migration
    log_info "Executing: wget $wget_opts"

    cd "$OUTPUT_DIR"
    if eval "wget $wget_opts 2>&1 | tee -a '$LOG_FILE'"; then
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        local minutes=$((duration / 60))
        local seconds=$((duration % 60))

        log_info "Migration completed successfully!"
        log_info "Duration: ${minutes}m ${seconds}s"
        log_info "Files saved to: $site_dir"

        # Show statistics
        show_statistics "$site_dir" "$duration"

        return 0
    else
        log_error "Migration failed. Check logs at: $LOG_FILE"
        return 1
    fi
}

build_wget_opts_fast() {
    local url=$1
    cat << EOF
--mirror \
--convert-links \
--adjust-extension \
--page-requisites \
--no-parent \
--random-wait \
--limit-rate=${FAST_MODE[rate_limit]} \
--tries=${FAST_MODE[retries]} \
--timeout=${FAST_MODE[timeout]} \
--level=${FAST_MODE[level]} \
--max-redirect=${FAST_MODE[max_redirect]} \
--reject="*.exe,*.dmg,*.pkg,*.deb,*.rpm,*.zip,*.tar.gz,*.iso" \
--user-agent="$USER_AGENT" \
--execute robots=off \
"$url"
EOF
}

build_wget_opts_balanced() {
    local url=$1
    cat << EOF
--mirror \
--convert-links \
--adjust-extension \
--page-requisites \
--no-parent \
--random-wait \
--limit-rate=${BALANCED_MODE[rate_limit]} \
--tries=${BALANCED_MODE[retries]} \
--timeout=${BALANCED_MODE[timeout]} \
--level=${BALANCED_MODE[level]} \
--max-redirect=${BALANCED_MODE[max_redirect]} \
--reject="*.exe,*.dmg,*.pkg,*.deb,*.rpm" \
--user-agent="$USER_AGENT" \
--execute robots=off \
"$url"
EOF
}

build_wget_opts_complete() {
    local url=$1
    cat << EOF
--mirror \
--convert-links \
--adjust-extension \
--page-requisites \
--no-parent \
--random-wait \
--limit-rate=${COMPLETE_MODE[rate_limit]} \
--tries=${COMPLETE_MODE[retries]} \
--timeout=${COMPLETE_MODE[timeout]} \
--level=${COMPLETE_MODE[level]} \
--max-redirect=${COMPLETE_MODE[max_redirect]} \
--user-agent="$USER_AGENT" \
--execute robots=off \
"$url"
EOF
}

show_statistics() {
    local site_dir=$1
    local duration=$2

    if [ -d "$site_dir" ]; then
        local file_count=$(find "$site_dir" -type f | wc -l)
        local total_size=$(du -sh "$site_dir" 2>/dev/null | cut -f1)
        local html_count=$(find "$site_dir" -type f -name "*.html" | wc -l)
        local css_count=$(find "$site_dir" -type f -name "*.css" | wc -l)
        local js_count=$(find "$site_dir" -type f -name "*.js" | wc -l)
        local img_count=$(find "$site_dir" -type f \( -name "*.jpg" -o -name "*.png" -o -name "*.gif" -o -name "*.svg" \) | wc -l)

        echo ""
        echo -e "${GREEN}╔═══════════════════════════════════════════════════════╗${NC}"
        echo -e "${GREEN}║              Migration Statistics                     ║${NC}"
        echo -e "${GREEN}╠═══════════════════════════════════════════════════════╣${NC}"
        printf "${GREEN}║${NC} %-35s ${BLUE}%-18s${GREEN}║${NC}\n" "Total Duration:" "$((duration / 60))m $((duration % 60))s"
        printf "${GREEN}║${NC} %-35s ${BLUE}%-18s${GREEN}║${NC}\n" "Total Files:" "$file_count"
        printf "${GREEN}║${NC} %-35s ${BLUE}%-18s${GREEN}║${NC}\n" "Total Size:" "$total_size"
        printf "${GREEN}║${NC} %-35s ${BLUE}%-18s${GREEN}║${NC}\n" "HTML Pages:" "$html_count"
        printf "${GREEN}║${NC} %-35s ${BLUE}%-18s${GREEN}║${NC}\n" "CSS Files:" "$css_count"
        printf "${GREEN}║${NC} %-35s ${BLUE}%-18s${GREEN}║${NC}\n" "JavaScript Files:" "$js_count"
        printf "${GREEN}║${NC} %-35s ${BLUE}%-18s${GREEN}║${NC}\n" "Images:" "$img_count"
        echo -e "${GREEN}╚═══════════════════════════════════════════════════════╝${NC}"
        echo ""

        if [ $duration -lt 1800 ]; then
            echo -e "${GREEN}✓ Migration completed in under 30 minutes!${NC}"
        else
            echo -e "${YELLOW}⚠ Migration took longer than 30 minutes. Consider using 'fast' mode.${NC}"
        fi
    fi
}

#############################################################################
# Main Script
#############################################################################

main() {
    print_banner

    # Parse command line arguments
    EXCLUDE_PATTERNS=()
    NO_PARENT=false
    IMAGES_ONLY=false
    ASSETS_ONLY=false
    CUSTOM_DEPTH=""

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
            -l|--log)
                LOG_DIR="$2"
                shift 2
                ;;
            -r|--rate-limit)
                RATE_LIMIT="$2"
                shift 2
                ;;
            -d|--depth)
                CUSTOM_DEPTH="$2"
                shift 2
                ;;
            -e|--exclude)
                EXCLUDE_PATTERNS+=("$2")
                shift 2
                ;;
            --no-parent)
                NO_PARENT=true
                shift
                ;;
            --mirror-images-only)
                IMAGES_ONLY=true
                shift
                ;;
            --mirror-assets-only)
                ASSETS_ONLY=true
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

    # Validate inputs
    if [ -z "$URL" ]; then
        log_error "No URL provided"
        show_usage
        exit 1
    fi

    if ! validate_url "$URL"; then
        exit 1
    fi

    if [[ ! "$MIGRATION_MODE" =~ ^(fast|balanced|complete)$ ]]; then
        log_error "Invalid migration mode: $MIGRATION_MODE"
        show_usage
        exit 1
    fi

    # Setup
    create_directories

    local domain=$(get_domain_from_url "$URL")
    LOG_FILE="$LOG_DIR/migration_${domain}_$(date +%Y%m%d_%H%M%S).log"

    log_info "Migration started at $(date)"
    log_info "Target URL: $URL"

    # Run migration
    if migrate_website "$URL"; then
        log_info "Migration process completed successfully"
        exit 0
    else
        log_error "Migration process failed"
        exit 1
    fi
}

# Run main function
main "$@"
