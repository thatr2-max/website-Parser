# Quick Start Guide - Website Migration Tool

Get started with website migrations in 60 seconds!

## 🚀 Installation (30 seconds)

```bash
# Clone the repository
git clone <your-repo-url>
cd website-Parser

# Make scripts executable (already done if you cloned)
chmod +x migrate.sh batch_migrate.sh

# You're ready to go!
```

## ⚡ Your First Migration (30 seconds)

### Single Website

```bash
# Migrate a website (fast mode - 5-15 minutes)
./migrate.sh https://example.com

# Done! Your site is now in: ./migrated_sites/example.com/
```

### Multiple Websites

```bash
# Create a list of sites
cat > sites.txt << EOF
https://example1.com
https://example2.com
https://example3.com
EOF

# Migrate all at once
./batch_migrate.sh sites.txt

# Done! All sites are in: ./migrated_sites/
```

## 📊 Check Your Results

```bash
# View migrated files
ls -lh migrated_sites/

# View migration logs
cat migration_logs/migration_*.log

# Open the migrated website
cd migrated_sites/example.com/
python3 -m http.server 8000
# Visit: http://localhost:8000
```

## 🎯 Common Scenarios

### Scenario 1: Quick Customer Website Backup
**Time Target**: < 10 minutes

```bash
./migrate.sh https://customer-site.com
```

### Scenario 2: Medium Website with Good Coverage
**Time Target**: 15-20 minutes

```bash
./migrate.sh -m balanced https://corporate-site.com
```

### Scenario 3: Full Website Archive
**Time Target**: 30+ minutes

```bash
./migrate.sh -m complete https://large-portal.com
```

### Scenario 4: Migrate 10 Customer Sites
**Time Target**: 1-2 hours (10 sites × 10 minutes avg)

```bash
# Create your list
nano sites.txt  # Add your URLs

# Migrate all
./batch_migrate.sh sites.txt
```

### Scenario 5: Only Download Images from Gallery
**Time Target**: 2-5 minutes

```bash
./migrate.sh --mirror-images-only https://photography-site.com/gallery
```

## 🛠️ Troubleshooting

### "Command not found: wget"

```bash
# Ubuntu/Debian
sudo apt-get install wget

# CentOS/RHEL
sudo yum install wget

# macOS
brew install wget
```

### "Permission denied"

```bash
chmod +x migrate.sh batch_migrate.sh
```

### Migration is too slow

```bash
# Use fast mode with shallow depth
./migrate.sh -m fast -d 1 https://example.com

# Or increase rate limit (if bandwidth allows)
./migrate.sh -r 10m https://example.com
```

### Missing pages or assets

```bash
# Increase depth
./migrate.sh -d 3 https://example.com

# Or use balanced mode
./migrate.sh -m balanced https://example.com
```

## 📈 Performance Tips

1. **Start with Fast Mode**: Try `./migrate.sh` first (fast mode is default)
2. **Use Shallow Depth for Speed**: Add `-d 1` for one level deep
3. **Exclude Large Files**: Add `-e "*.pdf" -e "*.zip"` to skip binaries
4. **Increase Rate Limit**: Add `-r 10m` if you have good bandwidth
5. **Monitor Progress**: Check logs in real-time: `tail -f migration_logs/*.log`

## 🎓 Next Steps

1. Read the full [README.md](README.md) for advanced options
2. Customize [config.example.sh](config.example.sh) for your needs
3. Set up batch migrations for multiple clients
4. Automate with cron jobs for regular backups

## 💡 Pro Tips

- **Test First**: Always test with fast mode before doing complete migrations
- **Check Logs**: Logs are in `migration_logs/` - review them for errors
- **Verify Results**: Open migrated sites locally to ensure completeness
- **Bandwidth Matters**: Slow migrations? Check your internet speed
- **Server Speed**: Remote server response time affects migration duration

## 🎯 Time Expectations

| Site Size | Fast Mode | Balanced Mode | Complete Mode |
|-----------|-----------|---------------|---------------|
| Small (< 20 pages) | 2-5 min | 5-10 min | 10-15 min |
| Medium (20-100 pages) | 8-15 min | 15-20 min | 25-35 min |
| Large (100+ pages) | 15-25 min | 25-40 min | 45+ min |

**Target: Sub-30-minute migrations** ✓

## ❓ Need Help?

- Check the [README.md](README.md) for detailed documentation
- Review your logs in `migration_logs/`
- Ensure wget is installed: `wget --version`
- Test connectivity: `wget https://example.com -O test.html`

---

**You're all set! Start migrating websites in under 30 minutes! 🚀**
