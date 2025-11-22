Build a robust municipal website content parser/scraper system.

OVERVIEW:
This tool takes any municipal website URL and intelligently extracts/parses content into a structured format that maps to our 12-page municipal website template.

---

INPUT:
- Single URL (municipal website homepage)
- Examples to test against:
  * https://www.cedarcrestblvd.org
  * https://www.tinytown.gov (if exists)
  * https://www.smallville.us (if exists)
  * [Add 3-5 real URLs you want to test]

---

CORE FUNCTIONALITY:

1. FETCH & CRAWL:
   - Fetch the homepage HTML
   - Identify and crawl key pages (about, contact, government, services, etc.)
   - Handle both:
     * Single-page sites (all content on one page)
     * Multi-page sites (content across multiple pages)
   - Follow internal links intelligently (max 20-30 pages)
   - Respect robots.txt (but be aggressive within allowed bounds)
   - Handle various site structures (WordPress, Wix, custom CMS, static HTML)

2. CONTENT EXTRACTION:
   Extract and categorize content into these sections:

   A. SITE METADATA:
      - Site name/municipality name
      - Logo URL (if exists)
      - Primary color scheme (detect dominant colors)
      - Contact info (phone, email, address)
      - Social media links

   B. HOME PAGE CONTENT:
      - Hero/welcome section (main heading, subheading)
      - Quick links/featured services
      - News items (latest 3-5)
      - Events (upcoming 3-5)
      - Any CTAs (call-to-action buttons)

   C. ABOUT/HISTORY:
      - Municipality history
      - Mission statement
      - Demographics/statistics
      - Any "about us" content

   D. GOVERNMENT:
      - Mayor/leadership info (name, photo, bio)
      - Council members (names, roles, photos)
      - Department listings
      - Organizational structure

   E. SERVICES:
      - All services offered (permits, utilities, etc.)
      - Service descriptions
      - How to access each service
      - Links to forms/applications

   F. NEWS/ANNOUNCEMENTS:
      - Recent news articles (get 5-10 latest)
      - Article titles, dates, summaries
      - Full content if available

   G. EVENTS:
      - Upcoming events (get next 5-10)
      - Event titles, dates, times, locations
      - Event descriptions

   H. CONTACT INFORMATION:
      - Physical address
      - Mailing address (if different)
      - Phone numbers (main + departments)
      - Email addresses
      - Office hours
      - Department contact info

   I. DOCUMENTS:
      - Links to PDFs, forms, documents
      - Document titles and categories

   J. EMPLOYMENT:
      - Job listings (if any)
      - How to apply
      - Benefits info

   K. OTHER:
      - FAQs
      - Any accessibility statements
      - Privacy policies
      - Meeting minutes/agendas

3. INTELLIGENT MAPPING:
   - Use AI/heuristics to determine which content belongs on which of our 12 pages:
     * Home
     * About
     * Government  
     * Departments
     * Services
     * News
     * Events
     * Contact
     * Documents
     * Employment
     * FAQs
     * Accessibility Statement

   - If content doesn't clearly map, make best guess or put in "Additional Content" section

4. CONTENT CLEANING:
   - Remove navigation menus, headers, footers
   - Remove sidebar content
   - Strip out ads, widgets, irrelevant sections
   - Clean up HTML (remove inline styles, scripts, etc.)
   - Fix broken formatting
   - Preserve important structure (headings, lists, tables)
   - Extract plain text but maintain semantic meaning

5. FORMAT CONVERSION:
   - Convert cleaned content to Markdown
   - Maintain heading hierarchy
   - Preserve links, lists, tables
   - Handle images (extract URLs, provide alt text)
   - Create clean, readable markdown

---

OUTPUT FORMAT:

Generate a JSON file with this structure:

