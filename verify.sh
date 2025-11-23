#!/bin/bash

#############################################################################
# Website Migration Tool - Verification Script
# Checks if all dependencies are installed and runs basic tests
#############################################################################

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "${BLUE}╔═══════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║     Website Migration Tool - Verification            ║${NC}"
    echo -e "${BLUE}╚═══════════════════════════════════════════════════════╝${NC}"
    echo ""
}

check_pass() {
    echo -e "${GREEN}✓${NC} $1"
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

check_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

verify_dependencies() {
    echo -e "${BLUE}Checking Dependencies...${NC}"
    echo ""

    local all_good=true

    # Check wget
    if command -v wget &> /dev/null; then
        local wget_version=$(wget --version | head -n1)
        check_pass "wget is installed: $wget_version"
    else
        check_fail "wget is NOT installed"
        echo "  Install: sudo apt-get install wget  (Ubuntu/Debian)"
        echo "          sudo yum install wget       (CentOS/RHEL)"
        echo "          brew install wget           (macOS)"
        all_good=false
    fi

    # Check bash version
    if [ -n "$BASH_VERSION" ]; then
        check_pass "bash is installed: $BASH_VERSION"
    else
        check_fail "bash is NOT available"
        all_good=false
    fi

    # Check for basic Unix tools
    for cmd in awk sed grep find du; do
        if command -v $cmd &> /dev/null; then
            check_pass "$cmd is available"
        else
            check_fail "$cmd is NOT available"
            all_good=false
        fi
    done

    echo ""
    return $([ "$all_good" = true ] && echo 0 || echo 1)
}

verify_scripts() {
    echo -e "${BLUE}Checking Scripts...${NC}"
    echo ""

    local all_good=true

    # Check if scripts exist and are executable
    for script in migrate.sh batch_migrate.sh; do
        if [ -f "$script" ]; then
            if [ -x "$script" ]; then
                check_pass "$script exists and is executable"
            else
                check_warn "$script exists but is not executable"
                echo "  Fix: chmod +x $script"
            fi
        else
            check_fail "$script is missing"
            all_good=false
        fi
    done

    # Check if documentation exists
    for doc in README.md QUICK_START.md; do
        if [ -f "$doc" ]; then
            check_pass "$doc exists"
        else
            check_warn "$doc is missing"
        fi
    done

    echo ""
    return $([ "$all_good" = true ] && echo 0 || echo 1)
}

verify_directories() {
    echo -e "${BLUE}Checking Directory Structure...${NC}"
    echo ""

    # Check if we can create directories
    if [ -w "." ]; then
        check_pass "Current directory is writable"
    else
        check_fail "Current directory is not writable"
        return 1
    fi

    # Check if output directories exist or can be created
    if [ -d "migrated_sites" ]; then
        check_info "migrated_sites directory exists"
    else
        check_info "migrated_sites directory will be created on first run"
    fi

    if [ -d "migration_logs" ]; then
        check_info "migration_logs directory exists"
    else
        check_info "migration_logs directory will be created on first run"
    fi

    echo ""
    return 0
}

test_basic_functionality() {
    echo -e "${BLUE}Running Basic Functionality Test...${NC}"
    echo ""

    # Test wget with a simple example
    check_info "Testing wget with example.com..."

    local test_file="/tmp/wget_test_$$.html"
    if wget -q -O "$test_file" --timeout=10 https://example.com 2>/dev/null; then
        if [ -f "$test_file" ] && [ -s "$test_file" ]; then
            check_pass "wget successfully downloaded a test page"
            rm -f "$test_file"
        else
            check_fail "wget download produced an empty file"
            rm -f "$test_file"
            return 1
        fi
    else
        check_fail "wget failed to download test page (check internet connection)"
        rm -f "$test_file"
        return 1
    fi

    echo ""
    return 0
}

show_summary() {
    local status=$1

    echo ""
    echo -e "${BLUE}╔═══════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║              Verification Summary                     ║${NC}"
    echo -e "${BLUE}╚═══════════════════════════════════════════════════════╝${NC}"
    echo ""

    if [ $status -eq 0 ]; then
        echo -e "${GREEN}✓ All checks passed!${NC}"
        echo -e "${GREEN}✓ Website Migration Tool is ready to use${NC}"
        echo ""
        echo "Next steps:"
        echo "  1. Read QUICK_START.md for a 60-second tutorial"
        echo "  2. Run your first migration: ./migrate.sh https://example.com"
        echo "  3. Check README.md for advanced options"
        echo ""
        return 0
    else
        echo -e "${RED}✗ Some checks failed${NC}"
        echo -e "${YELLOW}⚠ Please fix the issues above before using the tool${NC}"
        echo ""
        return 1
    fi
}

run_quick_test() {
    echo -e "${YELLOW}Would you like to run a quick test migration? (5-10 seconds)${NC}"
    echo -n "This will download example.com homepage only [y/N]: "
    read -r response

    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo ""
        echo -e "${BLUE}Running quick test migration...${NC}"
        echo ""

        # Create test directory
        local test_dir="/tmp/migration_test_$$"
        mkdir -p "$test_dir"

        # Run a minimal migration
        if wget -q --mirror --convert-links --adjust-extension \
               --page-requisites --no-parent --level=1 --tries=2 \
               --timeout=10 --directory-prefix="$test_dir" \
               https://example.com 2>/dev/null; then
            check_pass "Test migration completed successfully"

            local file_count=$(find "$test_dir" -type f | wc -l)
            check_info "Downloaded $file_count files"

            rm -rf "$test_dir"
            echo ""
            echo -e "${GREEN}✓ Test migration successful!${NC}"
            echo ""
            return 0
        else
            check_fail "Test migration failed"
            rm -rf "$test_dir"
            echo ""
            return 1
        fi
    fi

    return 0
}

main() {
    print_header

    local status=0

    # Run all verification checks
    verify_dependencies || status=1
    verify_scripts || status=1
    verify_directories || status=1
    test_basic_functionality || status=1

    # Show summary
    show_summary $status

    # Optionally run quick test
    if [ $status -eq 0 ]; then
        run_quick_test
    fi

    exit $status
}

main "$@"
