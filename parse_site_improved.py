#!/usr/bin/env python3
"""
Municipal Website Parser & Converter (Improved)
================================================
Automatically downloads OR parses local municipal websites into a
structured 12-page format with clean output and layouts.

Usage:
    python parse_site_improved.py

Author: Municipal Parser System
Version: 2.0.0
"""

import sys
import subprocess
import json
import re
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from urllib.parse import urlparse, urljoin

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
    """Displays formatted progress messages to user."""
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
    print("\n" + "=" * 60)
    print("🌐 Municipal Website Parser v2.0")
    print("=" * 60 + "\n")


def print_summary(data: Dict, file_count: int, output_dir: Path, image_count: int = 0):
    """Prints a summary of the parsing operation."""
    print("\n" + "=" * 60)
    print("✨ DONE!\n")
    print("📊 Summary:")
    print(f"   Municipality: {data['metadata'].get('municipality_name', 'Unknown')}")
    print(f"   HTML files parsed: {file_count}")
    print(f"   Images downloaded: {image_count}")

    pages_mapped = sum(1 for page_data in data['pages'].values()
                       if isinstance(page_data, dict) and page_data.get('content'))
    print(f"   Content mapped: {pages_mapped}/12 pages")
    print(f"   Output: {output_dir}/")
    print("=" * 60 + "\n")


# ============================================================================
# MODE SELECTION
# ============================================================================

def get_mode_and_path() -> Tuple[str, str, str]:
    """
    Asks user whether to download or parse local folder.

    Returns:
        Tuple of (mode, path, domain)
        mode: 'download' or 'local'
        path: URL or local folder path
        domain: domain name for organization
    """
    print("Choose parsing mode:\n")
    print("1. Download website from URL (uses wget)")
    print("2. Parse existing local website folder\n")

    while True:
        choice = input("Enter choice (1 or 2): ").strip()

        if choice == '1':
            url = input("\nEnter website URL (e.g., https://example.gov): ").strip()
            if not url:
                print("❌ URL cannot be empty!")
                continue

            parsed_url = urlparse(url)
            domain = parsed_url.netloc

            if not domain:
                print("❌ Invalid URL!")
                continue

            return ('download', url, domain)

        elif choice == '2':
            folder_path = input("\nEnter local folder path (e.g., ./www.abbottstownborough.com): ").strip()
            if not folder_path:
                print("❌ Path cannot be empty!")
                continue

            path = Path(folder_path)
            if not path.exists():
                print(f"❌ Folder not found: {folder_path}")
                continue

            if not path.is_dir():
                print(f"❌ Not a directory: {folder_path}")
                continue

            # Use folder name as domain
            domain = path.name
            return ('local', str(path), domain)

        else:
            print("❌ Invalid choice! Please enter 1 or 2.")


# ============================================================================
# DOWNLOAD FUNCTIONS
# ============================================================================

def download_site(url: str, domain: str) -> bool:
    """Downloads entire website using wget."""
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
        '--user-agent=Mozilla/5.0',
        '--quiet',
        '--show-progress',
        url
    ]

    try:
        result = subprocess.run(wget_cmd, capture_output=False, text=True)
        if result.returncode == 0:
            show_progress("Download complete", "success")
            return True
        else:
            show_progress(f"Download completed with warnings", "warning")
            return True
    except Exception as e:
        show_progress(f"Download failed: {e}", "error")
        return False


# ============================================================================
# FILE DISCOVERY FUNCTIONS
# ============================================================================

def find_html_files(download_path: str) -> List[Path]:
    """Recursively finds all HTML files in directory."""
    path = Path(download_path)
    html_files = list(path.rglob("*.html")) + list(path.rglob("*.htm"))

    show_progress(f"Found {len(html_files)} HTML files", "file")
    return html_files


# ============================================================================
# IMAGE HANDLING
# ============================================================================

