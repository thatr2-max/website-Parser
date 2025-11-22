#!/usr/bin/env python3
"""
Municipal Website Parser & Converter
=====================================
Automatically downloads, parses, and converts municipal websites into a
structured 12-page format with clean markdown output.

Usage:
    python parse_site.py https://example.gov

Author: Municipal Parser System
Version: 1.0.0
"""

import sys
import subprocess
import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from urllib.parse import urlparse

try:
    from bs4 import BeautifulSoup
    import html2text
except ImportError:
    print("❌ Missing dependencies!")
    print("Please install: pip install beautifulsoup4 html2text lxml")
    sys.exit(1)

# Import layout templates
try:
    from templates.layouts import get_layout, DEFAULT_LAYOUT_MAP
except ImportError:
    # Fallback if templates not found
    def get_layout(page_name, layout_override=None):
        return lambda content, meta, data: content
    DEFAULT_LAYOUT_MAP = {}


# ============================================================================
# PROGRESS & DISPLAY FUNCTIONS
# ============================================================================

def show_progress(message: str, status: str = 'info') -> None:
    """
    Displays formatted progress messages to user.

    Args:
        message (str): Progress message to display
        status (str): Status type - 'info', 'success', 'warning', 'error'

    Returns:
        None (prints to stdout)

    Examples:
        show_progress("Downloading site...", "info")
        show_progress("Download complete", "success")
    """
    icons = {
        'info': '🔍',
        'success': '✅',
        'warning': '⚠️',
        'error': '❌',
        'progress': '📥',
        'file': '📄',
        'save': '💾'
    }
    icon = icons.get(status, '•')
    print(f"{icon} {message}")


def print_header():
    """Prints the application header with branding."""
    print("\n" + "=" * 50)
    print("🌐 Municipal Website Parser")
    print("=" * 50 + "\n")


def print_summary(data: Dict, file_count: int, output_dir: Path):
    """
    Prints a summary of the parsing operation.

    Args:
        data (Dict): Parsed data dictionary containing metadata and pages
        file_count (int): Number of HTML files parsed
        output_dir (Path): Output directory path
    """
    print("\n" + "=" * 50)
    print("✨ DONE!\n")
    print("📊 Summary:")
    print(f"   Municipality: {data['metadata'].get('municipality_name', 'Unknown')}")
    print(f"   Pages parsed: {file_count}")

    pages_mapped = sum(1 for page_data in data['pages'].values()
                       if isinstance(page_data, dict) and (page_data.get('content') or page_data.get('hero')))
    print(f"   Content mapped: {pages_mapped}/12 pages")
    print(f"   Output: {output_dir}/")
    print("=" * 50 + "\n")


# ============================================================================
# DOWNLOAD FUNCTIONS
# ============================================================================

