Build a complete municipal website parser and converter system.

OVERVIEW:
Create a Python script that takes a municipal website URL, automatically downloads it via wget, parses all content, intelligently maps it to our 12-page structure, converts to markdown, and outputs a complete site ready for deployment.

---

WHAT THIS SCRIPT DOES (Full Automation):

1. User runs: `python parse_site.py https://example.gov`
2. Script uses wget to download entire site locally
3. Script finds and parses all HTML files
4. Script extracts metadata (logo, contact info, colors)
5. Script intelligently maps content to our 12 pages
6. Script converts all content to clean markdown
7. Script outputs JSON + 12 markdown files
8. Done - ready to deploy

---

TECHNICAL REQUIREMENTS:

LANGUAGE: Python 3.8+

DEPENDENCIES:
- beautifulsoup4 (HTML parsing)
- html2text (HTML to Markdown conversion)
- subprocess (for wget)
- json, pathlib, re (stdlib)

USAGE:
```bash
python parse_site.py https://abbottstown.comcastbiz.net
```

---

CORE FUNCTIONALITY:

STEP 1: DOWNLOAD SITE WITH WGET

Use subprocess to run wget with these flags:
```bash
wget --recursive \
     --no-clobber \
     --page-requisites \
     --html-extension \
     --convert-links \
     --restrict-file-names=windows \
     --domains={domain} \
     --no-parent \
     --directory-prefix=./downloads/{domain}/ \
     --timeout=10 \
     --tries=3 \
     {url}
```

Store in: `./downloads/{domain}/`
Show progress to user
Handle errors gracefully (wget not installed, network issues, etc.)

---

STEP 2: FIND ALL HTML FILES

Recursively find all .html files in `./downloads/{domain}/`
Return list of file paths to parse

---

STEP 3: PARSE EACH HTML FILE

For each HTML file:
1. Load with BeautifulSoup
2. Identify page type based on:
   - Filename (index.html → home, about.html → about, etc.)
   - URL path (if detectable)
   - Page title
   - Content keywords
3. Extract main content (remove nav, footer, sidebar, scripts)
4. Convert to markdown with html2text
5. Store in appropriate page category

---

STEP 4: EXTRACT SITE METADATA

From all pages, extract:
- Municipality name (from title, h1, header)
- Logo URL (img with "logo" in src/alt)
- Contact info:
  * Phone: regex `\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}`
  * Email: regex `[\w\.-]+@[\w\.-]+\.\w+`
  * Address: look for street addresses
  * Office hours: look for "Monday-Friday" patterns
- Social media links (facebook.com, twitter.com, etc.)
- Primary color: detect from CSS if possible, default to #0A2463

---

STEP 5: INTELLIGENT CONTENT MAPPING

Map content to these 12 pages based on Abbottstown structure:

HOME PAGE:
Extract:
- Hero section (main image + title)
- Events (look for dates, calendar, "upcoming events")
- News (look for dates, "news", "announcements")
- Information Center cards:
  * Contact Us
  * Utilities/Waste
  * New Residents
- Business section cards:
  * Officials
  * Committees
  * Meetings
  * Financial Records
- Documents section:
  * Open Records
  * Document Center

ABOUT:
- Look for: about*, history*, mission*, overview*
- Extract: history, mission, demographics

GOVERNMENT:
- Look for: government*, mayor*, council*, leadership*
- Extract: mayor info, council members, organizational structure

DEPARTMENTS:
- Look for: department*, division*
- Extract: list of departments, contact info

SERVICES:
- Look for: service*, permit*, license*, utilit*
- Extract: all services, how to access, forms

NEWS:
- Look for: news*, announcement*, press*
- Extract: articles with titles, dates, summaries (get 5-10 most recent)

EVENTS:
- Look for: event*, calendar*
- Extract: upcoming events with dates, times, locations

CONTACT:
- Look for: contact*, email*, phone*
- Extract: address, phone, email, hours, department contacts

DOCUMENTS:
- Look for: document*, form*, download*, pdf
- Extract: links to PDFs, forms, descriptions

EMPLOYMENT:
- Look for: job*, career*, employ*, work*
- Extract: job listings, how to apply, benefits

FAQS:
- Look for: faq*, question*
- Extract: questions and answers

ACCESSIBILITY:
- Look for: accessibility*, ada*, wcag*
- Extract: accessibility statement, compliance info

If content doesn't fit clearly, store in "additional_content"

---

STEP 6: CLEAN CONTENT

