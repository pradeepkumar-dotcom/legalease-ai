#!/usr/bin/env bash
# LegalEase Git Repository Initialization & Release Script

echo "=========================================================="
echo "    LegalEase: Git Repository Initialization & Release    "
echo "=========================================================="

# 1. Initialize Git repository if not present
if [ ! -d ".git" ]; then
    echo "[*] Initializing new Git repository..."
    git init
else
    echo "[*] Git repository already initialized."
fi

# 2. Stage all project files adhering to .gitignore
echo "[*] Staging all project files..."
git add .

# 3. Create initial production commit
echo "[*] Creating production release commit..."
git commit -m "feat: complete production release of LegalEase AI document generator"

echo ""
echo "=========================================================="
echo "  Git repository initialized & committed successfully!   "
echo "=========================================================="
echo "To connect to your remote GitHub repository, run:"
echo "  git branch -M main"
echo "  git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git"
echo "  git push -u origin main"
echo "=========================================================="
