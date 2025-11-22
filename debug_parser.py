#!/usr/bin/env python3
"""
Debug Parser - Test individual HTML files
Usage: python debug_parser.py <path-to-html-file>
"""

import sys
from pathlib import Path
from bs4 import BeautifulSoup

# Import functions from parse_site
from parse_site import (
    parse_html_file, clean_html_content, convert_to_markdown,
    detect_page_type, extract_phone_numbers, extract_emails, extract_dates
)

def debug_parse_file(file_path: str):
    """Parse a single file with detailed debug output"""

    print("=" * 70)
    print(f"🔍 DEBUG PARSER - {file_path}")
    print("=" * 70)

    file_path = Path(file_path)

    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return

    print(f"\n📂 File: {file_path.name}")
    print(f"📍 Full path: {file_path.absolute()}")

    # Step 1: Read raw HTML
    print("\n" + "-" * 70)
    print("STEP 1: Reading HTML file...")
    print("-" * 70)
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            html_content = f.read()
        print(f"✓ Read {len(html_content)} characters")
        print(f"✓ First 200 chars: {html_content[:200]}")
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return

    # Step 2: Parse with BeautifulSoup
    print("\n" + "-" * 70)
    print("STEP 2: Parsing with BeautifulSoup...")
    print("-" * 70)
    try:
        soup = BeautifulSoup(html_content, 'lxml')
        print(f"✓ Parsed successfully")

        # Extract title
        title_tag = soup.find('title')
        title = title_tag.get_text(strip=True) if title_tag else 'No title'
        print(f"✓ Title: {title}")

        # Count elements
        all_tags = soup.find_all(True)
        print(f"✓ Total elements: {len(all_tags)}")

        # Show element types
        tag_counts = {}
        for tag in all_tags[:100]:  # Check first 100 tags
            tag_name = tag.name if hasattr(tag, 'name') else 'unknown'
            tag_counts[tag_name] = tag_counts.get(tag_name, 0) + 1
        print(f"✓ Element types (first 100): {tag_counts}")

    except Exception as e:
        print(f"❌ Error parsing HTML: {e}")
        import traceback
        traceback.print_exc()
        return

    # Step 3: Clean HTML
    print("\n" + "-" * 70)
    print("STEP 3: Cleaning HTML (removing nav, footer, etc.)...")
    print("-" * 70)
    try:
        # Count before cleaning
        before_count = len(soup.find_all(True))
        print(f"✓ Elements before cleaning: {before_count}")

        cleaned_soup = clean_html_content(soup)

        # Count after cleaning
        after_count = len(cleaned_soup.find_all(True))
        print(f"✓ Elements after cleaning: {after_count}")
        print(f"✓ Removed {before_count - after_count} elements")

        # Show cleaned HTML (first 500 chars)
        cleaned_html = str(cleaned_soup)[:500]
        print(f"✓ Cleaned HTML preview:\n{cleaned_html}...")

    except Exception as e:
        print(f"❌ Error cleaning HTML: {e}")
        import traceback
        traceback.print_exc()
        return

    # Step 4: Detect page type
    print("\n" + "-" * 70)
    print("STEP 4: Detecting page type...")
    print("-" * 70)
    try:
        text_content = cleaned_soup.get_text(separator=' ', strip=True)
        page_type = detect_page_type(file_path.name, title, text_content)
        print(f"✓ Detected page type: {page_type}")
        print(f"✓ Filename: {file_path.name}")
        print(f"✓ Title: {title}")
        print(f"✓ Content preview: {text_content[:200]}...")
    except Exception as e:
        print(f"❌ Error detecting page type: {e}")
        import traceback
        traceback.print_exc()
        page_type = 'unknown'

    # Step 5: Convert to Markdown
    print("\n" + "-" * 70)
    print("STEP 5: Converting to Markdown...")
    print("-" * 70)
    try:
        markdown = convert_to_markdown(str(cleaned_soup))
        print(f"✓ Converted to markdown ({len(markdown)} characters)")
        print(f"\n--- MARKDOWN OUTPUT (first 1000 chars) ---")
        print(markdown[:1000])
        if len(markdown) > 1000:
            print(f"\n... ({len(markdown) - 1000} more characters)")
    except Exception as e:
        print(f"❌ Error converting to markdown: {e}")
        import traceback
        traceback.print_exc()
        return

    # Step 6: Extract metadata
    print("\n" + "-" * 70)
    print("STEP 6: Extracting metadata...")
    print("-" * 70)
    try:
        text_content = cleaned_soup.get_text(separator=' ', strip=True)

        phones = extract_phone_numbers(text_content)
        emails = extract_emails(text_content)
        dates = extract_dates(text_content)

        print(f"✓ Phone numbers found: {phones[:5] if phones else 'None'}")
        print(f"✓ Emails found: {emails[:5] if emails else 'None'}")
        print(f"✓ Dates found: {dates[:5] if dates else 'None'}")
    except Exception as e:
        print(f"❌ Error extracting metadata: {e}")
        import traceback
        traceback.print_exc()

    # Step 7: Full parse (using the actual function)
    print("\n" + "-" * 70)
    print("STEP 7: Running full parse_html_file() function...")
    print("-" * 70)
    try:
        result = parse_html_file(file_path)
        print(f"✓ Parse successful!")
        print(f"✓ Result keys: {result.keys()}")
        print(f"✓ Page type: {result.get('type')}")
        print(f"✓ Title: {result.get('title')}")
        print(f"✓ Content length: {len(result.get('content', ''))}")
    except Exception as e:
        print(f"❌ Error in parse_html_file: {e}")
        import traceback
        traceback.print_exc()
        return

    print("\n" + "=" * 70)
    print("✅ DEBUG COMPLETE")
    print("=" * 70)


def main():
    if len(sys.argv) < 2:
        print("Usage: python debug_parser.py <path-to-html-file>")
        print("\nExample:")
        print("  python debug_parser.py downloads/www.abbottstownborough.com/index.html")
        print("\nOr test all files in a directory:")
        print("  python debug_parser.py downloads/www.abbottstownborough.com/*.html")
        sys.exit(1)

    file_path = sys.argv[1]
    debug_parse_file(file_path)


if __name__ == '__main__':
    main()