def download_site(url: str, domain: str) -> bool:
    """
    Downloads entire website using wget with optimal flags.

    This function uses subprocess to execute wget with recursive download
    settings optimized for municipal websites. It handles the complete site
    mirroring process including converting links for offline browsing.

    Args:
        url (str): Full URL of the municipal website to download
        domain (str): Domain name for directory organization

    Returns:
        bool: True if download successful, False otherwise

    Implementation Details:
        - Uses subprocess to execute wget with recursive download
        - Stores files in ./downloads/{domain}/
        - Shows progress to user
        - Handles network errors and timeouts gracefully
        - Timeout: 10 seconds per request
        - Retries: 3 attempts per failed request

    Example:
        success = download_site("https://example.gov", "example.gov")
    """
    download_dir = Path(f"./downloads/{domain}")
    download_dir.mkdir(parents=True, exist_ok=True)

    show_progress(f"Downloading {url}...", "progress")

    # Check if wget is installed
    try:
        subprocess.run(['wget', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        show_progress("wget is not installed!", "error")
        print("\nPlease install wget:")
        print("  - Ubuntu/Debian: sudo apt-get install wget")
        print("  - macOS: brew install wget")
        print("  - Windows: download from https://eternallybored.org/misc/wget/")
        return False

    # Build wget command
    wget_cmd = [
        'wget',
        '--recursive',
        '--page-requisites',
        '--html-extension',
        '--convert-links',
        '--restrict-file-names=windows',
        f'--domains={domain}',
        '--no-parent',
        f'--directory-prefix=./downloads',
        '--timeout=10',
        '--tries=3',
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        '--quiet',  # Suppress verbose output
        '--show-progress',  # But show progress bar
        url
    ]

    try:
        result = subprocess.run(wget_cmd, capture_output=False, text=True)
        if result.returncode == 0:
            show_progress("Download complete", "success")
            return True
        else:
            show_progress(f"Download completed with warnings (exit code: {result.returncode})", "warning")
            return True  # Continue anyway, partial downloads can still be useful
    except subprocess.CalledProcessError as e:
        show_progress(f"Download failed: {e}", "error")
        return False
    except Exception as e:
        show_progress(f"Unexpected error during download: {e}", "error")
        return False


# ============================================================================
# FILE DISCOVERY FUNCTIONS
# ============================================================================

def find_html_files(download_path: str) -> List[Path]:
    """
    Recursively finds all HTML files in downloaded site.

    Args:
        download_path (str): Root directory to search for HTML files

    Returns:
        List[Path]: List of Path objects for all .html files found

    Example:
        html_files = find_html_files("./downloads/example.gov")
        # Returns: [Path("index.html"), Path("about.html"), ...]
    """
    path = Path(download_path)
    html_files = list(path.rglob("*.html")) + list(path.rglob("*.htm"))

    show_progress(f"Found {len(html_files)} HTML files", "file")
    return html_files


# ============================================================================
# EXTRACTION UTILITY FUNCTIONS
# ============================================================================

def extract_phone_numbers(text: str) -> List[str]:
    """
    Extracts phone numbers from text using regex.

    Args:
        text (str): Text to search for phone numbers

    Returns:
        List[str]: List of found phone numbers

    Supported Formats:
        - (555) 123-4567
        - 555-123-4567
        - 555.123.4567
        - 5551234567

    Example:
        phones = extract_phone_numbers("Call us at (717) 259-0965")
        # Returns: ["(717) 259-0965"]
    """
    pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    return re.findall(pattern, text)


def extract_emails(text: str) -> List[str]:
    """
    Extracts email addresses from text.

    Args:
        text (str): Text to search for emails

    Returns:
        List[str]: List of found email addresses

    Example:
        emails = extract_emails("Contact: info@example.gov")
        # Returns: ["info@example.gov"]
    """
    pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    return re.findall(pattern, text)


def extract_dates(text: str) -> List[str]:
    """
    Extracts dates from text in various formats.

    Args:
        text (str): Text to search for dates

    Returns:
        List[str]: List of found dates

    Supported Formats:
        - MM/DD/YYYY
        - January 15, 2024
        - Jan 15, 2024
        - 01-15-2024
        - 2024-01-15

    Example:
        dates = extract_dates("Meeting on January 15, 2024")
        # Returns: ["January 15, 2024"]
    """
    patterns = [
        r'\d{1,2}/\d{1,2}/\d{4}',  # MM/DD/YYYY
        r'\d{1,2}-\d{1,2}-\d{4}',  # MM-DD-YYYY
        r'\d{4}-\d{1,2}-\d{1,2}',  # YYYY-MM-DD
        r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}',
        r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4}'
    ]

    dates = []
    for pattern in patterns:
        dates.extend(re.findall(pattern, text))
    return dates


# ============================================================================
# CONTENT CLEANING FUNCTIONS
# ============================================================================

