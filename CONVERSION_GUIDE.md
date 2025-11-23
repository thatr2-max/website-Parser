# Website Conversion Guide 🎨

**Transform any website into a professional, standardized template format**

## 🎯 Overview

The Website Conversion Tool takes any migrated website and intelligently converts it into a clean, modern, standardized format using our 15-page template system.

### What You Get

**Before**: Messy, inconsistent website with various layouts and structures
**After**: Clean, professional 15-page website with:
- Modern, responsive design
- Consistent navigation and branding
- Accessible and SEO-friendly structure
- Easy to customize and deploy

---

## 🚀 Quick Start

### Complete Conversion (One Command)

```bash
# Download, parse, and convert in one step
./convert_website.sh https://www.example.com
```

That's it! In 15-30 minutes you'll have a complete, standardized website.

### Manual Workflow

If you want more control:

```bash
# Step 1: Migrate the website
./migrate.sh -m balanced https://www.example.com

# Step 2: Convert to templates
python3 parse_and_convert.py migrated_sites/www.example.com

# Step 3: Preview
cd converted_sites/www.example.com
python3 -m http.server 8000
```

---

## 📋 The 15 Template Pages

Our standardized template includes these pages:

### Core Pages (8)
1. **index.html** - Home page with hero, news, events
2. **about.html** - History, mission, leadership
3. **services.html** - Service listings and information
4. **departments.html** - Department directory
5. **news.html** - News articles and announcements
6. **events.html** - Event calendar and listings
7. **documents.html** - Document center and downloads
8. **contact.html** - Contact information and form

### Additional Pages (7)
9. **government.html** - Leadership and governance
10. **employment.html** - Job openings and careers
11. **faq.html** - Frequently asked questions
12. **accessibility.html** - Accessibility statement
13. **privacy.html** - Privacy policy
14. **terms.html** - Terms of service
15. **sitemap.html** - Complete site map

---

## 🔧 How It Works

### 1. Download Phase (migrate.sh)
- Uses wget to download the entire website
- Preserves all HTML, CSS, JS, images, documents
- Stores in `migrated_sites/<domain>/`

### 2. Analysis Phase (parse_and_convert.py)
**Metadata Extraction:**
- Site name, logo, colors
- Contact info (phone, email, address)
- Office hours, social media links

**Content Parsing:**
- Identifies page types intelligently
- Removes navigation, headers, footers
- Extracts clean main content
- Categorizes content by topic

**Smart Mapping:**
- Maps home page → index.html template
- Maps about pages → about.html template
- Maps contact info → contact.html template
- Maps news articles → news.html template
- And so on for all 15 pages...

### 3. Generation Phase
- Loads professional HTML templates
- Inserts parsed content into templates
- Applies consistent styling (CSS)
- Copies all assets (images, docs)
- Generates complete website

### 4. Output
- Clean, standardized website ready to deploy
- All 15 pages with consistent design
- Responsive, accessible, modern
- Saved in `converted_sites/<domain>/`

---

## 💡 Intelligent Content Mapping

The parser uses multiple heuristics to identify content:

### Page Type Detection
```
Homepage:     index.html, home.html, default.html
About:        about.html, about-us.html, history.html
Services:     services.html, programs.html
Contact:      contact.html, contact-us.html
News:         news.html, blog.html, articles.html
Events:       events.html, calendar.html
Documents:    documents.html, forms.html, downloads.html
Government:   government.html, council.html, mayor.html
Departments:  departments.html, divisions.html
Employment:   jobs.html, careers.html, employment.html
FAQ:          faq.html, questions.html
```

### Content Extraction
- Finds `<main>`, `<article>`, or `.content` areas
- Removes `<nav>`, `<header>`, `<footer>`, sidebars
- Preserves headings, paragraphs, lists, tables
- Keeps images and links
- Extracts clean, semantic HTML

### Metadata Extraction
- **Phone**: Regex pattern matching `(555) 123-4567`
- **Email**: Standard email format `user@domain.com`
- **Address**: Street addresses with city, state, zip
- **Hours**: Business hours patterns
- **Logo**: `<img>` tags with "logo" in src/alt/class

---

## 📂 Output Structure

After conversion:

```
converted_sites/www.example.com/
├── index.html              # Home page
├── about.html              # About page
├── services.html           # Services
├── departments.html        # Departments
├── news.html               # News
├── events.html             # Events
├── documents.html          # Documents
├── contact.html            # Contact
├── government.html         # Government
├── employment.html         # Jobs
├── faq.html                # FAQ
├── accessibility.html      # Accessibility
├── privacy.html            # Privacy
├── terms.html              # Terms
├── sitemap.html            # Sitemap
├── metadata.json           # Extracted metadata
└── assets/
    ├── css/
    │   └── main.css        # Professional stylesheet
    ├── js/
    │   └── main.js         # Interactive features
    └── images/             # All images from source
        └── *.jpg, *.png
```

---

## 🎨 Template Customization

### Modify Templates

Edit files in `templates/` directory:

```bash
templates/
├── _base.html              # Base layout (header, footer, nav)
├── index.html              # Home page template
├── about.html              # About page template
├── services.html           # Services template
└── ...                     # Other page templates
```

### Template Variables

Templates use `{{VARIABLE}}` placeholders:

