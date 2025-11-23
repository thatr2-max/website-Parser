# Website Migration & Conversion Tool 🚀

**Two powerful tools in one: Fast website migration + Professional template conversion**

A complete website migration and conversion system that can:
1. **Migrate**: Clone any website with wget (sub-30-minute migrations)
2. **Convert**: Transform migrated sites into professional, standardized templates

Perfect for web hosting providers, digital agencies, IT professionals, and anyone who needs to quickly migrate and standardize customer websites.

---

## 🎯 Two Ways to Use This Tool

### Option 1: Complete Conversion (Recommended) 🎨
**Download → Parse → Convert → Standardize**

Get a clean, professional, 15-page standardized website:

```bash
./convert_website.sh https://www.example.com
```

**Output**: Modern, responsive, standardized website with 15 professionally designed pages.

**See**: [CONVERSION_GUIDE.md](CONVERSION_GUIDE.md) for complete documentation.

### Option 2: Migration Only 📥
**Just download the website as-is**

Get an exact copy of the website:

```bash
./migrate.sh https://www.example.com
```

**Output**: Complete copy of the original website (HTML, CSS, JS, images, etc.)

**See**: Documentation below for migration-only features.

---

## ✨ Features

### Migration Features
- **⚡ Ultra-Fast Migrations**: Optimized for sub-30-minute migrations
- **🎯 Multiple Migration Modes**: Fast, Balanced, and Complete migration profiles
- **📊 Real-Time Statistics**: Track progress and view detailed migration stats
- **🔧 Highly Configurable**: Extensive options for customization
- **📝 Comprehensive Logging**: Detailed logs for every migration
- **🎨 Beautiful CLI**: Color-coded output with progress indicators
- **🔄 Batch Processing**: Migrate multiple websites at once
- **🛡️ Error Handling**: Robust retry mechanisms and timeout handling

### Conversion Features ⭐ NEW!
- **🎨 15 Professional Templates**: Standardized page structure
- **🤖 Intelligent Content Mapping**: AI-powered content extraction
- **📱 Responsive Design**: Mobile-friendly, modern layouts
- **♿ Accessible**: WCAG-compliant, semantic HTML
- **🎯 SEO-Friendly**: Clean URLs, proper meta tags
- **🔍 Smart Parsing**: Automatic page type detection
- **📦 Asset Preservation**: All images and documents preserved
- **⚙️ Customizable**: Easy to modify templates and styling

---

## 🚀 Quick Start

### Prerequisites

**For Migration Only:**
- Linux/Unix system (macOS, Ubuntu, Debian, etc.)
- `wget` installed (usually pre-installed)
- Bash shell

**For Conversion (Migration + Templates):**
- All of the above, plus:
- Python 3.7+
- pip (Python package manager)

### Basic Usage

**Complete Conversion** (Download + Convert to Templates):
```bash
# Recommended: Get a standardized, professional website
./convert_website.sh https://example.com
```

**Migration Only** (Download as-is):
```bash
# Fast mode - Surface level (5-15 min)
./migrate.sh https://example.com

# Balanced mode - Good coverage (15-25 min)
./migrate.sh -m balanced https://example.com

# Complete mode - Everything (30+ min)
./migrate.sh -m complete https://example.com
```

## 📋 Installation

```bash
# Clone this repository
git clone <your-repo-url>
cd website-Parser

# Make scripts executable
chmod +x migrate.sh convert_website.sh parse_and_convert.py

# Install Python dependencies (for conversion features)
pip3 install -r requirements.txt

# Run your first conversion!
./convert_website.sh https://example.com
```

## 🎮 Usage Guide

### Command Syntax

```bash
./migrate.sh [OPTIONS] <URL>
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `-m, --mode <mode>` | Migration mode: fast, balanced, complete | fast |
| `-o, --output <dir>` | Output directory for migrated sites | ./migrated_sites |
| `-l, --log <dir>` | Log directory | ./migration_logs |
| `-r, --rate-limit <rate>` | Download rate limit (e.g., 2m, 500k) | 2m |
| `-d, --depth <level>` | Maximum recursion depth | Mode-dependent |
| `-e, --exclude <pattern>` | Exclude URLs matching pattern | None |
| `--no-parent` | Don't ascend to parent directory | false |
| `--mirror-images-only` | Only download images | false |
| `--mirror-assets-only` | Only download assets (CSS, JS, images) | false |
| `-h, --help` | Show help message | - |

### Migration Modes

#### 🏃 Fast Mode (Default)
**Target Time**: 5-15 minutes
**Best For**: Landing pages, small business sites, quick backups

```bash
./migrate.sh https://example.com
```

**Settings**:
- Depth: 1 level
- Retries: 2
- Timeout: 10s
- Rate Limit: 5MB/s
- Excludes: Large binaries (exe, dmg, pkg, zip, tar.gz)

#### ⚖️ Balanced Mode
**Target Time**: 15-25 minutes
**Best For**: Medium-sized sites, corporate websites, portfolios

```bash
./migrate.sh -m balanced https://example.com
```

**Settings**:
- Depth: 3 levels
- Retries: 3
- Timeout: 15s
- Rate Limit: 3MB/s
- Excludes: System binaries

#### 🔍 Complete Mode
**Target Time**: 30+ minutes
**Best For**: Large sites, full archives, complete backups

```bash
./migrate.sh -m complete https://example.com
```

**Settings**:
- Depth: Unlimited
- Retries: 5
- Timeout: 30s
- Rate Limit: 2MB/s
- Excludes: None (downloads everything)

## 📚 Examples

### Basic Migrations

```bash
# Fast migration (default)
./migrate.sh https://example.com

