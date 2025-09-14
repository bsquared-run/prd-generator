#!/usr/bin/env python3
"""
Build script for creating PRD Generator executables

This script creates standalone Windows executables for both the core
and enhanced versions of the PRD Generator.
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔨 {description}")
    print(f"Running: {command}")

    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✅ {description} completed successfully")
        return True
    else:
        print(f"❌ {description} failed")
        print(f"Error: {result.stderr}")
        return False

def create_core_executable():
    """Create executable for core PRD Generator"""
    print("\n" + "="*60)
    print("Creating Core PRD Generator Executable")
    print("="*60)

    # PyInstaller command for core application
    command = [
        "pyinstaller",
        "--onefile",                    # Single executable file
        "--windowed",                   # No console window (GUI app)
        "--name=PRD_Generator",         # Output name
        "--icon=NONE",                  # No icon (could add later)
        "--add-data=sample_user_stories.txt;.",  # Include sample data
        "--hidden-import=customtkinter",
        "--hidden-import=reportlab",
        "--hidden-import=tkinter",
        "prd_generator.py"
    ]

    return run_command(" ".join(command), "Building core PRD Generator executable")

def create_enhanced_executable():
    """Create executable for enhanced AI version"""
    print("\n" + "="*60)
    print("Creating Enhanced AI PRD Generator Executable")
    print("="*60)

    # Note: Enhanced version requires MCP server dependencies
    # For now, we'll create a version that works without MCP server running
    command = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=PRD_Generator_Enhanced",
        "--icon=NONE",
        "--add-data=sample_user_stories.txt;.",
        "--add-data=mcp-server;mcp-server",     # Include MCP server files
        "--hidden-import=customtkinter",
        "--hidden-import=reportlab",
        "--hidden-import=tkinter",
        "--hidden-import=asyncio",
        "--hidden-import=requests",
        # Note: MCP dependencies might cause issues, so we'll try core first
        "prd_generator.py"  # Use core version for now
    ]

    return run_command(" ".join(command), "Building enhanced PRD Generator executable")

def create_batch_launcher():
    """Create a batch file launcher for the MCP server"""
    batch_content = '''@echo off
echo Starting PRD Generator MCP Server...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.7+ to use the MCP server
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking dependencies...
python -c "import mcp, requests, asyncio" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing MCP server dependencies...
    pip install -r mcp-server/requirements.txt
    if %errorlevel% neq 0 (
        echo Failed to install dependencies
        pause
        exit /b 1
    )
)

echo Starting MCP server...
cd mcp-server
python server.py

pause
'''

    with open("dist/Start_MCP_Server.bat", "w") as f:
        f.write(batch_content)

    print("✅ Created MCP server launcher batch file")

def create_release_package():
    """Create a complete release package"""
    print("\n" + "="*60)
    print("Creating Release Package")
    print("="*60)

    # Create release directory structure
    release_dir = Path("release")
    release_dir.mkdir(exist_ok=True)

    # Copy executables if they exist
    dist_dir = Path("dist")
    if dist_dir.exists():
        for exe_file in dist_dir.glob("*.exe"):
            target = release_dir / exe_file.name
            subprocess.run(f'copy "{exe_file}" "{target}"', shell=True)
            print(f"✅ Copied {exe_file.name} to release package")

        # Copy batch file if it exists
        batch_file = dist_dir / "Start_MCP_Server.bat"
        if batch_file.exists():
            target = release_dir / batch_file.name
            subprocess.run(f'copy "{batch_file}" "{target}"', shell=True)
            print(f"✅ Copied {batch_file.name} to release package")

    # Copy essential files
    essential_files = [
        "README.md",
        "sample_user_stories.txt",
        "requirements.txt"
    ]

    for file_name in essential_files:
        if Path(file_name).exists():
            target = release_dir / file_name
            subprocess.run(f'copy "{file_name}" "{target}"', shell=True)
            print(f"✅ Copied {file_name} to release package")

    # Copy MCP server directory
    mcp_source = Path("mcp-server")
    mcp_target = release_dir / "mcp-server"
    if mcp_source.exists():
        subprocess.run(f'xcopy "{mcp_source}" "{mcp_target}" /E /I /Y', shell=True)
        print(f"✅ Copied MCP server files to release package")

    # Create README for release
    release_readme = '''# PRD Generator - Release Package

This package contains the PRD Generator application in multiple formats:

## Files Included:
- `PRD_Generator.exe` - Standalone executable (no Python required)
- `sample_user_stories.txt` - Example user stories for testing
- `README.md` - Full documentation
- `requirements.txt` - Python dependencies (if running from source)
- `mcp-server/` - AI enhancement server (requires Python)
- `Start_MCP_Server.bat` - Easy MCP server launcher

## Quick Start:
1. **Simple Usage**: Just run `PRD_Generator.exe`
2. **AI-Enhanced**: Run `Start_MCP_Server.bat` first, then use the enhanced features

## System Requirements:
- Windows 10 or later
- For MCP server: Python 3.7+ (optional, for AI features)

## Usage:
1. Run the executable
2. Enter your user stories
3. Click "Parse Stories"
4. Fill in project information
5. Click "Generate PRD"
6. Export as PDF or text

For full documentation, see README.md or visit:
https://github.com/bsquared-run/prd-generator
'''

    with open(release_dir / "README_RELEASE.md", "w") as f:
        f.write(release_readme)

    print("✅ Created release README")
    print(f"\n📦 Release package created in: {release_dir.absolute()}")

def main():
    """Main build process"""
    print("🚀 PRD Generator Executable Build Process")
    print("=" * 60)

    # Change to project directory
    os.chdir(Path(__file__).parent)

    # Clean previous builds
    if Path("dist").exists():
        subprocess.run("rmdir /S /Q dist", shell=True)
    if Path("build").exists():
        subprocess.run("rmdir /S /Q build", shell=True)

    success_count = 0

    # Build core executable
    if create_core_executable():
        success_count += 1

        # Create batch launcher after successful build
        os.makedirs("dist", exist_ok=True)
        create_batch_launcher()

    # Create release package
    create_release_package()

    print("\n" + "=" * 60)
    print("BUILD SUMMARY")
    print("=" * 60)

    if success_count > 0:
        print(f"✅ Successfully created {success_count} executable(s)")
        print("📦 Release package created in 'release/' directory")
        print("\n🎯 Next steps:")
        print("1. Test the executable(s)")
        print("2. Create GitHub release")
        print("3. Upload release package as assets")
    else:
        print("❌ No executables were created successfully")
        print("Check the error messages above")

    return success_count > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)