def download_local_images(source_folder: Path, output_dir: Path, html_files: List[Path]) -> int:
    """
    Finds and copies images from local source to output.

    Args:
        source_folder: Root folder of website
        output_dir: Output directory
        html_files: List of HTML files to scan for images

    Returns:
        Number of images copied
    """
    images_dir = output_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    image_count = 0
    copied_images = set()

    # Common image extensions
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.ico'}

    # Find all images in getmedia and other folders
    for img_path in source_folder.rglob('*'):
        if img_path.is_file() and img_path.suffix.lower() in image_extensions:
            # Copy to output/images/ with relative path preserved
            relative_path = img_path.relative_to(source_folder)
            dest_path = images_dir / relative_path.name

            # Avoid duplicates
            if dest_path.name not in copied_images:
                try:
                    shutil.copy2(img_path, dest_path)
                    copied_images.add(dest_path.name)
                    image_count += 1
                except Exception as e:
                    show_progress(f"Failed to copy {img_path.name}: {e}", "warning")

    show_progress(f"Copied {image_count} images", "success")
    return image_count


def fix_image_paths(html_content: str, soup: BeautifulSoup) -> str:
    """
    Fixes image paths to point to local images/ folder.

    Args:
        html_content: Original HTML content
        soup: BeautifulSoup object

    Returns:
        HTML with fixed image paths
    """
    for img in soup.find_all('img'):
        src = img.get('src', '')
        if src:
            # Extract filename from path
            if 'getmedia' in src or '/' in src:
                filename = Path(src).name
                # Remove query parameters
                filename = filename.split('?')[0]
                img['src'] = f'images/{filename}'

    return str(soup)


# ============================================================================
# CONTENT EXTRACTION
# ============================================================================

def extract_main_content(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Extracts main content from <main> tag, removing nav/footer/scripts.

    Args:
        soup: BeautifulSoup object

    Returns:
        BeautifulSoup with only main content
    """
    # Try to find main content area
    main_content = soup.find('main', id='main')
    if not main_content:
        main_content = soup.find('main')
    if not main_content:
        main_content = soup.find('div', class_='contentWrapper')
    if not main_content:
        main_content = soup.find('body')

    # Create new soup with just main content
    if main_content:
        content_soup = BeautifulSoup(str(main_content), 'lxml')
    else:
        content_soup = soup

    # Remove unwanted elements
    for tag in content_soup.find_all(['script', 'style', 'nav', 'header', 'footer',
                                       'iframe', 'noscript']):
        tag.decompose()

    # Remove elements by class/id patterns
    remove_patterns = [
        'nav', 'menu', 'sidebar', 'breadcrumb', 'cookie', 'popup', 'modal',
        'advertisement', 'ad-', 'share', 'social', 'search', 'login', 'signup',
        'navbar', 'toggler', 'utilityBar', 'alertBar'
    ]

    for element in content_soup.find_all(True):
        if not hasattr(element, 'attrs'):
            continue

        class_str = ' '.join(element.get('class', [])).lower()
        id_str = element.get('id', '').lower()

        for pattern in remove_patterns:
            if pattern in class_str or pattern in id_str:
                element.decompose()
                break

    return content_soup


def clean_html_content(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Cleans HTML content while preserving structure.

    Args:
        soup: BeautifulSoup object

    Returns:
        Cleaned BeautifulSoup object
    """
    # First extract main content
    cleaned_soup = extract_main_content(soup)

    # Remove empty tags
    for tag in cleaned_soup.find_all():
        if len(tag.get_text(strip=True)) == 0 and tag.name not in ['br', 'hr', 'img']:
            tag.decompose()

    return cleaned_soup


def extract_footer_metadata(soup: BeautifulSoup) -> Dict:
    """
    Extracts contact info and metadata from footer.

    Args:
        soup: BeautifulSoup object

    Returns:
        Dictionary with contact information
    """
    metadata = {
        'phone': '',
        'fax': '',
        'email': '',
        'address': '',
        'hours': ''
    }

    # Find footer
    footer = soup.find('footer', id='footer')
    if not footer:
        footer = soup.find('footer')

    if footer:
        footer_text = footer.get_text()

        # Extract phone
        phone_pattern = r'Phone:\s*([\d\-\(\) ]+)'
        phone_match = re.search(phone_pattern, footer_text)
        if phone_match:
            metadata['phone'] = phone_match.group(1).strip()

        # Extract fax
        fax_pattern = r'Fax:\s*([\d\-\(\) ]+)'
        fax_match = re.search(fax_pattern, footer_text)
        if fax_match:
            metadata['fax'] = fax_match.group(1).strip()

        # Extract email
        email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
        email_match = re.search(email_pattern, footer_text)
        if email_match:
            metadata['email'] = email_match.group(0)

        # Extract address (simple pattern)
        address_pattern = r'(\d+\s+[\w\s]+(?:Street|St|Avenue|Ave|Road|Rd).*?PA\s+\d{5})'
        address_match = re.search(address_pattern, footer_text, re.IGNORECASE)
        if address_match:
            metadata['address'] = address_match.group(1).strip()

        # Extract office hours
        hours_pattern = r'(Monday.*?(?:AM|PM))'
        hours_match = re.search(hours_pattern, footer_text, re.IGNORECASE | re.DOTALL)
        if hours_match:
            hours_text = hours_match.group(1).strip()
            # Clean up
            hours_text = re.sub(r'\s+', ' ', hours_text)
            if len(hours_text) < 200:  # Sanity check
                metadata['hours'] = hours_text

    return metadata


# ============================================================================
# CONTENT CONVERSION
# ============================================================================

def convert_to_markdown(html_content: str) -> str:
    """Converts HTML to clean markdown."""
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.ignore_emphasis = False
    h.body_width = 0
    h.single_line_break = False

    markdown = h.handle(html_content)

    # Clean up excessive whitespace
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)
    markdown = markdown.strip()

    return markdown


