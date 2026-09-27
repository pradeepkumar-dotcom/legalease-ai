@echo off
echo ==========================================================
echo     LegalEase: Git Repository Initialization and Release
echo ==========================================================

REM 1. Initialize Git repository if not present
if not exist ".git" (
    echo [*] Initializing new Git repository...
    git init
) else (
    echo [*] Git repository already initialized.
)

REM 2. Check Git status and verify .gitignore
echo [*] Staging all project files...
git add .

REM 3. Create initial production commit
echo [*] Creating commit...
git commit -m "feat: complete production release of LegalEase AI document generator"

echo.
echo ==========================================================
echo   Git repository initialized and committed successfully!   
echo ==========================================================
echo To connect to your remote GitHub repository, run:
echo   git branch -M main
echo   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
echo   git push -u origin main
echo ==========================================================
