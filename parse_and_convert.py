#!/usr/bin/env python3
"""
Website Migration Tool - Intelligent Content Parser & Converter
Parses migrated websites and converts them to standardized templates
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
import html2text
from collections import defaultdict

class WebsiteParser:
    """Parse and convert migrated websites to standardized templates"""

    def __init__(self, source_dir, output_dir="converted_sites"):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.templates_dir = Path("templates")

        # Extracted metadata
        self.metadata = {
            "site_name": "",
            "site_description": "",
            "contact": {
                "phone": "",
                "email": "",
                "address": "",
                "fax": "",
                "hours": ""
            },
            "social_media": {},
            "logo_url": "",
            "primary_color": "#2c3e50"
        }

        # Content mapping
        self.content = defaultdict(str)
        self.pages = {}

        # HTML to Markdown converter
        self.h2t = html2text.HTML2Text()
        self.h2t.ignore_links = False
        self.h2t.body_width = 0

    def run(self):
        """Main execution flow"""
        print("╔═══════════════════════════════════════════════════════╗")
        print("║   Website Parser & Converter - Template Migration    ║")
        print("╚═══════════════════════════════════════════════════════╝\n")

        print(f"📂 Source: {self.source_dir}")
        print(f"📂 Output: {self.output_dir}\n")

        # Step 1: Find and parse all HTML files
        html_files = self.find_html_files()
        print(f"✓ Found {len(html_files)} HTML files\n")

        # Step 2: Extract metadata
        print("🔍 Extracting metadata...")
        self.extract_metadata(html_files)
        print(f"✓ Site Name: {self.metadata['site_name']}")
        print(f"✓ Contact: {self.metadata['contact']['email']}\n")

        # Step 3: Parse and categorize content
        print("📄 Parsing content...")
        self.parse_content(html_files)
        print(f"✓ Parsed {len(self.pages)} pages\n")

        # Step 4: Map content to templates
        print("🗺️  Mapping content to templates...")
        self.map_content_to_templates()
        print("✓ Content mapped\n")

        # Step 5: Generate output files
        print("💾 Generating output files...")
        self.generate_output()
        print("✓ Files generated\n")

        # Step 6: Copy assets
        print("📦 Copying assets...")
        self.copy_assets()
        print("✓ Assets copied\n")

        print("✨ DONE! Conversion complete.")
        print(f"📊 Output: {self.output_dir.absolute()}\n")

    def find_html_files(self):
        """Find all HTML files in source directory"""
        html_files = []
        for ext in ['*.html', '*.htm']:
            html_files.extend(self.source_dir.rglob(ext))
        return html_files

    def extract_metadata(self, html_files):
        """Extract site metadata from HTML files"""
        # Process first few files for metadata
        for html_file in html_files[:20]:
            try:
                with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                    soup = BeautifulSoup(f.read(), 'html.parser')

                    # Extract site name
                    if not self.metadata['site_name']:
                        # Try title tag
                        title = soup.find('title')
                        if title:
                            site_name = title.get_text().strip()
                            # Clean up common patterns
                            site_name = re.sub(r'\s*[-|:]\s*Home.*', '', site_name, flags=re.IGNORECASE)
                            site_name = re.sub(r'\s*[-|:]\s*Welcome.*', '', site_name, flags=re.IGNORECASE)
                            self.metadata['site_name'] = site_name

                        # Try logo alt text
                        if not self.metadata['site_name']:
                            logo = soup.find('img', {'alt': re.compile(r'logo', re.IGNORECASE)})
                            if logo and logo.get('alt'):
                                self.metadata['site_name'] = logo['alt']

                    # Extract logo
                    if not self.metadata['logo_url']:
                        logo = soup.find('img', {'src': re.compile(r'logo', re.IGNORECASE)}) or \
                               soup.find('img', {'alt': re.compile(r'logo', re.IGNORECASE)}) or \
                               soup.find('img', {'class': re.compile(r'logo', re.IGNORECASE)})
                        if logo and logo.get('src'):
                            self.metadata['logo_url'] = logo['src']

                    # Extract contact info
                    text = soup.get_text()

                    # Phone
                    if not self.metadata['contact']['phone']:
                        phone = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
                        if phone:
                            self.metadata['contact']['phone'] = phone.group()

                    # Email
                    if not self.metadata['contact']['email']:
                        email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
                        if email:
                            self.metadata['contact']['email'] = email.group()

                    # Address (simple pattern)
                    if not self.metadata['contact']['address']:
                        address = re.search(r'\d+\s+[\w\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct|Circle|Cir)[,\s]+[\w\s]+,\s*[A-Z]{2}\s+\d{5}', text)
                        if address:
                            self.metadata['contact']['address'] = address.group()

                    # Hours
                    if not self.metadata['contact']['hours']:
                        hours = re.search(r'(Monday|Mon).*?(Friday|Fri).*?\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)', text, re.IGNORECASE)
                        if hours:
                            self.metadata['contact']['hours'] = hours.group()

            except Exception as e:
                print(f"  Warning: Could not parse {html_file.name}: {e}")
                continue

        # Set defaults if not found
        if not self.metadata['site_name']:
            domain = self.source_dir.name
            self.metadata['site_name'] = domain.replace('-', ' ').replace('_', ' ').title()

    def parse_content(self, html_files):
        """Parse content from HTML files and categorize"""
        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                    soup = BeautifulSoup(f.read(), 'html.parser')

                    # Identify page type
                    page_type = self.identify_page_type(html_file, soup)

                    # Extract clean content
                    content = self.extract_clean_content(soup)

                    # Store page data
                    if page_type not in self.pages:
                        self.pages[page_type] = []

                    self.pages[page_type].append({
                        'file': html_file.name,
                        'title': self.get_page_title(soup),
                        'content': content,
                        'soup': soup
                    })

            except Exception as e:
                print(f"  Warning: Could not parse {html_file.name}: {e}")
                continue

    def identify_page_type(self, filepath, soup):
        """Identify what type of page this is"""
        filename = filepath.stem.lower()

        # URL/filename-based detection
        if filename in ['index', 'home', 'default']:
            return 'home'
        elif 'about' in filename:
            return 'about'
        elif 'service' in filename:
            return 'services'
        elif 'contact' in filename:
            return 'contact'
        elif any(x in filename for x in ['news', 'blog', 'article', 'post']):
            return 'news'
        elif any(x in filename for x in ['event', 'calendar']):
            return 'events'
        elif any(x in filename for x in ['document', 'form', 'download']):
            return 'documents'
        elif any(x in filename for x in ['department', 'division']):
            return 'departments'
        elif any(x in filename for x in ['government', 'council', 'mayor', 'official', 'leadership']):
            return 'government'
        elif any(x in filename for x in ['job', 'career', 'employ']):
            return 'employment'
        elif 'faq' in filename:
            return 'faq'

        # Title-based detection
        title = self.get_page_title(soup)
        if title:
            title_lower = title.lower()
            if 'about' in title_lower:
                return 'about'
            elif 'contact' in title_lower:
                return 'contact'
            elif 'news' in title_lower:
                return 'news'

        return 'other'

    def get_page_title(self, soup):
        """Extract page title"""
        # Try h1 first
        h1 = soup.find('h1')
        if h1:
            return h1.get_text().strip()

        # Try title tag
        title = soup.find('title')
        if title:
            text = title.get_text().strip()
            # Remove site name if present
            text = re.sub(r'\s*[-|:]\s*' + re.escape(self.metadata['site_name']), '', text)
            return text

        return "Untitled"

    def extract_clean_content(self, soup):
        """Extract main content, removing nav/footer/sidebar"""
        # Clone soup to avoid modifying original
        soup = BeautifulSoup(str(soup), 'html.parser')

        # Remove unwanted elements
        for element in soup.find_all(['script', 'style', 'nav', 'header', 'footer']):
            element.decompose()

        # Remove elements by class/id
        for selector in [
            {'class': re.compile(r'nav|menu|sidebar|aside', re.I)},
            {'id': re.compile(r'nav|menu|sidebar|aside|header|footer', re.I)}
        ]:
            for element in soup.find_all(attrs=selector):
                element.decompose()

        # Try to find main content area
        main = soup.find('main') or \
               soup.find('article') or \
               soup.find('div', {'class': re.compile(r'content|main', re.I)}) or \
               soup.find('div', {'id': re.compile(r'content|main', re.I)})

        if main:
            content_html = str(main)
        else:
            # Use body
            body = soup.find('body')
            content_html = str(body) if body else str(soup)

        return content_html

    def map_content_to_templates(self):
        """Map parsed content to template variables"""
        # Home page content
        if 'home' in self.pages and self.pages['home']:
            home = self.pages['home'][0]
            self.content['HOME_CONTENT'] = home['content']
            self.content['HERO_TITLE'] = self.metadata['site_name']
            self.content['HERO_SUBTITLE'] = self.metadata['site_description'] or f"Welcome to {self.metadata['site_name']}"

        # About page
        if 'about' in self.pages and self.pages['about']:
            about = self.pages['about'][0]
            self.content['ABOUT_HISTORY'] = about['content']

        # Services
        if 'services' in self.pages:
            services_html = ""
            for page in self.pages['services']:
                services_html += page['content']
            self.content['SERVICES_INTRO'] = "Browse our available services below."
            self.content['SERVICES_CONTENT'] = services_html

        # Contact
        if 'contact' in self.pages and self.pages['contact']:
            self.content['CONTACT_INTRO'] = "Get in touch with us using the information below."

        # News
        if 'news' in self.pages:
            news_html = '<div class="news-list">'
            for i, article in enumerate(self.pages['news'][:10]):
                news_html += f'''
                <article class="card">
                    <h3>{article['title']}</h3>
                    <div>{article['content'][:500]}...</div>
                </article>
                '''
            news_html += '</div>'
            self.content['NEWS_ARTICLES'] = news_html

            # Also add to home page
            self.content['NEWS_CARDS'] = news_html[:1000]

        # Events
        if 'events' in self.pages:
            events_html = '<div class="events-list">'
            for event in self.pages['events'][:10]:
                events_html += f'''
                <div class="card">
                    <h3>{event['title']}</h3>
                    <div>{event['content'][:300]}</div>
                </div>
                '''
            events_html += '</div>'
            self.content['UPCOMING_EVENTS'] = events_html
            self.content['EVENTS_LIST'] = events_html

        # Set defaults for missing content
        self.set_defaults()

    def set_defaults(self):
        """Set default values for any missing template variables"""
        defaults = {
            # Site-wide
            'SITE_NAME': self.metadata['site_name'],
            'SITE_DESCRIPTION': self.metadata.get('site_description', f'Welcome to {self.metadata["site_name"]}'),
            'META_DESCRIPTION': f'{self.metadata["site_name"]} - Official Website',
            'META_KEYWORDS': 'government, services, information',
            'CURRENT_YEAR': str(datetime.now().year),

            # Contact
            'CONTACT_PHONE': self.metadata['contact']['phone'] or 'Phone not available',
            'CONTACT_EMAIL': self.metadata['contact']['email'] or 'Email not available',
            'CONTACT_ADDRESS': self.metadata['contact']['address'] or 'Address not available',
            'CONTACT_FAX': self.metadata['contact'].get('fax', ''),
            'OFFICE_HOURS': self.metadata['contact'].get('hours', 'Monday-Friday, 9:00 AM - 5:00 PM'),

            # Hero
            'HERO_TITLE': self.metadata['site_name'],
            'HERO_SUBTITLE': f'Welcome to {self.metadata["site_name"]}',
            'HERO_IMAGE': '',

            # Defaults for empty sections
            'NEWS_CARDS': '<p>No news available at this time.</p>',
            'EVENTS_LIST': '<p>No upcoming events.</p>',
            'QUICK_LINKS_CARDS': '',
            'SERVICES_INTRO': 'Explore our services and resources.',
            'DEPARTMENTS_INTRO': 'Learn about our departments and their functions.',
            'DOCUMENTS_INTRO': 'Access important documents and forms.',
            'FAQ_INTRO': 'Find answers to common questions.',
            'EMPLOYMENT_INTRO': 'Join our team! View current openings below.',

            # Extra sections (empty by default)
            'EXTRA_HEAD': '',
            'EXTRA_SCRIPTS': '',
            'ABOUT_MISSION': '',
            'ABOUT_VALUES': '',
            'ABOUT_LEADERSHIP': '',
            'ABOUT_DEMOGRAPHICS': '',
            'ABOUT_ADDITIONAL_CONTENT': '',

            # Active navigation states (will be set per page)
            'ACTIVE_HOME': '',
            'ACTIVE_ABOUT': '',
            'ACTIVE_SERVICES': '',
            'ACTIVE_DEPARTMENTS': '',
            'ACTIVE_NEWS': '',
            'ACTIVE_EVENTS': '',
            'ACTIVE_DOCUMENTS': '',
            'ACTIVE_CONTACT': '',
        }

        # Apply defaults for any missing keys
        for key, value in defaults.items():
            if key not in self.content or not self.content[key]:
                self.content[key] = value

    def generate_output(self):
        """Generate final HTML files from templates"""
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Copy templates assets
        import shutil
        assets_src = self.templates_dir / "assets"
        assets_dst = self.output_dir / "assets"
        if assets_src.exists():
            shutil.copytree(assets_src, assets_dst, dirs_exist_ok=True)

        # Load base template
        base_template = self.load_template('_base.html')

        # Generate each page
        pages_to_generate = [
            ('index.html', 'Home', 'ACTIVE_HOME'),
            ('about.html', 'About Us', 'ACTIVE_ABOUT'),
            ('services.html', 'Services', 'ACTIVE_SERVICES'),
            ('departments.html', 'Departments', 'ACTIVE_DEPARTMENTS'),
            ('news.html', 'News', 'ACTIVE_NEWS'),
            ('events.html', 'Events', 'ACTIVE_EVENTS'),
            ('documents.html', 'Documents', 'ACTIVE_DOCUMENTS'),
            ('contact.html', 'Contact', 'ACTIVE_CONTACT'),
            ('government.html', 'Government', ''),
            ('employment.html', 'Employment', ''),
            ('faq.html', 'FAQ', ''),
            ('accessibility.html', 'Accessibility', ''),
            ('privacy.html', 'Privacy Policy', ''),
            ('terms.html', 'Terms of Service', ''),
            ('sitemap.html', 'Sitemap', ''),
        ]

        for filename, page_title, active_key in pages_to_generate:
            print(f"  ✓ Generating {filename}...")

            # Load page template
            page_content = self.load_template(filename)

            # Set active nav
            content_vars = self.content.copy()
            content_vars['PAGE_TITLE'] = page_title
            if active_key:
                content_vars[active_key] = 'active'

            # Merge page content into base
            content_vars['MAIN_CONTENT'] = page_content

            # Replace all variables
            final_html = self.replace_variables(base_template, content_vars)

            # Write output file
            output_file = self.output_dir / filename
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(final_html)

        # Generate metadata JSON
        metadata_file = self.output_dir / 'metadata.json'
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=2)
        print(f"  ✓ Generating metadata.json...")

    def load_template(self, filename):
        """Load a template file"""
        template_path = self.templates_dir / filename
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        return ''

    def replace_variables(self, template, variables):
        """Replace {{VARIABLES}} in template with actual values"""
        result = template
        for key, value in variables.items():
            placeholder = f'{{{{{key}}}}}'
            result = result.replace(placeholder, str(value))

        # Remove any unreplaced variables
        result = re.sub(r'\{\{[A-Z_]+\}\}', '', result)

        return result

    def copy_assets(self):
        """Copy images and other assets from source"""
        import shutil

        # Create assets directory in output
        assets_dir = self.output_dir / "assets" / "images"
        assets_dir.mkdir(parents=True, exist_ok=True)

        # Copy images
        image_exts = ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.ico']
        for ext in image_exts:
            for img_file in self.source_dir.rglob(f'*{ext}'):
                try:
                    dest = assets_dir / img_file.name
                    shutil.copy2(img_file, dest)
                except Exception as e:
                    pass  # Skip if copy fails

        print(f"  ✓ Copied images to {assets_dir}")


def main():
    """Main entry point"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python parse_and_convert.py <migrated_site_directory>")
        print("\nExample:")
        print("  python parse_and_convert.py migrated_sites/www.example.com")
        sys.exit(1)

    source_dir = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "converted_sites"

    # Create output dir name from source
    if output_dir == "converted_sites":
        source_name = Path(source_dir).name
        output_dir = f"converted_sites/{source_name}"

    try:
        parser = WebsiteParser(source_dir, output_dir)
        parser.run()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
