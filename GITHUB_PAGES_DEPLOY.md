# Panduan Deploy Static Website ke GitHub Pages

## 📋 Persiapan

Pastikan Anda sudah setup GitHub repository. Jika belum:

```bash
cd /workspaces/ebooks
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/ebooks.git
git branch -M main
git push -u origin main
```

## 🚀 Step-by-Step Deployment

### Step 1: Siapkan Branch gh-pages

```bash
# Create and checkout gh-pages branch
git checkout --orphan gh-pages

# Clear working directory
git rm -rf .

# Create minimal files untuk GitHub Pages
git add .
git commit --allow-empty -m "Init gh-pages"
git push origin gh-pages
```

### Step 2: Setup GitHub Pages Settings

1. Buka repository di GitHub
2. Masuk ke **Settings → Pages**
3. **Source**: Select `gh-pages` branch
4. **Folder**: Select `/ (root)`
5. Klik **Save**

GitHub akan memberi URL: `https://YOUR_USERNAME.github.io/ebooks/`

### Step 3: Copy Static Files ke gh-pages Branch

Gunakan script ini untuk auto-copy:

```bash
#!/bin/bash
# Copy static files ke gh-pages branch

# Go to repo root
cd /workspaces/ebooks

# Create temp directory
mkdir -p /tmp/gh-pages-build
cd /tmp/gh-pages-build

# Clone into fresh directory
git clone --branch gh-pages https://github.com/YOUR_USERNAME/ebooks.git .

# Copy static files
cp /workspaces/ebooks/index-github-pages.html ./index.html
cp /workspaces/ebooks/books_data.js ./
cp /workspaces/ebooks/books_manifest.json ./

# Copy PDF folders (symlink atau copy)
# Option 1: Copy all (warning: besar ~930MB)
# cp -r /workspaces/ebooks/EBOOKS ./
# cp -r /workspaces/ebooks/pengetahuan ./

# Option 2: Gunakan Git LFS untuk PDF besar
# (Lihat section "Large Files" di bawah)

# Commit and push
git add .
git commit -m "Deploy static website with books data"
git push origin gh-pages

cd /workspaces/ebooks
```

### Step 4: Update Manifest Secara Regular

```bash
# Setiap kali ada perubahan:
python3 generate_books_manifest.py
cp books_data.js /tmp/gh-pages-build/
cp books_manifest.json /tmp/gh-pages-build/
cd /tmp/gh-pages-build
git add .
git commit -m "Update books manifest"
git push origin gh-pages
```

## 📦 Opsi: Hosting PDF dengan Git LFS

Jika ingin include PDF files (rekomendasi untuk koleksi besar):

### Install Git LFS

```bash
sudo apt-get install git-lfs
git lfs install
```

### Track PDF Files

```bash
cd /workspaces/ebooks
git lfs track "*.pdf"
echo ".gitattributes" >> .gitignore
```

### Add PDF Folders

```bash
git add EBOOKS/ pengetahuan/
git commit -m "Add PDF files with Git LFS"
git push origin main

# Push to gh-pages
git checkout gh-pages
git merge main
git push origin gh-pages
```

## 🗂️ Alternative: Hosting di Subdirectory

Jika repo bukan user/org site (contoh: `github.com/USERNAME/ebooks`):

Update `index-github-pages.html`:

```javascript
// Change download paths
const basePath = '/ebooks/'; // Add basePath

// Update book paths
book.path = basePath + book.path; // e.g., /ebooks/EBOOKS/file.pdf
```

## ✅ Verify Deployment

```bash
# Test locally sebelum push
python3 -m http.server 8000 --directory /tmp/gh-pages-build

# Akses: http://localhost:8000/index.html
```

Kunjungi: `https://YOUR_USERNAME.github.io/ebooks/`

## 📊 Pilihan Struktur Repository

### Option A: All-in-One (Rekomendasi untuk koleksi Anda)

```
main branch:
├── EBOOKS/                    ✅ Include PDF (573 MB)
├── pengetahuan/               ✅ Include PDF (362 MB)
├── books_data.js              
├── books_manifest.json        
├── index-github-pages.html    
└── README.md

gh-pages branch:
├── index.html                 (copy dari index-github-pages.html)
├── books_data.js              
├── books_manifest.json        
├── EBOOKS/                    (symlink atau copy)
└── pengetahuan/               (symlink atau copy)
```

**Pros:** Simple, PDFs directly served  
**Cons:** Large repo size (~930 MB)

### Option B: Data Separated (Advanced)

```
main branch:
├── index-github-pages.html
├── books_data.js
└── README.md

gh-pages branch:
├── index.html
├── books_data.js
└── EBOOKS/, pengetahuan/

Hosting PDF:
- AWS S3
- Cloudflare R2
- Google Drive
- atau external URL
```

**Pros:** Kleiner repo size  
**Cons:** Perlu setup external hosting

## 🔄 CI/CD Automation (Optional)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Generate manifest
        run: |
          python3 generate_books_manifest.py
      
      - name: Deploy to gh-pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./
          include_files: |
            index-github-pages.html=index.html
            books_data.js
            books_manifest.json
            EBOOKS/
            pengetahuan/
```

## 🌐 Custom Domain

Jika ingin custom domain (contoh: ebooks.yourdomain.com):

1. Update DNS settings:
   - Add CNAME record: `ebook-github.yourdomain.com` → `USERNAME.github.io`

2. Repository Settings → Pages → Custom domain
   - Input: `ebooks.yourdomain.com`

## 📈 Performance Tips

1. **Compress PDFs** sebelum add ke repo:
   ```bash
   gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 \
      -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET -dBATCH \
      -sOutputFile=output.pdf input.pdf
   ```

2. **Gunakan CDN** untuk serve static assets:
   - Cloudflare Pages
   - Netlify
   - Vercel

3. **Lazy load** PDFs jika banyak

4. **Optimize manifest.json** - gzip compression

## 🐛 Troubleshooting

**Problem:** PDF files not downloading  
**Solution:** Ensure `raw.githubusercontent.com` accessible; check CORS settings

**Problem:** Site not loading  
**Solution:** 
- Check branch is set to `gh-pages`
- Verify index.html exists in root
- Clear browser cache

**Problem:** Paths broken  
**Solution:** Update base paths in index-github-pages.html

## 📱 Testing Locally

```bash
# Method 1: Python
python3 -m http.server 8000 --directory /workspaces/ebooks

# Method 2: Node.js (recommended)
npm install -g http-server
http-server /workspaces/ebooks -p 8000

# Method 3: Live Server (VS Code extension)
# Install "Live Server" extension dan klik "Go Live"
```

Akses: `http://localhost:8000/index-github-pages.html`

## ✨ Final Checklist

- ✅ `index-github-pages.html` di root
- ✅ `books_data.js` tergenerate
- ✅ `books_manifest.json` updated
- ✅ EBOOKS folder ter-include
- ✅ pengetahuan folder ter-include
- ✅ gh-pages branch created
- ✅ GitHub Pages settings configured
- ✅ Deploy sukses di domain

---

**Selesai! Website Anda sekarang live di GitHub Pages! 🎉**