# ============================================================================
# PAGE TYPE DETECTION
# ============================================================================

def detect_page_type(filename: str, title: str, content: str, file_path: Path) -> str:
    """
    Identifies page type using filename, title, and content.

    Args:
        filename: HTML filename
        title: Page title
        content: Page content
        file_path: Full path to file

    Returns:
        Page type string
    """
    filename_lower = filename.lower()
    title_lower = title.lower()
    content_lower = content.lower()
    path_str = str(file_path).lower()

    # Check path for better detection
    if '/home/news/' in path_str or 'home/news' in path_str:
        return 'news'

    # Filename-based detection
    if 'index' in filename_lower or filename_lower == 'home.html':
        return 'home'
    elif 'news' in filename_lower:
        return 'news'
    elif 'contact' in filename_lower:
        return 'contact'
    elif 'calendar' in filename_lower or 'event' in filename_lower:
        return 'events'
    elif 'document' in filename_lower or 'form' in filename_lower:
        return 'documents'
    elif 'official' in filename_lower or 'committee' in filename_lower:
        return 'government'
    elif 'meeting' in filename_lower:
        return 'events'
    elif 'ordinance' in filename_lower or 'resolution' in filename_lower or 'plan' in filename_lower:
        return 'documents'
    elif 'waste' in filename_lower or 'service' in filename_lower:
        return 'services'
    elif 'resident' in filename_lower or 'welcome' in filename_lower:
        return 'about'
    elif 'financial' in filename_lower or 'budget' in filename_lower:
        return 'documents'
    elif 'emergency' in filename_lower:
        return 'services'
    elif 'right-to-know' in filename_lower:
        return 'documents'

    # Title-based detection
    if 'contact' in title_lower:
        return 'contact'
    elif 'news' in title_lower or 'announcement' in title_lower:
        return 'news'
    elif 'event' in title_lower or 'calendar' in title_lower:
        return 'events'
    elif 'document' in title_lower:
        return 'documents'
    elif 'official' in title_lower or 'government' in title_lower:
        return 'government'

    return 'additional_content'


# ============================================================================
# PARSING FUNCTIONS
# ============================================================================

