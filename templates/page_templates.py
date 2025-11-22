"""
Page Template System
Different HTML layouts for different types of municipal website pages
"""

def template_hero_landing(content_html: str, metadata: dict, page_data: dict) -> str:
    """
    Template 1: Hero/Landing Page (Home)
    Features: Large hero section, events, news highlights
    """
    events = page_data.get('events', [])[:5]

    events_html = ""
    if events:
        events_html = '<div class="events-section"><h2>Upcoming Events</h2>'
        for event in events:
            events_html += f'''
            <div class="event-item">
                <span class="event-date">{event.get("date", "TBD")}</span>
                <h3>{event.get("title", "Event")}</h3>
            </div>'''
        events_html += '</div>'

    return f'''
<div class="hero-section">
    <div class="hero-content">
        {content_html}
    </div>
</div>
{events_html}
'''


def template_text_content(content_html: str, metadata: dict, page_data: dict) -> str:
    """
    Template 2: Standard Text Content (About, Government, etc.)
    Features: Clean article layout, headings, paragraphs
    """
    return f'''
<div class="text-content">
    {content_html}
</div>
'''


def template_contact(content_html: str, metadata: dict, page_data: dict) -> str:
    """
    Template 3: Contact Page
    Features: Structured contact info, office hours, map placeholder
    """
    contact = metadata.get('contact', {})

    contact_cards = []

    if contact.get('address'):
        contact_cards.append(f'''
        <div class="card contact-card">
            <h3>📍 Visit Us</h3>
            <p>{contact['address']}</p>
        </div>''')

    if contact.get('phone'):
        contact_cards.append(f'''
        <div class="card contact-card">
            <h3>📞 Call Us</h3>
            <p><strong>Phone:</strong> {contact['phone']}</p>
            {f'<p><strong>Fax:</strong> {contact.get("fax", "")}</p>' if contact.get('fax') else ''}
        </div>''')

    if contact.get('email'):
        contact_cards.append(f'''
        <div class="card contact-card">
            <h3>✉️ Email Us</h3>
            <p><a href="mailto:{contact['email']}">{contact['email']}</a></p>
        </div>''')

    if contact.get('hours'):
        contact_cards.append(f'''
        <div class="card contact-card">
            <h3>🕐 Office Hours</h3>
            <p>{contact['hours']}</p>
        </div>''')

    contact_grid = '\n'.join(contact_cards)

    return f'''
<div class="contact-page">
    <h1>Contact Information</h1>
    <div class="contact-grid">
        {contact_grid}
    </div>
    {content_html if content_html else ''}
</div>
'''


def template_directory_list(content_html: str, metadata: dict, page_data: dict) -> str:
    """
    Template 4: Directory/List (Departments, Services)
    Features: Grid layout, service cards
    """
    return f'''
<div class="directory-page">
    <div class="directory-content">
        {content_html}
    </div>
</div>
'''


def template_news_blog(content_html: str, metadata: dict, page_data: dict) -> str:
    """
    Template 5: News/Blog Articles
    Features: Article cards with dates, excerpts
    """
    return f'''
<div class="news-page">
    <h1>News & Announcements</h1>
    <div class="news-content">
        {content_html}
    </div>
</div>
'''


def template_events_calendar(content_html: str, metadata: dict, page_data: dict) -> str:
    """
    Template 6: Events/Calendar
    Features: Event listings with dates, times, locations
    """
    return f'''
<div class="events-page">
    <h1>Events Calendar</h1>
    <div class="events-content">
        {content_html}
    </div>
</div>
'''


def template_documents(content_html: str, metadata: dict, page_data: dict) -> str:
    """
    Template 7: Documents/Downloads
    Features: File listings, download links, categories
    """
    return f'''
<div class="documents-page">
    <h1>Documents & Forms</h1>
    <div class="alert alert-info">
        <p>📄 Download forms and documents below. Most files are in PDF format.</p>
    </div>
    <div class="documents-content">
        {content_html}
    </div>
</div>
'''


def template_faq(content_html: str, metadata: dict, page_data: dict) -> str:
    """
    Template 8: FAQs
    Features: Q&A format, expandable sections
    """
    return f'''
<div class="faq-page">
    <h1>Frequently Asked Questions</h1>
    <div class="faq-content">
        {content_html}
    </div>
</div>
'''


def template_employment(content_html: str, metadata: dict, page_data: dict) -> str:
    """
    Template 9: Employment/Jobs
    Features: Job listings, application info
    """
    return f'''
<div class="employment-page">
    <h1>Employment Opportunities</h1>
    <div class="employment-content">
        {content_html}
    </div>
</div>
'''


def template_forms_permits(content_html: str, metadata: dict, page_data: dict) -> str:
    """
    Template 10: Forms/Permits
    Features: Form categories, download links, instructions
    """
    return f'''
<div class="forms-page">
    <h1>Forms & Permits</h1>
    <div class="alert alert-info">
        <p>📋 Submit completed forms to the Borough Office or email to {metadata.get('contact', {}).get('email', 'the office')}.</p>
    </div>
    <div class="forms-content">
        {content_html}
    </div>
</div>
'''


# Template mapping: page_name -> template function
TEMPLATE_MAP = {
    'home': template_hero_landing,
    'about': template_text_content,
    'government': template_text_content,
    'departments': template_directory_list,
    'services': template_directory_list,
    'news': template_news_blog,
    'events': template_events_calendar,
    'contact': template_contact,
    'documents': template_documents,
    'employment': template_employment,
    'faqs': template_faq,
    'accessibility': template_text_content,
}


def get_template(page_name: str):
    """
    Get the appropriate template function for a page.

    Args:
        page_name: Name of the page (home, about, contact, etc.)

    Returns:
        Template function to use
    """
    return TEMPLATE_MAP.get(page_name, template_text_content)
