#!/bin/bash

#############################################################################
# Batch Website Migration Tool
# Migrate multiple websites from a list file
#############################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
MIGRATION_MODE="fast"
OUTPUT_DIR="./migrated_sites"
LOG_DIR="./migration_logs"
PARALLEL_JOBS=1
CONTINUE_ON_ERROR=true

show_usage() {
    cat << EOF
Usage: $0 [OPTIONS] <sites-file>

Batch migrate multiple websites from a text file (one URL per line).

OPTIONS:
    -m, --mode <mode>        Migration mode: fast, balanced, complete (default: fast)
    -o, --output <dir>       Output directory (default: ./migrated_sites)
    -l, --log <dir>          Log directory (default: ./migration_logs)
    -j, --jobs <number>      Number of parallel jobs (default: 1)
    --stop-on-error          Stop if any migration fails (default: continue)
    -h, --help               Show this help message

SITES FILE FORMAT:
    One URL per line, e.g.:
    https://example1.com
    https://example2.com
    https://example3.com

    Lines starting with # are ignored (comments)

EXAMPLES:
    # Migrate all sites in fast mode
    $0 sites.txt

    # Balanced mode with 3 parallel jobs
    $0 -m balanced -j 3 sites.txt

    # Stop on first error
    $0 --stop-on-error sites.txt

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

print_banner() {
    echo -e "${BLUE}"
    echo "╔═══════════════════════════════════════════════════════╗"
    echo "║         Batch Website Migration Tool                  ║"
    echo "║         Migrate Multiple Sites Efficiently            ║"
    echo "╚═══════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

read_sites_file() {
    local file=$1
    local -a urls=()

    if [ ! -f "$file" ]; then
        log_error "Sites file not found: $file"
        return 1
    fi

    while IFS= read -r line || [ -n "$line" ]; do
        # Skip empty lines and comments
        if [[ -n "$line" ]] && [[ ! "$line" =~ ^[[:space:]]*# ]]; then
            # Trim whitespace
            line=$(echo "$line" | xargs)
            if [[ $line =~ ^https?:// ]]; then
                urls+=("$line")
            else
                log_warn "Skipping invalid URL: $line"
            fi
        fi
    done < "$file"

    # Export array for use in main
    printf '%s\n' "${urls[@]}"
}

migrate_single_site() {
    local url=$1
    local index=$2
    local total=$3

    log_info "[$index/$total] Starting migration: $url"

    if ./migrate.sh -m "$MIGRATION_MODE" -o "$OUTPUT_DIR" -l "$LOG_DIR" "$url"; then
        log_info "[$index/$total] ✓ Successfully migrated: $url"
        return 0
    else
        log_error "[$index/$total] ✗ Failed to migrate: $url"
        return 1
    fi
}

main() {
    print_banner

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
            -l|--log)
                LOG_DIR="$2"
                shift 2
                ;;
            -j|--jobs)
                PARALLEL_JOBS="$2"
                shift 2
                ;;
            --stop-on-error)
                CONTINUE_ON_ERROR=false
                shift
                ;;
            -h|--help)
                show_usage
                exit 0
                ;;
            *)
                SITES_FILE="$1"
                shift
                ;;
        esac
    done

    # Validate inputs
    if [ -z "$SITES_FILE" ]; then
        log_error "No sites file provided"
        show_usage
        exit 1
    fi

    if [ ! -f "$SITES_FILE" ]; then
        log_error "Sites file not found: $SITES_FILE"
        exit 1
    fi

    # Read URLs from file
    mapfile -t URLS < <(read_sites_file "$SITES_FILE")

    if [ ${#URLS[@]} -eq 0 ]; then
        log_error "No valid URLs found in $SITES_FILE"
        exit 1
    fi

    log_info "Found ${#URLS[@]} sites to migrate"
    log_info "Migration mode: $MIGRATION_MODE"
    log_info "Parallel jobs: $PARALLEL_JOBS"
    echo ""

    # Migration tracking
    local success_count=0
    local failure_count=0
    local start_time=$(date +%s)

    # Migrate each site
    local index=1
    for url in "${URLS[@]}"; do
        echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

        if migrate_single_site "$url" "$index" "${#URLS[@]}"; then
            ((success_count++))
        else
            ((failure_count++))
            if [ "$CONTINUE_ON_ERROR" = false ]; then
                log_error "Stopping due to error (--stop-on-error enabled)"
                break
            fi
        fi

        ((index++))
        echo ""
    done

    # Calculate total time
    local end_time=$(date +%s)
    local total_duration=$((end_time - start_time))
    local minutes=$((total_duration / 60))
    local seconds=$((total_duration % 60))

    # Print summary
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}"
    echo "╔═══════════════════════════════════════════════════════╗"
    echo "║              Batch Migration Summary                  ║"
    echo "╠═══════════════════════════════════════════════════════╣"
    printf "║ %-35s ${BLUE}%-18s${GREEN}║${NC}\n" "Total Sites:" "${#URLS[@]}"
    printf "${GREEN}║${NC} %-35s ${GREEN}%-18s${GREEN}║${NC}\n" "Successful:" "$success_count"
    printf "${GREEN}║${NC} %-35s ${RED}%-18s${GREEN}║${NC}\n" "Failed:" "$failure_count"
    printf "${GREEN}║${NC} %-35s ${BLUE}%-18s${GREEN}║${NC}\n" "Total Time:" "${minutes}m ${seconds}s"
    printf "${GREEN}║${NC} %-35s ${BLUE}%-18s${GREEN}║${NC}\n" "Average per Site:" "$((total_duration / ${#URLS[@]}))s"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════╝${NC}"
    echo ""

    if [ $failure_count -eq 0 ]; then
        echo -e "${GREEN}✓ All migrations completed successfully!${NC}"
        exit 0
    else
        echo -e "${YELLOW}⚠ Some migrations failed. Check logs for details.${NC}"
        exit 1
    fi
}

main "$@"
