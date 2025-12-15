@echo off
REM Batch script to run Git Bash upload script
echo Starting Git Bash upload script...
echo.

REM Try to find Git Bash
if exist "C:\Program Files\Git\bin\bash.exe" (
    "C:\Program Files\Git\bin\bash.exe" upload-with-git-bash.sh
) else if exist "C:\Program Files (x86)\Git\bin\bash.exe" (
    "C:\Program Files (x86)\Git\bin\bash.exe" upload-with-git-bash.sh
) else (
    echo Git Bash not found in default locations.
    echo Please run this script from Git Bash directly:
    echo   bash upload-with-git-bash.sh
    pause
)