def parse_html_file(file_path: Path) -> Dict:
    """
    Parses individual HTML file and extracts content.

    Args:
        file_path: Path to HTML file

    Returns:
        Dictionary with page data
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

    # Fix image paths
    cleaned_html = fix_image_paths(str(cleaned_soup), cleaned_soup)
    cleaned_soup = BeautifulSoup(cleaned_html, 'lxml')

    # Get text content for analysis
    text_content = cleaned_soup.get_text(separator=' ', strip=True)

    # Detect page type
    page_type = detect_page_type(file_path.name, title, text_content, file_path)

    # Convert to markdown
    markdown_content = convert_to_markdown(str(cleaned_soup))

    return {
        'type': page_type,
        'title': title,
        'content': markdown_content,
        'file_path': str(file_path),
        'text_content': text_content
    }


def extract_metadata(html_files: List[Path], source_folder: Path) -> Dict:
    """
    Extracts site-wide metadata from HTML files.

    Args:
        html_files: List of HTML files
        source_folder: Root folder of website

    Returns:
        Metadata dictionary
    """
    municipality_name = "Unknown Municipality"
    logo_url = None
    contact_info = {}

    # Try to read index.html for main metadata
    index_file = source_folder / 'index.html'
    if index_file.exists():
        try:
            with open(index_file, 'r', encoding='utf-8', errors='ignore') as f:
                html = f.read()

            soup = BeautifulSoup(html, 'lxml')

            # Extract municipality name from title
            title = soup.find('title')
            if title:
                title_text = title.get_text(strip=True)
                # Clean up title
                municipality_name = re.sub(r'\s*[-|]\s*.*$', '', title_text)
                municipality_name = municipality_name.replace('Adams County Municipality', '').strip()

            # Find logo
            for img in soup.find_all('img'):
                alt = img.get('alt', '').lower()
                src = img.get('src', '').lower()
                if 'logo' in alt or 'seal' in alt or 'logo' in src or 'seal' in src:
                    logo_url = img.get('src', '')
                    break

            # Extract footer metadata
            contact_info = extract_footer_metadata(soup)

        except Exception as e:
            show_progress(f"Error extracting metadata: {e}", "warning")

    return {
        'municipality_name': municipality_name,
        'logo_url': logo_url or '',
        'primary_color': '#0A2463',
        'contact': contact_info,
        'social_media': {}
    }


# ============================================================================
# CONTENT MAPPING
# ============================================================================

def map_content_to_pages(parsed_files: List[Dict]) -> Dict:
    """
    Maps parsed content to 12-page structure.

    Args:
        parsed_files: List of parsed file dictionaries

    Returns:
        Dictionary with 12 pages
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
            pages['home']['content'] = content
            pages['home']['hero']['title'] = title
        else:
            # For other pages, append content
            if pages[page_type]['content']:
                pages[page_type]['content'] += '\n\n---\n\n' + content
            else:
                pages[page_type]['content'] = content

    return pages


# ============================================================================
# OUTPUT GENERATION
# ============================================================================

def markdown_to_html(markdown_text: str) -> str:
    """Converts markdown to HTML."""
    try:
        import markdown
        return markdown.markdown(markdown_text, extensions=['extra', 'nl2br'])
    except ImportError:
        # Basic conversion
        html = markdown_text
        html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
        html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)

        paragraphs = html.split('\n\n')
        html = ''.join([f'<p>{p}</p>\n' if p.strip() and not p.strip().startswith('<') else p + '\n'
                       for p in paragraphs])
        return html


def generate_html_page(page_name: str, content: str, metadata: Dict, pages: Dict) -> str:
    """Generates complete HTML page with navigation and styling."""
    html_content = markdown_to_html(content) if content else "<p><em>No content available for this page.</em></p>"

    # Apply layout template
    page_data = pages.get(page_name, {})
    layout_func = get_layout(page_name)
    html_content = layout_func(html_content, metadata, page_data)

    current_layout = DEFAULT_LAYOUT_MAP.get(page_name, 'a')

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

    # Build navigation
    nav_items = []
    for nav_page in page_titles.keys():
        active_class = ' class="active"' if nav_page == page_name else ''
        nav_items.append(f'                <li><a href="{nav_page}.html"{active_class}>{page_titles[nav_page]}</a></li>')
    nav_html = '\n'.join(nav_items)

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

    # Layout switcher
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
                {f'<img src="images/{Path(metadata.get("logo_url", "")).name}" alt="Logo" class="logo">' if metadata.get('logo_url') else ''}
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

            <div class="copyright">
                <p>&copy; {datetime.now().year} {site_name}. All rights reserved.</p>
                <p style="font-size: 0.8rem; margin-top: 0.5rem; opacity: 0.7;">Generated by Municipal Website Parser v2.0 • Layout: {current_layout.upper()}</p>
            </div>
        </div>
    </footer>