{
  "metadata": {
    "source_url": "https://example.gov",
    "municipality_name": "Smalltown",
    "scraped_at": "2024-01-16T12:00:00Z",
    "logo_url": "https://example.gov/logo.png",
    "primary_color": "#0A2463",
    "contact": {
      "phone": "(555) 123-4567",
      "email": "info@example.gov",
      "address": "123 Main St, Smalltown, ST 12345",
      "hours": "Mon-Fri, 8AM-5PM"
    },
    "social_media": {
      "facebook": "https://facebook.com/...",
      "twitter": "https://twitter.com/..."
    }
  },
  "pages": {
    "home": {
      "hero": {
        "title": "Welcome to Smalltown",
        "subtitle": "Your gateway to municipal services",
        "cta_primary": "View Services",
        "cta_secondary": "Contact Us"
      },
      "quick_links": [
        {"title": "Pay Utilities", "url": "/utilities"},
        {"title": "Permits", "url": "/permits"}
      ],
      "content": "# Welcome\n\nMarkdown content here..."
    },
    "about": {
      "content": "# About Smalltown\n\n## History\n\nFounded in 1843..."
    },
    "government": {
      "mayor": {
        "name": "Jane Smith",
        "photo_url": "https://...",
        "bio": "Mayor Smith has served..."
      },
      "council": [
        {"name": "John Doe", "role": "Council Member", "photo_url": "..."}
      ],
      "content": "# Our Government\n\n..."
    },
    "departments": {
      "content": "# Departments\n\n## Public Works\n\n..."
    },
    "services": {
      "content": "# Services\n\n## Permits & Licenses\n\n..."
    },
    "news": {
      "articles": [
        {
          "title": "City Council Approves Budget",
          "date": "2024-01-15",
          "summary": "The council voted...",
          "content": "Full article markdown..."
        }
      ],
      "content": "# Latest News\n\n..."
    },
    "events": {
      "upcoming": [
        {
          "title": "Town Hall Meeting",
          "date": "2024-01-20",
          "time": "6:00 PM",
          "location": "City Hall",
          "description": "Monthly town hall..."
        }
      ],
      "content": "# Upcoming Events\n\n..."
    },
    "contact": {
      "content": "# Contact Us\n\n..."
    },
    "documents": {
      "content": "# Documents & Forms\n\n..."
    },
    "employment": {
      "content": "# Employment Opportunities\n\n..."
    },
    "faqs": {
      "content": "# Frequently Asked Questions\n\n..."
    },
    "accessibility": {
      "content": "# Accessibility Statement\n\n..."
    }
  },
  "additional_content": {
    "unmapped": [
      {
        "title": "Some other page",
        "content": "Content that didn't fit elsewhere..."
      }
    ]
  }
}

---

TECHNICAL REQUIREMENTS:

1. LANGUAGE/FRAMEWORK:
   - Use Python with BeautifulSoup4 + Requests
   - OR Node.js with Cheerio + Axios
   - (Choose whatever is fastest to implement)

2. ROBUSTNESS:
   - Handle timeouts gracefully
   - Handle SSL certificate errors
   - Handle broken HTML
   - Handle missing content (return empty strings, not errors)
   - Handle various character encodings
   - Handle redirects
   - Retry failed requests (3 attempts)

3. PERFORMANCE:
   - Complete parsing in under 2 minutes for typical site
   - Concurrent requests where possible (don't be too slow)
   - Cache pages during single run (don't refetch same page)

4. USER EXPERIENCE:
   - Progress indicators (show what it's doing)
   - Clear error messages if something fails
   - Summary stats at end (pages crawled, content extracted, etc.)

5. USAGE:
   - Command-line interface:
```
     python parser.py https://example.gov
     OR
     node parser.js https://example.gov
```
   - Outputs JSON file: `example-gov-parsed.json`
   - Also generate individual markdown files per page in `/output/example-gov/` folder

---

INTELLIGENT HEURISTICS:

Use these clues to identify content:

- Navigation links → Discover key pages
- URL patterns → /about, /government, /services, /contact, etc.
- Page titles → Match to our 12-page structure
- Heading content → Identify sections
- Common municipal keywords → "mayor", "council", "permits", "utilities", etc.
- Date patterns → Identify news/events
- Email/phone patterns → Extract contact info
- PDF links → Identify documents

Be smart about:
- Wordpress sites (common structure)
- Wix sites (iframe content)
- GoDaddy website builder
- Custom HTML sites
- Sites with poor structure

---

ERROR HANDLING:

If parsing fails or content is minimal:
- Return JSON with metadata + empty pages
- Include error details in JSON
- Don't crash - always return valid JSON
- Log what went wrong for debugging

---

TESTING:

Test on at least 5 different municipal sites with varying structures:
1. Modern responsive site
2. Old HTML site (2000s era)
3. WordPress site
4. Site with minimal content
5. Site with complex navigation

Show parsing results for each test case.

---

OUTPUT EXAMPLES:

Provide clear examples of:
1. What the JSON output looks like for a real site
2. What the generated markdown files look like
3. How to use the parsed data

---

DELIVERABLES:

1. The parser script (Python or Node.js)
2. README with:
   - Installation instructions
   - Usage examples
   - How it works (high-level)
3. Test results on 5 sample sites
4. Example output JSON
5. Any dependencies/requirements file

---

MAKE IT PRODUCTION-READY:

This needs to work reliably during live sales demos.
- Fast enough (< 2 minutes)
- Reliable enough (90%+ success rate)
- Good enough content extraction (doesn't have to be perfect)
- Clear output that can be reviewed/edited if needed

Build this to be the secret weapon that closes deals.
