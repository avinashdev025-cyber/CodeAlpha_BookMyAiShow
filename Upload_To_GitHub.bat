@echo off
title BookMyAiShow GitHub Uploader
color 0C

echo ===================================================
echo     BookMyAiShow GitHub Uploader
echo ===================================================
echo.
echo Step 1: We are opening GitHub in your browser.
echo Please create a new repository named: CodeAlpha_BookMyAiShow
echo (Leave everything else as it is and click "Create repository")
echo.
start https://github.com/new
echo Press any key in this window AFTER you have created the repository on GitHub...
pause >nul
echo.
set /p username="Step 2: Enter your GitHub Username: "
echo.
echo Step 3: Connecting local code to GitHub...
git remote remove origin >nul 2>&1
git remote add origin https://github.com/%username%/CodeAlpha_BookMyAiShow.git
git branch -M main
echo.
echo Step 4: Uploading your code...
echo (A popup window will appear asking you to log in to GitHub. Please click "Sign in with your browser".)
echo.
git push -u origin main
echo.
echo ===================================================
echo SUCCESS! Your sharing link is:
echo https://github.com/%username%/CodeAlpha_BookMyAiShow
echo ===================================================
echo.
pause