def clean_html_content(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Removes navigation, headers, footers, and other non-content elements.

    This function strips away all the structural and navigational elements
    of a webpage, leaving only the main content that should be converted
    to markdown.

    Args:
        soup (BeautifulSoup): BeautifulSoup object to clean

    Returns:
        BeautifulSoup: Cleaned soup object with only main content

    Removes:
        - Navigation menus (<nav>, multi-link menus)
        - Site headers (logo/nav)
        - Footers (copyright, bottom links)
        - Sidebars (elements with "sidebar" in class)
        - Breadcrumbs, share widgets, social embeds
        - Cookie notices, search forms
        - Scripts and styles

    Preserves:
        - Main content text, headings (h1-h6)
        - Paragraphs, lists (ul, ol), tables
        - Images (src + alt), links (href + text)

    Example:
        cleaned_soup = clean_html_content(soup)
    """
    # Elements to remove by tag
    for tag in soup.find_all(['script', 'style', 'nav', 'header', 'footer', 'iframe', 'noscript']):
        tag.decompose()

    # Remove elements by common class/id patterns
    remove_patterns = [
        'nav', 'menu', 'sidebar', 'side-bar', 'breadcrumb', 'breadcrumbs',
        'cookie', 'popup', 'modal', 'advertisement', 'ad-', 'ads-',
        'share', 'social', 'follow', 'newsletter', 'subscription',
        'search', 'login', 'signup', 'header', 'footer'
    ]

    for element in soup.find_all(True):  # Find all tags
        # Skip elements without attributes (like NavigableString, Comment, etc.)
        if not hasattr(element, 'attrs') or element.attrs is None:
            continue

        class_str = ' '.join(element.get('class', [])).lower()
        id_str = element.get('id', '').lower()

        for pattern in remove_patterns:
            if pattern in class_str or pattern in id_str:
                element.decompose()
                break

    return soup


def convert_to_markdown(html_content: str) -> str:
    """
    Converts cleaned HTML to well-formatted markdown.

    Args:
        html_content (str): Clean HTML content string

    Returns:
        str: Markdown formatted content

    Processing:
        - Uses html2text library
        - Preserves heading hierarchy and lists
        - Maintains link structure
        - Cleans extra whitespace
        - Removes HTML attributes

    Example:
        markdown = convert_to_markdown("<h1>Title</h1><p>Content</p>")
        # Returns: "# Title\n\nContent"
    """
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.ignore_emphasis = False
    h.body_width = 0  # Don't wrap lines
    h.single_line_break = False

    markdown = h.handle(html_content)

    # Clean up excessive whitespace
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)
    markdown = markdown.strip()

    return markdown


# ============================================================================
# PAGE TYPE DETECTION
# ============================================================================

def detect_page_type(filename: str, title: str, content: str) -> str:
    """
    Identifies page type using multiple heuristics.

    Uses filename, page title, and content keywords to intelligently
    determine what type of page this is in the municipal site structure.

    Args:
        filename (str): HTML filename
        title (str): Page title from <title> tag
        content (str): Page content text

    Returns:
        str: Page type (home, about, government, departments, services,
             news, events, contact, documents, employment, faqs, accessibility)

    Detection Methods:
        - Filename matching (index.html → home, about.html → about)
        - URL path patterns (/about, /contact, /services)
        - Title keyword matching ("About Us", "Contact", etc.)
        - Content keyword analysis

    Example:
        page_type = detect_page_type("about.html", "About Us", "Our history...")
        # Returns: "about"
    """
    filename_lower = filename.lower()
    title_lower = title.lower()
    content_lower = content.lower()

    # Filename-based detection (most reliable)
    if 'index' in filename_lower or filename_lower == 'home.html':
        return 'home'
    elif 'about' in filename_lower:
        return 'about'
    elif 'government' in filename_lower or 'mayor' in filename_lower or 'council' in filename_lower:
        return 'government'
    elif 'department' in filename_lower:
        return 'departments'
    elif 'service' in filename_lower or 'permit' in filename_lower:
        return 'services'
    elif 'news' in filename_lower or 'announcement' in filename_lower:
        return 'news'
    elif 'event' in filename_lower or 'calendar' in filename_lower:
        return 'events'
    elif 'contact' in filename_lower:
        return 'contact'
    elif 'document' in filename_lower or 'form' in filename_lower:
        return 'documents'
    elif 'job' in filename_lower or 'employ' in filename_lower or 'career' in filename_lower:
        return 'employment'
    elif 'faq' in filename_lower:
        return 'faqs'
    elif 'accessibility' in filename_lower or 'ada' in filename_lower:
        return 'accessibility'

    # Title-based detection
    if 'about' in title_lower:
        return 'about'
    elif 'government' in title_lower or 'mayor' in title_lower or 'council' in title_lower:
        return 'government'
    elif 'department' in title_lower:
        return 'departments'
    elif 'service' in title_lower:
        return 'services'
    elif 'news' in title_lower:
        return 'news'
    elif 'event' in title_lower or 'calendar' in title_lower:
        return 'events'
    elif 'contact' in title_lower:
        return 'contact'
    elif 'document' in title_lower or 'form' in title_lower:
        return 'documents'
    elif 'employment' in title_lower or 'job' in title_lower or 'career' in title_lower:
        return 'employment'
    elif 'faq' in title_lower or 'question' in title_lower:
        return 'faqs'
    elif 'accessibility' in title_lower:
        return 'accessibility'

    # Content-based detection (least reliable, for fallback)
    # Look for concentration of keywords
    keyword_counts = {
        'government': content_lower.count('mayor') + content_lower.count('council') + content_lower.count('borough'),
        'services': content_lower.count('permit') + content_lower.count('license') + content_lower.count('utility'),
        'news': content_lower.count('news') + content_lower.count('announcement'),
        'events': content_lower.count('event') + content_lower.count('meeting'),
        'contact': content_lower.count('phone') + content_lower.count('email') + content_lower.count('address'),
    }

    max_type = max(keyword_counts, key=keyword_counts.get)
    if keyword_counts[max_type] > 3:
        return max_type

    return 'additional_content'


# ============================================================================
# PARSING FUNCTIONS
# ============================================================================

def parse_html_file(file_path: Path) -> Dict:
    """
    Parses individual HTML file and extracts content.

    Args:
        file_path (Path): Path to HTML file to parse

    Returns:
        Dict: Dictionary containing page type, content, and metadata

    Implementation Details:
        - Loads file with BeautifulSoup
        - Identifies page type based on filename, title, and content keywords
        - Extracts main content (removes nav, footer, sidebar, scripts)
        - Converts to markdown with html2text

    Example:
        page_data = parse_html_file(Path("about.html"))
        # Returns: {"type": "about", "content": "# About...", ...}
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            html_content = f.read()
    except Exception as e:
        show_progress(f"Error reading {file_path.name}: {e}", "error")
        return {}

    soup = BeautifulSoup(html_content, 'lxml')

    # Extract title
    title_tag = soup.find('title')
    title = title_tag.get_text(strip=True) if title_tag else ''

    # Clean content
    cleaned_soup = clean_html_content(soup)

    # Get text content for analysis
    text_content = cleaned_soup.get_text(separator=' ', strip=True)

    # Detect page type
    page_type = detect_page_type(file_path.name, title, text_content)

    # Convert to markdown
    markdown_content = convert_to_markdown(str(cleaned_soup))

    return {
        'type': page_type,
        'title': title,
        'content': markdown_content,
        'file_path': str(file_path),
        'text_content': text_content  # For metadata extraction
    }


def extract_metadata(html_files: List[Path]) -> Dict:
    """
    Extracts site-wide metadata from all HTML files.

    Analyzes all HTML files to find common metadata like municipality name,
    logo, contact information, and branding colors.

    Args:
        html_files (List[Path]): List of HTML files to analyze

    Returns:
        Dict: Metadata including municipality name, logo, contact info, social media links

    Extraction Patterns:
        - Municipality name: from title, h1, header tags
        - Logo URL: img tags with "logo" in src/alt attributes
        - Phone: regex pattern for US phone numbers
        - Email: standard email regex
        - Address: street address patterns with city, state, zip
        - Office hours: "Monday-Friday" time patterns
        - Social media: links to facebook.com, twitter.com, etc.
        - Primary color: from CSS or default to #0A2463

    Example:
        metadata = extract_metadata([Path("index.html"), Path("about.html")])
    """
    all_text = ""
    municipality_names = []
    logo_url = None
    phones = []
    emails = []
    addresses = []
    social_media = {}

    for file_path in html_files[:5]:  # Check first 5 files for metadata
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                html = f.read()

            soup = BeautifulSoup(html, 'lxml')
            all_text += soup.get_text(separator=' ', strip=True) + " "

            # Extract municipality name from title
            title = soup.find('title')
            if title:
                title_text = title.get_text(strip=True)
                # Remove common suffixes
                name = re.sub(r'\s*[-|]\s*(Home|Welcome|Official Site).*$', '', title_text, flags=re.IGNORECASE)
                municipality_names.append(name)

            # Find logo
            if not logo_url:
                for img in soup.find_all('img'):
                    src = img.get('src', '')
                    alt = img.get('alt', '')
                    if 'logo' in src.lower() or 'logo' in alt.lower():
                        logo_url = src
                        break

            # Find social media links
            for link in soup.find_all('a', href=True):
                href = link['href']
                if 'facebook.com' in href:
                    social_media['facebook'] = href
                elif 'twitter.com' in href:
                    social_media['twitter'] = href
                elif 'instagram.com' in href:
                    social_media['instagram'] = href
                elif 'youtube.com' in href:
                    social_media['youtube'] = href

        except Exception:
            continue

    # Extract contact info from combined text
    phones = extract_phone_numbers(all_text)
    emails = extract_emails(all_text)

    # Find address (simplified pattern)
    address_pattern = r'\d+\s+[\w\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Court|Ct|Place|Pl),?\s+[\w\s]+,\s+[A-Z]{2}\s+\d{5}'
    addresses = re.findall(address_pattern, all_text)

    # Find office hours
    hours_pattern = r'(Monday|Mon).*?(Friday|Fri).*?\d{1,2}:\d{2}\s*(?:AM|PM).*?\d{1,2}:\d{2}\s*(?:AM|PM)'
    hours_match = re.search(hours_pattern, all_text, re.IGNORECASE | re.DOTALL)
    office_hours = hours_match.group(0) if hours_match else ""

    # Determine municipality name (most common)
    municipality_name = municipality_names[0] if municipality_names else "Unknown Municipality"

    return {
        'municipality_name': municipality_name,
        'logo_url': logo_url or '',
        'primary_color': '#0A2463',  # Default color
        'contact': {
            'phone': phones[0] if phones else '',
            'email': emails[0] if emails else '',
            'address': addresses[0] if addresses else '',
            'hours': office_hours.strip() if office_hours else ''
        },
        'social_media': social_media
    }


# ============================================================================
# CONTENT MAPPING FUNCTIONS
# ============================================================================

def map_content_to_pages(parsed_files: List[Dict]) -> Dict:
    """
    Intelligently maps parsed content to 12-page structure.

    Takes all parsed HTML files and organizes them into the standardized
    12-page municipal website structure. Handles multiple files mapping to
    the same page type by combining content.

    Args:
        parsed_files (List[Dict]): List of parsed HTML file dictionaries

    Returns:
        Dict: Content organized into 12 page categories (home, about, government,
              departments, services, news, events, contact, documents,
              employment, faqs, accessibility)

    Example:
        pages = map_content_to_pages(parsed_files)
    """
    pages = {
        'home': {'content': '', 'hero': {}, 'events': [], 'news': []},
        'about': {'content': ''},
        'government': {'content': ''},
        'departments': {'content': ''},
        'services': {'content': ''},
        'news': {'content': ''},
        'events': {'content': ''},
        'contact': {'content': ''},
        'documents': {'content': ''},
        'employment': {'content': ''},
        'faqs': {'content': ''},
        'accessibility': {'content': ''},
        'additional_content': []
    }

    for parsed in parsed_files:
        page_type = parsed.get('type', 'additional_content')
        content = parsed.get('content', '')
        title = parsed.get('title', '')

        if page_type == 'additional_content':
            pages['additional_content'].append({
                'title': title,
                'content': content,
                'file': parsed.get('file_path', '')
            })
        elif page_type == 'home':
            # For home page, try to extract structured content
            pages['home']['content'] = content
            pages['home']['hero']['title'] = title

            # Extract events from content
            text = parsed.get('text_content', '')
            dates = extract_dates(text)
            if dates:
                # Simple event extraction
                for date in dates[:5]:  # Max 5 events
                    pages['home']['events'].append({'date': date, 'title': 'Event'})
        else:
            # For other pages, append content (in case multiple files map to same type)
            if pages[page_type]['content']:
                pages[page_type]['content'] += '\n\n---\n\n' + content
            else:
                pages[page_type]['content'] = content

    return pages


# ============================================================================
# OUTPUT GENERATION
# ============================================================================

def markdown_to_html(markdown_text: str) -> str:
    """
    Converts markdown text to HTML.

    Uses html2text in reverse - we'll use a simple markdown-to-HTML converter.
    For now, we'll handle basic markdown syntax.

    Args:
        markdown_text (str): Markdown formatted text

    Returns:
        str: HTML formatted content
    """
    # Try to use markdown library if available, otherwise do basic conversion
    try:
        import markdown
        return markdown.markdown(markdown_text, extensions=['extra', 'nl2br'])
    except ImportError:
        # Basic markdown conversion (fallback)
        html = markdown_text

        # Headers
        html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)

        # Bold and italic
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)

        # Links
        html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)

        # Images
        html = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1">', html)

        # Paragraphs (double newline = new paragraph)
        paragraphs = html.split('\n\n')
        html = ''.join([f'<p>{p}</p>\n' if p.strip() and not p.strip().startswith('<') else p + '\n' for p in paragraphs])

        # Lists (basic)
        html = re.sub(r'^\* (.*?)$', r'<li>\1</li>', html, flags=re.MULTILINE)
        html = re.sub(r'(<li>.*?</li>\n)+', r'<ul>\n\g<0></ul>\n', html, flags=re.DOTALL)

        return html


