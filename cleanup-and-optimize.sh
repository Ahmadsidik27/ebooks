#!/bin/bash
# Cleanup & Optimization Script untuk GitHub Pages Static Website

set -e

echo "🚀 Starting cleanup and optimization..."
echo ""

# Step 1: Backup before cleanup
echo "📦 Step 1: Creating backup..."
mkdir -p backups
tar -czf "backups/backup-$(date +%Y%m%d_%H%M%S).tar.gz" \
  api.py notebook_api.py extract_knowledge.py home.html chat.html \
  2>/dev/null || true
echo "✅ Backup created"
echo ""

# Step 2: Delete unnecessary files for static website
echo "🗑️  Step 2: Deleting unnecessary files..."

echo "  Removing Flask servers & APIs..."
rm -f api.py notebook_api.py
rm -f server.py extract_knowledge.py get_files.py
rm -f web-server-static.py

echo "  Removing Flask HTML files..."
rm -f home.html chat.html

echo "  Removing Flask index.html (will be replaced with static)..."
rm -f index.html

echo "  Removing knowledge base folder..."
rm -rf knowledge_base

echo "  Removing HTML_EBOOKS (converted HTML files)..."
rm -rf HTML_EBOOKS

echo "  Removing unnecessary documentation..."
rm -f pdf_to_html_converter.py STATIC_WEBSITE_READY.txt

echo "✅ Unnecessary files deleted"
echo ""

# Step 3: Minify JavaScript files
echo "📝 Step 3: Minifying JavaScript..."

# Remove unnecessary whitespace from books_data.js
if command -v node &> /dev/null; then
    echo "  Using Node.js for minification..."
    # Use sed for basic minification if uglify not available
    sed -E 's/\s+/ /g; s/([{}:;,])\s+/\1/g; s/\s+([{}:;,])/\1/g' \
      books_data.js > books_data.min.js
    mv books_data.min.js books_data.js
else
    echo "  Using sed for basic minification..."
    sed -E 's/\s+/ /g; s/([{}:;,])\s+/\1/g; s/\s+([{}:;,])/\1/g' \
      books_data.js > books_data.tmp.js
    mv books_data.tmp.js books_data.js
fi

echo "✅ JavaScript minified"
echo ""

# Step 4: Minify JSON
echo "📝 Step 4: Minifying JSON..."

# Compact JSON format
python3 << 'PYTHON'
import json

# Minify books_manifest.json
with open('books_manifest.json', 'r') as f:
    data = json.load(f)
with open('books_manifest.json', 'w') as f:
    json.dump(data, f, separators=(',', ':'), ensure_ascii=True)

print("✅ JSON files minified")
PYTHON

echo ""

# Step 5: Size report
echo "📊 Step 5: Size comparison..."

echo ""
echo "File sizes after cleanup:"
ls -lh index-github-pages.html books_data.js books_manifest.json \
  static-website-setup.html 2>/dev/null | awk '{printf "  %-35s %6s\n", $9, $5}'

TOTAL_SIZE=$(du -sh . 2>/dev/null | awk '{print $1}')
echo ""
echo "📊 Total repository size: $TOTAL_SIZE"
echo ""

# Step 6: Create index.html for GitHub Pages
echo "🔄 Step 6: Preparing index.html for GitHub Pages..."
cp index-github-pages.html index.html
echo "✅ index.html created from index-github-pages.html"
echo ""

# Step 7: Git operations
echo "📤 Step 7: Git operations..."
git add -A
git status --short | head -20

CHANGES=$(git status --short | wc -l)
echo ""
echo "📝 Changes to commit: $CHANGES files"
echo ""

read -p "💾 Commit and push to GitHub? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Committing changes..."
    git commit -m "Cleanup: Remove Flask files, optimize for static website GitHub Pages"
    
    echo "Pushing to GitHub..."
    git push origin main
    
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "📖 Next steps:"
    echo "  1. Go to GitHub repository settings"
    echo "  2. Pages → Source: main branch, / (root)"
    echo "  3. Website will be live at:"
    echo "     https://YOUR_USERNAME.github.io/ebooks/"
    echo ""
else
    echo "❌ Push cancelled (staged but not committed)"
    git reset
fi

echo "✨ Cleanup and optimization complete!"
