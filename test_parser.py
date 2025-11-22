#!/usr/bin/env python3
"""
Test script for the municipal parser using local sample data
"""

import sys
from pathlib import Path
from datetime import datetime
import json

# Import functions from parse_site
from parse_site import (
    find_html_files, parse_html_file, extract_metadata,
    map_content_to_pages, generate_output_files,
    print_header, show_progress, print_summary
)

def main():
    print_header()

    # Use the sample site we created
    download_path = "./downloads/sampletown.gov"
    domain = "sampletown.gov"

    # Step 1: Find HTML files
    html_files = find_html_files(download_path)

    if not html_files:
        show_progress("No HTML files found in downloaded content", "error")
        sys.exit(1)

    # Step 2: Parse HTML files
    show_progress("Parsing content...", "progress")
    parsed_files = []
    for html_file in html_files:
        parsed = parse_html_file(html_file)
        if parsed:
            parsed_files.append(parsed)
            show_progress(f"✓ Parsed {html_file.name} ({parsed.get('type', 'unknown')})", "success")

    # Step 3: Extract metadata
    show_progress("Extracting metadata...", "progress")
    metadata = extract_metadata(html_files)
    metadata['source_url'] = f"http://{domain}"
    metadata['parsed_at'] = datetime.now().isoformat()
    show_progress(f"✓ Found municipality: {metadata['municipality_name']}", "success")

    # Step 4: Map content to pages
    show_progress("Mapping content to pages...", "progress")
    pages = map_content_to_pages(parsed_files)

    # Step 5: Build complete data structure
    data = {
        'metadata': metadata,
        'pages': pages
    }

    # Step 6: Generate output files
    output_dir = Path(f"./output/{domain}")
    generate_output_files(data, output_dir)

    # Step 7: Print summary
    print_summary(data, len(html_files), output_dir)

    print("🎯 Next steps:")
    print("   1. Review JSON file for accuracy")
    print("   2. Edit markdown files as needed")
    print("   3. Deploy to platform\n")

if __name__ == '__main__':
    main()