def generate_html_page(page_name: str, content: str, metadata: Dict, pages: Dict) -> str:
    """
    Generates a complete HTML page with navigation and styling.

    Args:
        page_name (str): Name of the page (home, about, etc.)
        content (str): Markdown content for the page
        metadata (Dict): Site metadata
        pages (Dict): All pages data for navigation

    Returns:
        str: Complete HTML page
    """
    # Convert markdown to HTML
    html_content = markdown_to_html(content) if content else f"<p><em>No content available for this page.</em></p>"

    # Apply layout template
    page_data = pages.get(page_name, {})
    layout_func = get_layout(page_name)
    html_content = layout_func(html_content, metadata, page_data)

    # Get current layout key for switcher
    current_layout = DEFAULT_LAYOUT_MAP.get(page_name, 'a')

    # Page display names
    page_titles = {
        'home': 'Home',
        'about': 'About',
        'government': 'Government',
        'departments': 'Departments',
        'services': 'Services',
        'news': 'News',
        'events': 'Events',
        'contact': 'Contact',
        'documents': 'Documents',
        'employment': 'Employment',
        'faqs': 'FAQs',
        'accessibility': 'Accessibility'
    }

    page_title = page_titles.get(page_name, page_name.title())
    site_name = metadata.get('municipality_name', 'Municipal Website')

    # Build navigation menu
    nav_items = []
    for nav_page in page_titles.keys():
        active_class = ' class="active"' if nav_page == page_name else ''
        nav_items.append(f'                <li><a href="{nav_page}.html"{active_class}>{page_titles[nav_page]}</a></li>')

    nav_html = '\n'.join(nav_items)

    # Social media links
    social_media = metadata.get('social_media', {})
    social_links = []
    if social_media.get('facebook'):
        social_links.append(f'<a href="{social_media["facebook"]}" target="_blank">Facebook</a>')
    if social_media.get('twitter'):
        social_links.append(f'<a href="{social_media["twitter"]}" target="_blank">Twitter</a>')
    if social_media.get('instagram'):
        social_links.append(f'<a href="{social_media["instagram"]}" target="_blank">Instagram</a>')

    social_html = '\n                '.join(social_links) if social_links else ''

    # Contact info
    contact = metadata.get('contact', {})
    contact_html = f"""
                <div class="footer-section">
                    <h4>Contact Information</h4>
                    {f'<p>{contact.get("phone", "")}</p>' if contact.get('phone') else ''}
                    {f'<p><a href="mailto:{contact.get("email", "")}">{contact.get("email", "")}</a></p>' if contact.get('email') else ''}
                    {f'<p>{contact.get("address", "")}</p>' if contact.get('address') else ''}
                </div>
    """ if contact.get('phone') or contact.get('email') or contact.get('address') else ''

    hours_html = f"""
                <div class="footer-section">
                    <h4>Office Hours</h4>
                    <p>{contact.get('hours', '')}</p>
                </div>
    """ if contact.get('hours') else ''

    # Layout switcher UI
    layout_switcher = f'''
    <div class="layout-switcher">
        <h4>View Layout:</h4>
        <div class="layout-buttons">
            <button class="layout-btn {'active' if current_layout == 'a' else ''}" data-layout="a" onclick="switchLayout('a')">A</button>
            <button class="layout-btn {'active' if current_layout == 'b' else ''}" data-layout="b" onclick="switchLayout('b')">B</button>
            <button class="layout-btn {'active' if current_layout == 'c' else ''}" data-layout="c" onclick="switchLayout('c')">C</button>
            <button class="layout-btn {'active' if current_layout == 'd' else ''}" data-layout="d" onclick="switchLayout('d')">D</button>
            <button class="layout-btn {'active' if current_layout == 'e' else ''}" data-layout="e" onclick="switchLayout('e')">E</button>
        </div>
    </div>'''

    # Complete HTML template
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title} - {site_name}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body data-page="{page_name}" data-layout="{current_layout}">
    <header>
        <div class="header-content">
            <div class="site-title">
                {f'<img src="{metadata.get("logo_url", "")}" alt="Logo" class="logo">' if metadata.get('logo_url') else ''}
                <h1>{site_name}</h1>
            </div>
        </div>
    </header>

    <nav>
        <ul>
{nav_html}
        </ul>
    </nav>

    <main>
        <div class="content">
{html_content}
        </div>
    </main>

    <footer>
        <div class="footer-content">
            <div class="footer-info">
{contact_html}
{hours_html}
            </div>

            {f'<div class="social-media">{social_html}</div>' if social_html else ''}

            <div class="copyright">
                <p>&copy; {datetime.now().year} {site_name}. All rights reserved.</p>
                <p style="font-size: 0.8rem; margin-top: 0.5rem; opacity: 0.7;">Generated by Municipal Website Parser • Layout: {current_layout.upper()}</p>
            </div>
        </div>
    </footer>