# Balanced migration with custom output directory
./migrate.sh -m balanced -o /backup/websites https://example.com

# Complete migration
./migrate.sh -m complete https://example.com
```

### Advanced Usage

```bash
# Exclude specific patterns (admin pages)
./migrate.sh -e "*/admin/*" -e "*/wp-admin/*" https://example.com

# Custom depth and rate limit
./migrate.sh -d 5 -r 10m https://example.com

# Only download images from a gallery
./migrate.sh --mirror-images-only https://example.com/gallery

# Only download website assets (CSS, JS, images, fonts)
./migrate.sh --mirror-assets-only https://example.com

# Prevent ascending to parent directories
./migrate.sh --no-parent https://example.com/blog
```

### Batch Migrations

```bash
# Use the batch migration script
./batch_migrate.sh sites.txt

# Where sites.txt contains:
# https://example1.com
# https://example2.com
# https://example3.com
```

## 📊 Output Structure

After migration, your files will be organized as follows:

```
website-Parser/
├── migrated_sites/
│   ├── example.com/
│   │   ├── index.html
│   │   ├── about.html
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── another-site.com/
│       └── ...
└── migration_logs/
    ├── migration_example.com_20250101_120000.log
    └── migration_another-site.com_20250101_130000.log
```

## 📈 Performance Tips

### For Fastest Migrations (< 10 minutes)

1. **Use Fast Mode**: Default settings are optimized for speed
2. **Limit Depth**: Use `-d 1` or `-d 2` for shallow crawls
3. **Exclude Large Files**: Use `-e` to skip unnecessary content
4. **Increase Rate Limit**: Use `-r 10m` or higher if bandwidth allows
5. **Skip Assets**: Use `--mirror-images-only` if you only need images

### For Complete Migrations

1. **Use Complete Mode**: `-m complete` for full site coverage
2. **Check robots.txt**: Tool bypasses robots.txt by default
3. **Monitor Logs**: Watch log files for errors or issues
4. **Allocate Time**: Full sites may take 30+ minutes

## 🛠️ Troubleshooting

### Migration Takes Too Long

```bash
# Use fast mode with shallow depth
./migrate.sh -m fast -d 1 https://example.com

# Exclude large file types
./migrate.sh -e "*.pdf" -e "*.zip" https://example.com
```

### Missing Files or Pages

```bash
# Increase depth
./migrate.sh -d 5 https://example.com

# Use balanced or complete mode
./migrate.sh -m complete https://example.com
```

### SSL/Certificate Errors

The tool uses standard wget which respects SSL certificates. For testing environments:

```bash
# Add this to the script if needed (not recommended for production)
--no-check-certificate
```

### Rate Limiting Issues

```bash
# Reduce rate limit to be more respectful
./migrate.sh -r 500k https://example.com

# Or increase for faster downloads (if allowed)
./migrate.sh -r 20m https://example.com
```

## 📋 Migration Statistics

After each migration, you'll see detailed statistics:

```
╔═══════════════════════════════════════════════════════╗
║              Migration Statistics                     ║
╠═══════════════════════════════════════════════════════╣
║ Total Duration:                     12m 34s           ║
║ Total Files:                        342               ║
║ Total Size:                         45.2 MB           ║
║ HTML Pages:                         87                ║
║ CSS Files:                          23                ║
║ JavaScript Files:                   56                ║
║ Images:                             156               ║
╚═══════════════════════════════════════════════════════╝

✓ Migration completed in under 30 minutes!
```

## 🔐 Security Considerations

- **robots.txt**: By default, the tool bypasses robots.txt for migration purposes
- **Authentication**: Does not handle login/authentication (add wget auth flags if needed)
- **HTTPS**: Respects SSL certificates by default
- **User-Agent**: Uses a standard browser user-agent to avoid blocking

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## 📝 License

This tool is provided as-is for website migration purposes. Ensure you have permission to migrate/clone any website you target.

## 🆘 Support

For issues, questions, or feature requests:
- Check the [Troubleshooting](#-troubleshooting) section
- Review the logs in `migration_logs/`
- Open an issue on GitHub

## 🎯 Use Cases

- **Web Hosting Migration**: Move customer sites between hosting providers
- **Website Backups**: Create local backups of websites
- **Development**: Clone production sites for local development
- **Archiving**: Archive websites for historical purposes
- **Testing**: Create test environments from live sites
- **Disaster Recovery**: Quick site recovery from live URLs

## ⚡ Performance Benchmarks

Based on typical usage:

| Site Type | Pages | Size | Fast Mode | Balanced Mode | Complete Mode |
|-----------|-------|------|-----------|---------------|---------------|
| Landing Page | 1-5 | < 5MB | 1-3 min | 2-4 min | 3-5 min |
| Small Business | 10-30 | 5-20MB | 5-10 min | 10-15 min | 15-20 min |
| Corporate Site | 50-100 | 20-50MB | 10-15 min | 15-25 min | 25-35 min |
| Large Portal | 200+ | 100MB+ | 15-20 min | 25-35 min | 45+ min |

*Times vary based on network speed, server response time, and content type.*

---

**Made with ❤️ for fast, reliable website migrations**
