#!/usr/bin/env node

/**
 * Municipal Website Template Generator
 *
 * This script fills Handlebars templates with municipality data
 * and generates static HTML pages.
 *
 * Usage:
 *   node generate.js [data-file.json] [output-directory]
 *
 * Example:
 *   node generate.js example-data.json output/
 */

const fs = require('fs');
const path = require('path');
const Handlebars = require('handlebars');

// Configuration
const TEMPLATES_DIR = './templates';
const DEFAULT_DATA_FILE = './example-data.json';
const DEFAULT_OUTPUT_DIR = './output';

/**
 * Load and parse JSON data file
 */
function loadData(dataFile) {
  try {
    const content = fs.readFileSync(dataFile, 'utf8');
    return JSON.parse(content);
  } catch (error) {
    console.error(`Error loading data file: ${error.message}`);
    process.exit(1);
  }
}

/**
 * Load a template file
 */
function loadTemplate(templatePath) {
  try {
    return fs.readFileSync(templatePath, 'utf8');
  } catch (error) {
    console.error(`Error loading template: ${error.message}`);
    process.exit(1);
  }
}

/**
 * Ensure output directory exists
 */
function ensureOutputDir(outputDir) {
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
    console.log(`✓ Created output directory: ${outputDir}`);
  }
}

/**
 * Copy static assets to output directory
 */
function copyStaticAssets(outputDir) {
  const staticDir = './static';
  const outputStaticDir = path.join(outputDir, 'static');

  if (!fs.existsSync(staticDir)) {
    console.warn('⚠ Warning: static directory not found');
    return;
  }

  // Copy entire static directory
  copyRecursive(staticDir, outputStaticDir);
  console.log('✓ Copied static assets');
}

/**
 * Recursively copy directory
 */
function copyRecursive(src, dest) {
  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }

  const entries = fs.readdirSync(src, { withFileTypes: true });

  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isDirectory()) {
      copyRecursive(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

/**
 * Register Handlebars helpers
 */
function registerHelpers() {
  // Helper for array iteration with index
  Handlebars.registerHelper('each', function(context, options) {
    let ret = '';
    if (context && context.length > 0) {
      for (let i = 0; i < context.length; i++) {
        ret += options.fn(context[i], { data: { index: i } });
      }
    }
    return ret;
  });

  // Helper for conditional rendering
  Handlebars.registerHelper('if', function(conditional, options) {
    if (conditional) {
      return options.fn(this);
    } else {
      return options.inverse(this);
    }
  });
}

/**
 * Generate all pages from templates
 */
function generatePages(data, outputDir) {
  const templates = [
    'home.html',
    'about.html',
    'government.html',
    'departments.html',
    'services.html',
    'news.html',
    'events.html',
    'contact.html',
    'documents.html',
    'meetings.html',
    'employment.html',
    'faqs.html',
    'accessibility.html',
    'privacy.html',
    'sitemap.html'
  ];

  registerHelpers();

  templates.forEach(templateName => {
    const templatePath = path.join(TEMPLATES_DIR, templateName);
    const outputPath = path.join(outputDir, templateName);

    // Load template
    const templateContent = loadTemplate(templatePath);
    const template = Handlebars.compile(templateContent);

    // Get page-specific data
    const pageData = getPageData(templateName, data);

    // Generate HTML
    const html = template(pageData);

    // Write output file
    fs.writeFileSync(outputPath, html, 'utf8');
    console.log(`✓ Generated ${templateName}`);
  });
}

/**
 * Get page-specific data merged with global data
 */
function getPageData(templateName, data) {
  const globalData = {
    municipality_name: data.municipality_name,
    logo_url: data.logo_url,
    contact_address_line1: data.contact.address_line1,
    contact_address_line2: data.contact.address_line2,
    contact_phone: data.contact.phone,
    contact_phone_formatted: data.contact.phone_formatted,
    contact_email: data.contact.email,
    office_hours: data.contact.office_hours,
    current_year: new Date().getFullYear()
  };

  // Get page-specific data from the pages object
  const pageName = templateName.replace('.html', '');
  const pageSpecificData = data.pages[pageName] || {};

  return { ...globalData, ...pageSpecificData };
}

/**
 * Main execution
 */
function main() {
  console.log('🏛️  Municipal Website Template Generator\n');

  // Parse command line arguments
  const args = process.argv.slice(2);
  const dataFile = args[0] || DEFAULT_DATA_FILE;
  const outputDir = args[1] || DEFAULT_OUTPUT_DIR;

  console.log(`Data file: ${dataFile}`);
  console.log(`Output directory: ${outputDir}\n`);

  // Load data
  console.log('Loading data...');
  const data = loadData(dataFile);
  console.log(`✓ Loaded data for: ${data.municipality_name}\n`);

  // Prepare output directory
  console.log('Preparing output directory...');
  ensureOutputDir(outputDir);

  // Copy static assets
  console.log('\nCopying static assets...');
  copyStaticAssets(outputDir);

  // Generate pages
  console.log('\nGenerating pages...');
  generatePages(data, outputDir);

  console.log('\n✅ Generation complete!');
  console.log(`\n📁 Output location: ${path.resolve(outputDir)}`);
  console.log(`\n🌐 Open ${path.join(outputDir, 'home.html')} in your browser to view the site.\n`);
}

// Check if Handlebars is installed
try {
  require.resolve('handlebars');
} catch (e) {
  console.error('❌ Error: Handlebars is not installed.');
  console.error('\nPlease install it by running:');
  console.error('  npm install handlebars\n');
  process.exit(1);
}

// Run the generator
if (require.main === module) {
  main();
}

module.exports = { generatePages, loadData };