{layout_switcher}

    <script src="layout_switcher.js"></script>
</body>
</html>"""

    return html


def generate_output_files(data: Dict, output_dir: Path) -> None:
    """
    Generates complete HTML website with navigation and styling.

    Creates a browsable HTML website with all pages, navigation menu,
    styling, and the original JSON data file.

    Args:
        data (Dict): Complete parsed and mapped data
        output_dir (Path): Directory to save output files

    Generates:
        - {domain}-parsed.json - Complete structured data
        - 12 individual HTML files (home.html, about.html, etc.)
        - style.css - Website styling
        - index.html - Redirect to home.html

    Example:
        generate_output_files(data, Path("./output/example.gov"))
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    show_progress("Generating output files...", "save")

    # Generate JSON file
    domain = data['metadata'].get('source_url', 'unknown').replace('https://', '').replace('http://', '').replace('/', '-')
    json_file = output_dir / f"{domain}-parsed.json"

    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    show_progress(f"✓ {json_file.name}", "success")

    # Copy CSS and JS files to output directory
    script_dir = Path(__file__).parent
    import shutil

    # Copy CSS
    css_source = script_dir / "templates" / "style.css"
    css_dest = output_dir / "style.css"
    if css_source.exists():
        shutil.copy(css_source, css_dest)
        show_progress(f"✓ style.css", "success")
    else:
        show_progress(f"⚠️  CSS file not found at {css_source}", "warning")

    # Copy JavaScript
    js_source = script_dir / "templates" / "layout_switcher.js"
    js_dest = output_dir / "layout_switcher.js"
    if js_source.exists():
        shutil.copy(js_source, js_dest)
        show_progress(f"✓ layout_switcher.js", "success")
    else:
        show_progress(f"⚠️  JS file not found at {js_source}", "warning")

    # Generate individual HTML files
    page_names = ['home', 'about', 'government', 'departments', 'services',
                  'news', 'events', 'contact', 'documents', 'employment',
                  'faqs', 'accessibility']

    for page_name in page_names:
        html_file = output_dir / f"{page_name}.html"
        page_data = data['pages'].get(page_name, {})
        content = page_data.get('content', '')

        if not content:
            content = f"# {page_name.title()}\n\n*No content found for this page.*"

        # Generate complete HTML page
        html_content = generate_html_page(page_name, content, data['metadata'], data['pages'])

        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        show_progress(f"✓ {html_file.name}", "success")

    # Create index.html that redirects to home.html
    index_html = output_dir / "index.html"
    with open(index_html, 'w', encoding='utf-8') as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0; url=home.html">
    <title>Redirecting...</title>