```html
<!-- Site-wide variables -->
{{SITE_NAME}}               <!-- Website name -->
{{SITE_DESCRIPTION}}        <!-- Description -->
{{CONTACT_PHONE}}           <!-- Phone number -->
{{CONTACT_EMAIL}}           <!-- Email address -->
{{OFFICE_HOURS}}            <!-- Business hours -->

<!-- Page-specific variables -->
{{HOME_CONTENT}}            <!-- Home page content -->
{{ABOUT_HISTORY}}           <!-- About page history -->
{{NEWS_ARTICLES}}           <!-- News article list -->
{{UPCOMING_EVENTS}}         <!-- Event listings -->
```

### Customize Styling

Edit `templates/assets/css/main.css`:

```css
:root {
    /* Change colors */
    --primary-color: #2c3e50;
    --secondary-color: #3498db;
    --accent-color: #e74c3c;

    /* Change fonts */
    --font-family-base: 'Arial', sans-serif;
    --font-family-heading: 'Georgia', serif;

    /* Change spacing */
    --spacing-sm: 1rem;
    --spacing-md: 1.5rem;
    --spacing-lg: 2rem;
}
```

After modifying templates, re-run the parser:

```bash
python3 parse_and_convert.py migrated_sites/www.example.com
```

---

## ⚙️ Advanced Usage

### Parse Only (Skip Migration)

If you already have a migrated site:

```bash
python3 parse_and_convert.py <path_to_migrated_site> [output_dir]

# Example
python3 parse_and_convert.py migrated_sites/www.citygovt.gov converted_sites/citygovt
```

### Keep Raw Migrated Files

```bash
./convert_website.sh --keep-migrated https://www.example.com
```

### Custom Output Directory

```bash
./convert_website.sh -o /var/www/mysite https://www.example.com
```

### Migration Modes

```bash
# Fast mode (5-15 min) - Surface level
./convert_website.sh -m fast https://www.example.com

# Balanced mode (15-25 min) - Recommended
./convert_website.sh -m balanced https://www.example.com

# Complete mode (30-45 min) - Deep crawl
./convert_website.sh -m complete https://www.example.com
```

---

## 🔍 Troubleshooting

### Missing Content

**Problem**: Some pages are empty or have "No content available"

**Solution**:
1. Use `complete` mode for deeper crawling
2. Check `metadata.json` to see what was extracted
3. Manually add content to template HTML files
4. Verify source site has the content

### Wrong Page Mapping

**Problem**: Content appears on wrong pages

**Solution**:
1. Review `parse_and_convert.py` page detection logic
2. Manually edit generated HTML files
3. Modify templates to better match your needs

### Broken Images

**Problem**: Images don't display

**Solution**:
1. Check `assets/images/` directory
2. Verify image paths in HTML
3. Re-run with `--keep-migrated` to debug
4. Manually copy missing images

### Python Dependencies

**Problem**: `ModuleNotFoundError: No module named 'bs4'`

**Solution**:
```bash
pip3 install -r requirements.txt

# Or manually
pip3 install beautifulsoup4 lxml html2text
```

---

## 📊 Conversion Examples

### Small Business Website
```bash
# Input: 10-page small business site
./convert_website.sh -m fast https://www.smallbiz.com

# Output:
# - 15 standardized pages
# - Modern, professional design
# - All services and contact info preserved
# - Time: ~10 minutes
```

### Municipal Government Site
```bash
# Input: 100+ page government website
./convert_website.sh -m complete https://www.citygovernment.gov

# Output:
# - 15 core pages with all essential info
# - Departments, officials, documents organized
# - News and events preserved
# - Time: ~35 minutes
```

### Corporate Website
```bash
# Input: Medium corporate site with blog
./convert_website.sh -m balanced https://www.corporation.com

# Output:
# - Professional 15-page structure
# - About, services, team, contact
# - Blog posts converted to news
# - Time: ~20 minutes
```

---

## 🎯 Best Practices

### For Best Results

1. **Use Balanced Mode**: Best trade-off between speed and accuracy
2. **Review Output**: Always check generated pages for accuracy
3. **Customize Templates**: Modify colors, fonts to match brand
4. **Add Missing Content**: Some content may need manual addition
5. **Test Thoroughly**: Preview locally before deploying

### Deployment Checklist

- [ ] Preview all 15 pages locally
- [ ] Check all links work
- [ ] Verify images display correctly
- [ ] Test navigation on mobile
- [ ] Update contact information
- [ ] Customize colors/fonts to match brand
- [ ] Add any missing content
- [ ] Test forms (if applicable)
- [ ] Run accessibility checker
- [ ] Deploy to web server

---

## 💻 Technical Details

### Dependencies

- **wget**: Website download
- **Python 3.7+**: Content parsing
- **BeautifulSoup4**: HTML parsing
- **html2text**: HTML to Markdown conversion
- **lxml**: Fast XML/HTML processing

### Template System

- **Base Template**: `_base.html` - Header, footer, navigation
- **Page Templates**: Individual page layouts
- **Variable Replacement**: `{{VAR}}` → actual content
- **CSS Framework**: Custom responsive grid system
- **JavaScript**: Vanilla JS, no frameworks required

### Parser Features

- Intelligent page type detection
- Metadata extraction (contact, hours, etc.)
- Content cleaning (removes nav/footer/sidebar)
- Smart content categorization
- Asset copying (images, documents)
- JSON metadata export

---

## 🆘 Support

Need help?

1. Check this guide and [README.md](README.md)
2. Review [QUICK_START.md](QUICK_START.md)
3. Check the output `metadata.json` for debugging
4. Review logs in `migration_logs/`
5. Open an issue on GitHub

---

## 📝 License

This tool is provided as-is for website migration and conversion. Ensure you have permission to migrate and convert any website you target.

---

**Made with ❤️ for fast, professional website conversions**
