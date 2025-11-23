#!/bin/bash

#############################################################################
# Website Migration Tool - Configuration Example
# Copy this file to config.sh and customize as needed
#############################################################################

# Default Migration Mode
# Options: fast, balanced, complete
export MIGRATION_MODE="fast"

# Output Directory
# Where migrated websites will be saved
export OUTPUT_DIR="./migrated_sites"

# Log Directory
# Where migration logs will be stored
export LOG_DIR="./migration_logs"

# Download Rate Limit
# Examples: 1m (1 MB/s), 500k (500 KB/s), 10m (10 MB/s)
export RATE_LIMIT="2m"

# Maximum Retries
# How many times to retry failed downloads
export MAX_RETRIES=3

# Timeout
# Connection timeout in seconds
export TIMEOUT=15

# User Agent
# Browser user-agent string to use
export USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# Exclusion Patterns
# Domains or patterns to exclude (space-separated)
export EXCLUDE_PATTERNS="*.exe *.dmg *.pkg *.deb *.rpm"

# Include Patterns
# Only download files matching these patterns (leave empty for all)
export INCLUDE_PATTERNS=""

# Fast Mode Settings
export FAST_LEVEL=1
export FAST_RETRIES=2
export FAST_TIMEOUT=10
export FAST_RATE_LIMIT="5m"

# Balanced Mode Settings
export BALANCED_LEVEL=3
export BALANCED_RETRIES=3
export BALANCED_TIMEOUT=15
export BALANCED_RATE_LIMIT="3m"

# Complete Mode Settings
export COMPLETE_LEVEL=0  # 0 = infinite
export COMPLETE_RETRIES=5
export COMPLETE_TIMEOUT=30
export COMPLETE_RATE_LIMIT="2m"

# Advanced Options
export CONVERT_LINKS=true           # Convert links for offline browsing
export PAGE_REQUISITES=true         # Download images, CSS, JS
export ADJUST_EXTENSION=true        # Add .html to files without extension
export NO_PARENT=true               # Don't ascend to parent directory
export RANDOM_WAIT=true             # Random wait between requests (polite)
export SPAN_HOSTS=false             # Don't download from other domains
export ROBOTS_OFF=true              # Ignore robots.txt

# Parallel Downloads (experimental)
export PARALLEL_DOWNLOADS=1         # Number of parallel wget processes

# Notification Settings (optional)
export ENABLE_NOTIFICATIONS=false   # Enable desktop notifications
export NOTIFY_ON_COMPLETE=true      # Notify when migration completes
export NOTIFY_ON_ERROR=true         # Notify on errors

# Email Notifications (requires mailx or sendmail)
export EMAIL_NOTIFICATIONS=false
export EMAIL_TO=""
export EMAIL_FROM=""

# Slack/Webhook Notifications
export WEBHOOK_URL=""
export WEBHOOK_ON_COMPLETE=false
export WEBHOOK_ON_ERROR=false

# Custom wget options
# Add any additional wget options here
export CUSTOM_WGET_OPTS=""

#############################################################################
# Usage: Source this file in your migration scripts
# source ./config.sh
#############################################################################
