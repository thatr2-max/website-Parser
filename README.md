# Municipal Website Templates

**Perfect, ADA-compliant page templates for small municipalities.**

This repository contains a complete set of 15 HTML page templates designed specifically for small city and town governments. The templates are WCAG 2.1 AA compliant, fully responsive, and built to serve 500+ municipalities with identical design and structure.

## Features

- **15 Complete Page Templates** - Everything a municipality needs
- **WCAG 2.1 AA Compliant** - Fully accessible to all users
- **Responsive Design** - Works on all devices (320px to 4K)
- **No Frameworks** - Pure HTML/CSS/JS for maximum performance
- **Professional Design** - Trustworthy, government-appropriate styling
- **Easy Customization** - Handlebars templates with simple data files
- **Fast Loading** - Optimized for sub-1-second load times

## Templates Included

1. **home.html** - Homepage with hero, quick links, news, and events
2. **about.html** - About page with sidebar for quick facts
3. **government.html** - Mayor and City Council information
4. **departments.html** - Department directory with contact info
5. **services.html** - Municipal services grid
6. **news.html** - News articles feed
7. **events.html** - Community events calendar
8. **contact.html** - Contact form and information
9. **documents.html** - Document library with categories
10. **meetings.html** - Meeting schedule and archives
11. **employment.html** - Job listings and applications
12. **faqs.html** - Frequently asked questions
13. **accessibility.html** - ADA compliance statement
14. **privacy.html** - Privacy policy
15. **sitemap.html** - Site navigation overview

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Generate Sample Site

```bash
node generate.js
```

This creates a complete website in the `output/` directory using the example data.

### 3. View the Site

Open `output/home.html` in your web browser.

## Usage

### Creating a New Municipality Site

1. **Copy the example data file:**
   ```bash
   cp example-data.json mytown-data.json
   ```

2. **Edit the data file** with your municipality's information:
   - Municipality name, logo, contact info
   - Page content (text, images, links)
   - News articles, events, council members, etc.

3. **Generate the site:**
   ```bash
   node generate.js mytown-data.json output/mytown
   ```

4. **Deploy** the contents of `output/mytown/` to your web server.

## Data File Structure

The data file is a JSON file with the following structure:

```json
{
  "municipality_name": "Your Town Name",
  "logo_url": "path/to/logo.png",
  "contact": {
    "address_line1": "123 Main St",
    "address_line2": "Town, ST 12345",
    "phone": "+15555551234",
    "phone_formatted": "(555) 555-1234",
    "email": "info@yourtown.gov",
    "office_hours": "Mon-Fri, 8AM-5PM"
  },
  "pages": {
    "home": { ... },
    "about": { ... },
    ...
  }
}
```

See `example-data.json` for a complete reference.

## Customization

### Colors

Edit `static/css/main.css` and modify the CSS variables:

```css
:root {
  --primary-blue: #0A2463;  /* Primary color */
  --white: #FFFFFF;         /* Background */
  /* ... other colors ... */
}
```

### Fonts

The templates use Open Sans from Google Fonts. To change:

1. Update the font link in each template
2. Update the `--font-family` CSS variable

### Content

All content is controlled through the data JSON file. The templates use Handlebars syntax:

- `{{variable}}` - Insert text
- `{{{variable}}}` - Insert HTML
- `{{#each array}}...{{/each}}` - Loop through arrays
- `{{#if condition}}...{{/if}}` - Conditional rendering

## Accessibility Features

- ✅ Semantic HTML5 markup
- ✅ ARIA labels and landmarks
- ✅ Keyboard navigation support
- ✅ Screen reader compatibility
- ✅ Color contrast ratios (WCAG AA)
- ✅ Responsive design (mobile-first)
- ✅ Focus indicators
- ✅ Skip links
- ✅ Minimum tap target sizes (44×44px)
- ✅ Support for reduced motion preferences

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Performance

- No external dependencies (except Google Fonts)
- Minimal JavaScript (mobile menu only)
- Optimized CSS (one stylesheet)
- Fast load times (<1s on modern connections)
- Works offline (static HTML)

## File Structure

```
.
├── templates/              # HTML templates (15 files)
│   ├── home.html
│   ├── about.html
│   └── ...
├── static/                 # Static assets
│   ├── css/
│   │   └── main.css       # Single stylesheet
│   └── js/
│       └── main.js        # Mobile menu script
├── generate.js            # Template generator
├── example-data.json      # Sample data
├── package.json           # Dependencies
└── README.md             # This file
```

## Development

### Testing Accessibility

1. Use browser DevTools Lighthouse audit
2. Test with screen readers (NVDA, JAWS, VoiceOver)
3. Navigate with keyboard only (Tab, Enter, Esc)
4. Verify color contrast with browser extensions
5. Test at different zoom levels (up to 200%)

### Making Changes

1. Edit templates in `templates/`
2. Edit styles in `static/css/main.css`
3. Test with `node generate.js`
4. View results in browser

## Deployment

1. Generate site: `node generate.js yourdata.json output/site`
2. Upload contents of `output/site/` to web server
3. Ensure proper MIME types are set
4. Configure HTTPS (required for modern browsers)
5. Set up proper caching headers

## Support

For questions or issues:
- Check the example data file for reference
- Review template HTML for variable names
- Consult WCAG 2.1 guidelines for accessibility questions

## License

This template system is provided as-is for use by municipalities.

## Credits

Built with:
- Pure HTML5, CSS3, JavaScript
- Handlebars.js for templating
- Open Sans font family
- WCAG 2.1 AA standards

---

**Built for municipalities. Designed for everyone.**
