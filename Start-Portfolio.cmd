@echo off
cd /d "%~dp0"
where node >nul 2>nul
if errorlevel 1 (
  echo Node.js is required to run the enquiry form.
  pause
  exit /b 1
)
echo Open http://localhost:3000 in your browser.
echo Keep this window open while the site is running.
node server.mjs
pause
