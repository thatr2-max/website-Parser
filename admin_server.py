#!/usr/bin/env python3
"""
Admin Dashboard Server
Simple Flask server for editing parsed websites before deployment
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from pathlib import Path
import json
from bs4 import BeautifulSoup

app = Flask(__name__)

# Configuration
OUTPUT_DIR = Path('./output')

def get_available_sites():
    """Get list of all parsed sites in output directory"""
    if not OUTPUT_DIR.exists():
        return []
    return [d.name for d in OUTPUT_DIR.iterdir() if d.is_dir()]

def get_site_pages(site_name):
    """Get list of all pages for a site"""
    site_dir = OUTPUT_DIR / site_name
    if not site_dir.exists():
        return []

    pages = []
    for html_file in site_dir.glob('*.html'):
        if html_file.name != 'index.html':  # Skip redirect page
            pages.append(html_file.stem)
    return sorted(pages)

@app.route('/')
def index():
    """Admin dashboard home - list all sites"""
    sites = get_available_sites()
    return render_template('admin_index.html', sites=sites)

@app.route('/edit/<site_name>')
def edit_site(site_name):
    """Edit interface for a specific site"""
    pages = get_site_pages(site_name)
    return render_template('admin_edit.html', site_name=site_name, pages=pages)

@app.route('/api/page/<site_name>/<page_name>')
def get_page(site_name, page_name):
    """API: Get page HTML for editing"""
    page_path = OUTPUT_DIR / site_name / f"{page_name}.html"

    if not page_path.exists():
        return jsonify({'error': 'Page not found'}), 404

    with open(page_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    return jsonify({'html': html_content})

@app.route('/api/page/<site_name>/<page_name>', methods=['POST'])
def save_page(site_name, page_name):
    """API: Save edited page HTML"""
    page_path = OUTPUT_DIR / site_name / f"{page_name}.html"

    if not page_path.exists():
        return jsonify({'error': 'Page not found'}), 404

    data = request.json
    new_html = data.get('html', '')

    # Backup original
    backup_path = page_path.with_suffix('.html.backup')
    if not backup_path.exists():
        import shutil
        shutil.copy(page_path, backup_path)

    # Save new version
    with open(page_path, 'w', encoding='utf-8') as f:
        f.write(new_html)

    return jsonify({'success': True, 'message': f'Saved {page_name}.html'})

@app.route('/api/content/<site_name>/<page_name>')
def get_page_content(site_name, page_name):
    """API: Get just the editable content from a page"""
    page_path = OUTPUT_DIR / site_name / f"{page_name}.html"

    if not page_path.exists():
        return jsonify({'error': 'Page not found'}), 404

    with open(page_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Parse and extract main content
    soup = BeautifulSoup(html_content, 'html.parser')
    main_content = soup.find('main')

    if main_content:
        content_html = str(main_content)
    else:
        content_html = html_content

    return jsonify({'content': content_html})

@app.route('/api/content/<site_name>/<page_name>', methods=['POST'])
def save_page_content(site_name, page_name):
    """API: Save just the content portion of a page"""
    page_path = OUTPUT_DIR / site_name / f"{page_name}.html"

    if not page_path.exists():
        return jsonify({'error': 'Page not found'}), 404

    data = request.json
    new_content = data.get('content', '')

    # Read original HTML
    with open(page_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Parse and replace main content
    soup = BeautifulSoup(html_content, 'html.parser')
    main_tag = soup.find('main')

    if main_tag:
        # Backup original
        backup_path = page_path.with_suffix('.html.backup')
        if not backup_path.exists():
            import shutil
            shutil.copy(page_path, backup_path)

        # Replace main content
        new_main = BeautifulSoup(new_content, 'html.parser')
        main_tag.replace_with(new_main)

        # Save updated HTML
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))

        return jsonify({'success': True, 'message': f'Saved {page_name}.html'})
    else:
        return jsonify({'error': 'Could not find main content'}), 400

@app.route('/preview/<site_name>/<path:filename>')
def preview_file(site_name, filename):
    """Serve files from site directory for preview"""
    site_dir = OUTPUT_DIR / site_name
    return send_from_directory(site_dir, filename)

@app.route('/api/metadata/<site_name>')
def get_metadata(site_name):
    """API: Get site metadata"""
    # Find the JSON file
    site_dir = OUTPUT_DIR / site_name
    json_files = list(site_dir.glob('*-parsed.json'))

    if not json_files:
        return jsonify({'error': 'No metadata found'}), 404

    with open(json_files[0], 'r', encoding='utf-8') as f:
        metadata = json.load(f)

    return jsonify(metadata)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎨 Admin Dashboard Server")
    print("="*60)
    print(f"\n📂 Serving sites from: {OUTPUT_DIR.absolute()}")
    print(f"🌐 Open in browser: http://localhost:5000")
    print("\n✏️  Edit sites, then deploy the output/ folder to production")
    print("="*60 + "\n")

    app.run(debug=True, port=5000)
