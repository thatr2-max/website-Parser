"""
Generic Layout Templates
5 flexible layouts that can be used for any page type
Data is semantically flagged so layouts can be switched
"""

def layout_a_single_column(content_html: str, metadata: dict, page_data: dict) -> str:
    """
    LAYOUT A: Single Column (Clean & Simple)
    - Full width content
    - Best for: Text-heavy pages, About, Government, FAQs
    """
    return f'''
<div class="layout layout-a" data-layout="a">
    <div class="content-wrapper single-column">
        {content_html}
    </div>
</div>
'''


def layout_b_two_column(content_html: str, metadata: dict, page_data: dict) -> str:
    """
    LAYOUT B: Two Column (Content + Sidebar)
    - Main content on left, info cards on right
    - Best for: Services, Departments, Contact
    """
    contact = metadata.get('contact', {})

    # Build sidebar
    sidebar_items = []

    if contact.get('phone'):
        sidebar_items.append(f'''
        <div class="sidebar-card" data-type="contact-card">
            <h3 data-type="card-title">📞 Contact</h3>
            <p data-type="phone">{contact['phone']}</p>
        </div>''')

    if contact.get('email'):
        sidebar_items.append(f'''
        <div class="sidebar-card" data-type="contact-card">
            <h3 data-type="card-title">✉️ Email</h3>
            <p data-type="email"><a href="mailto:{contact['email']}">{contact['email']}</a></p>
        </div>''')

    if contact.get('hours'):
        sidebar_items.append(f'''
        <div class="sidebar-card" data-type="hours-card">
            <h3 data-type="card-title">🕐 Hours</h3>
            <p data-type="hours">{contact['hours']}</p>
        </div>''')

    sidebar_html = '\n'.join(sidebar_items) if sidebar_items else '<div class="sidebar-card"><p>Additional information</p></div>'

    return f'''
<div class="layout layout-b" data-layout="b">
    <div class="content-wrapper two-column">
        <div class="main-content">
            {content_html}
        </div>
        <aside class="sidebar">
            {sidebar_html}
        </aside>
    </div>
</div>
'''


def layout_c_card_grid(content_html: str, metadata: dict, page_data: dict) -> str:
    """
    LAYOUT C: Card Grid (Visual & Organized)
    - Content broken into cards in a grid
    - Best for: Services, Departments, Events, News
    """
    return f'''
<div class="layout layout-c" data-layout="c">
    <div class="content-wrapper card-grid">
        {content_html}
    </div>
</div>
'''


def layout_d_hero_featured(content_html: str, metadata: dict, page_data: dict) -> str:
    """
    LAYOUT D: Hero/Featured (Bold & Eye-catching)
    - Large hero section at top
    - Best for: Home, Landing pages, Major announcements
    """
    events = page_data.get('events', [])[:3]

    events_html = ""
    if events:
        events_html = '''
        <div class="featured-section" data-type="events">
            <h2 data-type="section-heading">Upcoming Events</h2>
            <div class="featured-grid">'''

        for event in events:
            events_html += f'''
                <div class="featured-card" data-type="event-card">
                    <span class="featured-date" data-type="event-date">{event.get("date", "TBD")}</span>
                    <h3 data-type="event-title">{event.get("title", "Event")}</h3>
                </div>'''

        events_html += '</div></div>'

    return f'''
<div class="layout layout-d" data-layout="d">
    <div class="hero-section" data-type="hero">
        <div class="hero-content">
            {content_html}
        </div>
    </div>
    {events_html}
</div>
'''


def layout_e_list_compact(content_html: str, metadata: dict, page_data: dict) -> str:
    """
    LAYOUT E: Compact List (Dense & Scannable)
    - Tight spacing, easy to scan
    - Best for: Documents, Forms, Employment, FAQ
    """
    return f'''
<div class="layout layout-e" data-layout="e">
    <div class="content-wrapper compact-list">
        {content_html}
    </div>
</div>
'''


# Layout mapping
LAYOUTS = {
    'a': layout_a_single_column,
    'b': layout_b_two_column,
    'c': layout_c_card_grid,
    'd': layout_d_hero_featured,
    'e': layout_e_list_compact,
}

# Default layout assignments (can be overridden)
DEFAULT_LAYOUT_MAP = {
    'home': 'd',           # Hero layout
    'about': 'a',          # Single column
    'government': 'b',     # Two column
    'departments': 'c',    # Card grid
    'services': 'c',       # Card grid
    'news': 'c',           # Card grid
    'events': 'c',         # Card grid
    'contact': 'b',        # Two column
    'documents': 'e',      # Compact list
    'employment': 'e',     # Compact list
    'faqs': 'e',           # Compact list
    'accessibility': 'a',  # Single column
}


def get_layout(page_name: str, layout_override: str = None):
    """
    Get layout function for a page.

    Args:
        page_name: Name of the page
        layout_override: Force a specific layout (a, b, c, d, e)

    Returns:
        Layout function
    """
    layout_key = layout_override or DEFAULT_LAYOUT_MAP.get(page_name, 'a')
    return LAYOUTS.get(layout_key, layout_a_single_column)