{layout_switcher}

    <script src="layout_switcher.js"></script>
</body>
</html>"""

    return html


def generate_output_files(data: Dict, output_dir: Path) -> None:
    """Generates complete HTML website with all pages."""
    output_dir.mkdir(parents=True, exist_ok=True)

    show_progress("Generating output files...", "save")

    # Generate JSON file
    domain = data['metadata'].get('municipality_name', 'unknown').replace(' ', '-').lower()
    json_file = output_dir / f"{domain}-parsed.json"

    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    show_progress(f"✓ {json_file.name}", "success")

    # Copy CSS and JS
    script_dir = Path(__file__).parent

    css_source = script_dir / "templates" / "style.css"
    css_dest = output_dir / "style.css"
    if css_source.exists():
        shutil.copy(css_source, css_dest)
        show_progress(f"✓ style.css", "success")

    js_source = script_dir / "templates" / "layout_switcher.js"
    js_dest = output_dir / "layout_switcher.js"
    if js_source.exists():
        shutil.copy(js_source, js_dest)
        show_progress(f"✓ layout_switcher.js", "success")

    # Generate HTML files
    page_names = ['home', 'about', 'government', 'departments', 'services',
                  'news', 'events', 'contact', 'documents', 'employment',
                  'faqs', 'accessibility']

    for page_name in page_names:
        html_file = output_dir / f"{page_name}.html"
        page_data = data['pages'].get(page_name, {})
        content = page_data.get('content', '')

        if not content:
            content = f"# {page_name.title()}\n\n*No content found for this page.*"

        html_content = generate_html_page(page_name, content, data['metadata'], data['pages'])

        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        show_progress(f"✓ {html_file.name}", "success")

    # Create index.html redirect
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
    """Main execution function."""
    print_header()

    # Get mode and path from user
    mode, path, domain = get_mode_and_path()

    # Step 1: Download or use local
    if mode == 'download':
        if not download_site(path, domain):
            show_progress("Failed to download site. Exiting.", "error")
            sys.exit(1)
        source_path = f"./downloads/{domain}"
    else:
        source_path = path
        show_progress(f"Using local folder: {source_path}", "info")

    # Step 2: Find HTML files
    html_files = find_html_files(source_path)

    if not html_files:
        show_progress("No HTML files found!", "error")
        sys.exit(1)

    # Step 3: Parse HTML files
    show_progress("Parsing content...", "progress")
    parsed_files = []
    for html_file in html_files:
        parsed = parse_html_file(html_file)
        if parsed:
            parsed_files.append(parsed)
            show_progress(f"✓ {html_file.name} ({parsed.get('type', 'unknown')})", "success")

    # Step 4: Extract metadata
    show_progress("Extracting metadata...", "progress")
    metadata = extract_metadata(html_files, Path(source_path))
    metadata['source_path'] = source_path
    metadata['parsed_at'] = datetime.now().isoformat()
    show_progress(f"✓ Found: {metadata['municipality_name']}", "success")

    # Step 5: Map content to pages
    show_progress("Mapping content to pages...", "progress")
    pages = map_content_to_pages(parsed_files)

    # Step 6: Build data structure
    data = {
        'metadata': metadata,
        'pages': pages
    }

    # Step 7: Setup output directory
    output_dir = Path(f"./output/{domain}")

    # Step 8: Download/copy images
    show_progress("Copying images...", "progress")
    image_count = download_local_images(Path(source_path), output_dir, html_files)

    # Step 9: Generate output files
    generate_output_files(data, output_dir)

    # Step 10: Print summary
    print_summary(data, len(html_files), output_dir, image_count)


if __name__ == '__main__':
    main()
