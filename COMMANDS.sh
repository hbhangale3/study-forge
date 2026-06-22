#!/bin/bash
# StudyForge Command Reference
# Run these commands in your terminal to manage the app

# ============================================
# FIRST TIME SETUP
# ============================================

# Create virtual environment
python3 -m venv venv

# Activate virtual environment (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file for Groq API (optional)
cp .env.example .env


# ============================================
# START THE APP
# ============================================

# Standard start (with venv activation)
source venv/bin/activate && python app.py

# Or if venv already activated:
python app.py

# Visit: http://localhost:3000


# ============================================
# STOP THE APP
# ============================================

# Option 1: Interactive stop (if running in foreground)
# Just press: Ctrl+C in the terminal


# Option 2: Kill by process name (simple)
pkill -f "python app.py"


# Option 3: Kill by port (if stuck)
lsof -i :3000 | grep -v COMMAND | awk '{print $2}' | xargs kill -9


# Option 4: Kill by specific PID
# First find PID: ps aux | grep "python app.py"
# Then kill:
kill -9 <PID>


# ============================================
# RESTART THE APP
# ============================================

# Quick restart (all in one)
pkill -f "python app.py" && sleep 2 && source venv/bin/activate && python app.py


# ============================================
# CHECK APP STATUS
# ============================================

# Check if port 3000 is in use
lsof -i :3000

# List all Python processes
ps aux | grep python

# Check if venv is activated
which python


# ============================================
# TROUBLESHOOTING
# ============================================

# Reinstall all dependencies (clean install)
pip install --upgrade --force-reinstall -r requirements.txt

# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +
find . -name "*.pyc" -delete

# Check Python version
python --version

# Verify Flask installation
python -c "import flask; print(f'Flask version: {flask.__version__}')"


# ============================================
# DEVELOPMENT
# ============================================

# Run app in background (macOS/Linux)
source venv/bin/activate && python app.py &

# View recent log (if you want to add logging)
# tail -f app.log


# ============================================
# GIT
# ============================================

# Initialize git (if not done)
git init

# Check what will be ignored
cat .gitignore

# Stage all files (ignores .gitignore patterns)
git add .

# Commit
git commit -m "Initial StudyForge setup"

# Push to remote
git push origin main