For extracted HTML content:
1. Remove these elements:
   - Navigation menus (<nav>, menus with many links)
   - Headers (site header with logo/nav)
   - Footers (copyright, bottom links)
   - Sidebars (often have "sidebar" in class)
   - Breadcrumbs
   - "Share this" widgets
   - Social media embeds
   - Cookie notices
   - Search forms
   - Scripts and styles

2. Keep only:
   - Main content text
   - Headings (h1-h6)
   - Paragraphs
   - Lists (ul, ol)
   - Tables
   - Images (src + alt)
   - Links (href + text)

3. Convert to markdown:
   - Use html2text library
   - Preserve heading hierarchy
   - Preserve lists and links
   - Clean up extra whitespace
   - Remove HTML attributes

---

STEP 7: OUTPUT FILES

Generate these files in `./output/{domain}/`:

1. `{domain}-parsed.json` - Complete structured data:
```json
{
  "metadata": {
    "municipality_name": "Abbottstown Borough",
    "source_url": "https://...",
    "parsed_at": "2024-01-16T...",
    "logo_url": "images/logo.png",
    "primary_color": "#7d4745",
    "contact": {
      "phone": "717-259-0965",
      "email": "abbottstown@comcast.net",
      "address": "241 High Street, Abbottstown, PA 17301",
      "hours": "Monday-Thursday 9:00 AM-5:00 PM, Friday 9:00 AM-4:00 PM"
    },
    "social_media": {}
  },
  "pages": {
    "home": {
      "hero": {
        "image": "mural.jpg",
        "title": "Borough of Abbottstown"
      },
      "events": [...],
      "news": [...],
      "information_center": [...],
      "business_section": [...],
      "documents_section": [...]
    },
    "about": {"content": "# About..."},
    "government": {"content": "# Government..."},
    ...
  }
}
```

2. Individual markdown files for each page:
   - `home.md`
   - `about.md`
   - `government.md`
   - `departments.md`
   - `services.md`
   - `news.md`
   - `events.md`
   - `contact.md`
   - `documents.md`
   - `employment.md`
   - `faqs.md`
   - `accessibility.md`

---

USER EXPERIENCE:

Show progress:
```
🌐 Municipal Website Parser
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📥 Downloading https://abbottstown.comcastbiz.net...
   [progress bar]
✅ Download complete

📄 Found 23 HTML files

🔍 Parsing content...
   ✓ Identified home page
   ✓ Found 3 news articles
   ✓ Found 2 upcoming events
   ✓ Extracted contact info
   ✓ Mapped 8 of 12 pages

💾 Generating output files...
   ✓ abbottstown-comcastbiz-net-parsed.json
   ✓ home.md
   ✓ about.md
   ✓ government.md
   ...

✨ DONE!

📊 Summary:
   Municipality: Abbottstown Borough
   Pages parsed: 23
   Content mapped: 8/12 pages
   Output: ./output/abbottstown.comcastbiz.net/

⚠️  Warnings:
   - No employment page found
   - FAQs page not detected
   - Accessibility statement missing

🎯 Next steps:
   1. Review JSON file for accuracy
   2. Edit markdown files as needed
   3. Deploy to platform
```

---

ERROR HANDLING:

Handle these gracefully:
- wget not installed → clear error message with install instructions
- Network timeout → retry, then fail gracefully
- No HTML files found → check if download succeeded
- Broken HTML → BeautifulSoup handles this
- Missing content → log warning, return empty string
- Can't detect page type → put in "additional_content"

NEVER crash - always produce output files

---

SMART HEURISTICS:

Date detection:
- MM/DD/YYYY
- January 15, 2024
- Jan 15, 2024
- 01-15-2024
- 2024-01-15

Phone detection:
- (555) 123-4567
- 555-123-4567
- 555.123.4567
- 5551234567

Email detection:
- Standard email regex

Address detection:
- Number + street type + city, state zip

Page type detection:
- Filename: index.html, about.html, contact.html, etc.
- Title: "About Us", "Contact", "Services", etc.
- URL path: /about, /contact, /services
- Content keywords: "mayor", "council", "permits", etc.

---

DELIVERABLES:

1. Single Python script: `parse_site.py`
2. README.md with:
   - Installation: `pip install beautifulsoup4 html2text lxml`
   - Requirements: Python 3.8+, wget installed
   - Usage: `python parse_site.py <url>`
   - Examples
3. Make it production-ready:
   - Fast (complete in 2-5 minutes)
   - Reliable (works on 90% of sites)
   - User-friendly (clear progress, helpful errors)
   - Well-commented code

---

TEST ON:
https://abbottstown.comcastbiz.net

Show me the output JSON and home.md for this test case.

---

BUILD THIS TO BE MY SECRET WEAPON.

Make it bulletproof, fast, and easy to use.

This is what closes deals.