</head>
<body>
    <p>Redirecting to <a href="home.html">home page</a>...</p>
</body>
</html>""")
    show_progress(f"✓ index.html (redirect)", "success")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main execution function that orchestrates the entire parsing process.

    Workflow:
        1. Validate command line arguments
        2. Download website with wget
        3. Find all HTML files
        4. Parse each file
        5. Extract metadata
        6. Map content to 12-page structure
        7. Generate output files
        8. Display summary
    """
    print_header()

    # Check arguments
    if len(sys.argv) < 2:
        print("Usage: python parse_site.py <url>")
        print("\nExample:")
        print("  python parse_site.py https://abbottstown.comcastbiz.net")
        sys.exit(1)

    url = sys.argv[1]

    # Parse domain from URL
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    if not domain:
        show_progress("Invalid URL provided", "error")
        sys.exit(1)

    # Step 1: Download site
    if not download_site(url, domain):
        show_progress("Failed to download site. Exiting.", "error")
        sys.exit(1)

    # Step 2: Find HTML files
    download_path = f"./downloads/{domain}"
    html_files = find_html_files(download_path)

    if not html_files:
        show_progress("No HTML files found in downloaded content", "error")
        sys.exit(1)

    # Step 3: Parse HTML files
    show_progress("Parsing content...", "progress")
    parsed_files = []
    for html_file in html_files:
        parsed = parse_html_file(html_file)
        if parsed:
            parsed_files.append(parsed)
            show_progress(f"✓ Parsed {html_file.name} ({parsed.get('type', 'unknown')})", "success")

    # Step 4: Extract metadata
    show_progress("Extracting metadata...", "progress")
    metadata = extract_metadata(html_files)
    metadata['source_url'] = url
    metadata['parsed_at'] = datetime.now().isoformat()
    show_progress(f"✓ Found municipality: {metadata['municipality_name']}", "success")

    # Step 5: Map content to pages
    show_progress("Mapping content to pages...", "progress")
    pages = map_content_to_pages(parsed_files)

    # Step 6: Build complete data structure
    data = {
        'metadata': metadata,
        'pages': pages
    }

    # Step 7: Generate output files
    output_dir = Path(f"./output/{domain}")
    generate_output_files(data, output_dir)

    # Step 8: Print summary
    print_summary(data, len(html_files), output_dir)

    # Show warnings for missing pages
    warnings = []
    for page_name in ['employment', 'faqs', 'accessibility']:
        if not pages[page_name]['content']:
            warnings.append(f"- No {page_name} page found")

    if warnings:
        print("⚠️  Warnings:")
        for warning in warnings:
            print(f"   {warning}")
        print()

    print("🎯 Next steps:")
    print("   1. Review JSON file for accuracy")
    print("   2. Edit markdown files as needed")
    print("   3. Deploy to platform\n")


if __name__ == '__main__':
    main()
