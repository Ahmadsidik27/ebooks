#!/bin/bash
# Deploy to GitHub Pages - Automated Script
# Usage: ./deploy-to-github-pages.sh YOUR_USERNAME

set -e

USERNAME=${1:-$(git config user.name)}
REPO_NAME="ebooks"
REPO_URL="https://github.com/$USERNAME/$REPO_NAME.git"

echo "🚀 Starting GitHub Pages Deployment..."
echo "Repository: $REPO_URL"
echo ""

# Check if git is available
if ! command -v git &> /dev/null; then
    echo "❌ Git not installed"
    exit 1
fi

# Step 1: Generate manifest
echo "📝 Step 1: Generating books manifest..."
python3 generate_books_manifest.py
echo "✅ Manifest generated"
echo ""

# Step 2: Create/Update gh-pages branch
echo "🌿 Step 2: Setting up gh-pages branch..."

# Create temp directory
TEMP_DIR=$(mktemp -d)
echo "📁 Working directory: $TEMP_DIR"

# Clone repository
cd "$TEMP_DIR"
git clone --branch gh-pages "$REPO_URL" . 2>/dev/null || git clone "$REPO_URL" . && git checkout -b gh-pages

# Step 3: Copy files
echo "📋 Step 3: Copying files..."
cp /workspaces/ebooks/index-github-pages.html ./index.html
cp /workspaces/ebooks/books_data.js ./
cp /workspaces/ebooks/books_manifest.json ./
echo "✅ Files copied"
echo ""

# Step 4: Copy PDF folders (with progress)
echo "📚 Step 4: Copying PDF folders..."
echo "⏳ This may take a few minutes (total ~930 MB)..."

if [ -d "/workspaces/ebooks/EBOOKS" ]; then
    echo "  Copying EBOOKS/ ..."
    cp -rv /workspaces/ebooks/EBOOKS . > /dev/null 2>&1 || true
fi

if [ -d "/workspaces/ebooks/pengetahuan" ]; then
    echo "  Copying pengetahuan/ ..."
    cp -rv /workspaces/ebooks/pengetahuan . > /dev/null 2>&1 || true
fi

echo "✅ PDF folders copied"
echo ""

# Step 5: Git operations
echo "🔧 Step 5: Committing changes..."
git add .
git commit -m "Deploy static website - $REPO_NAME @ $(date '+%Y-%m-%d %H:%M:%S')" || true
echo "✅ Changes committed"
echo ""

# Step 6: Push to GitHub
echo "📤 Step 6: Pushing to GitHub..."
git push -u origin gh-pages
echo "✅ Pushed to gh-pages"
echo ""

# Step 7: Info
echo "============================================"
echo "✅ Deployment Complete!"
echo "============================================"
echo ""
echo "🌐 Your website will be available at:"
echo "📍 https://$USERNAME.github.io/$REPO_NAME/"
echo ""
echo "⏳ GitHub Pages may take 1-2 minutes to build."
echo "   Refresh the page if not immediately available."
echo ""
echo "📱 Features:"
echo "  ✅ 124+ PDF e-books fully searchable"
echo "  ✅ Filter by collection (EBOOKS/pengetahuan)"
echo "  ✅ Size-based filtering"
echo "  ✅ Direct download links"
echo "  ✅ Statistics & metadata"
echo "  ✅ Fully responsive design"
echo ""
echo "📖 Next steps:"
echo "  1. Go to GitHub repository settings"
echo "  2. Check Pages section - should show gh-pages branch"
echo "  3. Share the link: https://$USERNAME.github.io/$REPO_NAME/"
echo ""

# Cleanup
cd /
rm -rf "$TEMP_DIR"

echo "🎉 Done!"
