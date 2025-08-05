#!/bin/bash

# THOR Gamer OS - Ultimate Startup Script
# "Water Your Tree" - Complete Platform Launcher

echo "🌱 THOR Gamer OS Ultimate Startup Script 🌱"
echo "============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check if Python 3 is available
echo -e "${BLUE}🔍 Checking Python installation...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    echo -e "${GREEN}✅ Python 3 found: $(python3 --version)${NC}"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    echo -e "${GREEN}✅ Python found: $(python --version)${NC}"
else
    echo -e "${RED}❌ Python not found. Please install Python 3.7+${NC}"
    exit 1
fi

# Check if virtual environment exists
echo -e "${BLUE}🔍 Checking virtual environment...${NC}"
if [ -d ".venv" ]; then
    echo -e "${GREEN}✅ Virtual environment found${NC}"
    source .venv/bin/activate
    echo -e "${CYAN}📦 Activated virtual environment${NC}"
else
    echo -e "${YELLOW}⚠️  No virtual environment found${NC}"
    echo -e "${BLUE}🔧 Creating virtual environment...${NC}"
    
    $PYTHON_CMD -m venv .venv
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Virtual environment created${NC}"
        source .venv/bin/activate
        echo -e "${CYAN}📦 Activated virtual environment${NC}"
    else
        echo -e "${RED}❌ Failed to create virtual environment${NC}"
        echo -e "${YELLOW}⚠️  Continuing without virtual environment...${NC}"
    fi
fi

# Install/upgrade pip
echo -e "${BLUE}🔧 Ensuring pip is up to date...${NC}"
$PYTHON_CMD -m pip install --upgrade pip > /dev/null 2>&1

# Install required packages
echo -e "${BLUE}📦 Installing required packages...${NC}"

REQUIRED_PACKAGES=(
    "asyncio-mqtt"
    "aiohttp"
    "websockets"
    "cryptography"
    "Pillow"
    "requests"
    "psutil"
    "gitpython"
)

OPTIONAL_PACKAGES=(
    "numpy"
    "matplotlib"
    "beautifulsoup4"
    "lxml"
    "discord.py"
)

# Install required packages
for package in "${REQUIRED_PACKAGES[@]}"; do
    echo -e "${CYAN}📦 Installing $package...${NC}"
    $PYTHON_CMD -m pip install $package > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ $package installed${NC}"
    else
        echo -e "${YELLOW}⚠️  $package installation failed (will continue)${NC}"
    fi
done

# Install optional packages
echo -e "${BLUE}📦 Installing optional packages...${NC}"
for package in "${OPTIONAL_PACKAGES[@]}"; do
    echo -e "${CYAN}📦 Installing $package...${NC}"
    $PYTHON_CMD -m pip install $package > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ $package installed${NC}"
    else
        echo -e "${YELLOW}⚠️  $package installation failed (optional)${NC}"
    fi
done

# Create logs directory
mkdir -p logs

# Banner
echo -e "${PURPLE}"
echo "╔═══════════════════════════════════════════════════════════════════════════╗"
echo "║                          🌱 THOR GAMER OS 🌱                             ║"
echo "║                    Ultimate Platform Ready to Launch                     ║"
echo "║                                                                           ║"
echo "║  🎯 Complete Unified Developer & Gamer Platform                          ║"
echo "║  🌱 \"Water Your Tree\" - Repository Sync & Collaboration                 ║"
echo "║  🌐 P2P Cloud Network - Decentralized File Sharing                       ║"
echo "║  🤖 AI Content Generation - Text, Images, Guides                         ║"
echo "║  🎮 Universal Game Tracking - Cross-Platform Analytics                   ║"
echo "║  📚 Gaming Knowledge Base - \"Google of Gaming\"                          ║"
echo "║  🔧 Driver Optimization - Automated Performance Tuning                   ║"
echo "║  ⚡ Real-time Monitoring - System Health & Performance                   ║"
echo "║  🎨 Beautiful UI - Interactive Sync Interface                            ║"
echo "║  🔐 Privacy-First - GDPR/CCPA Compliant                                  ║"
echo "║                                                                           ║"
echo "║              🌳 \"The tree never minds, water is water\" 🌳                ║"
echo "╚═══════════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Menu system
while true; do
    echo -e "${CYAN}"
    echo "🎮 THOR Gamer OS Launch Menu:"
    echo "=============================="
    echo "1. 🚀 Launch Complete THOR Platform (Ultimate Launcher)"
    echo "2. 🌱 Launch \"Water Your Tree\" Sync UI Only"
    echo "3. 🌐 Launch P2P Network Only"
    echo "4. 🤖 Launch AI Content Creator Only"
    echo "5. 🎮 Launch Game Tracker Only"
    echo "6. 📚 Launch Knowledge Base Only"
    echo "7. 🔧 Launch Driver Manager Only"
    echo "8. 📊 System Status & Health Check"
    echo "9. 🎨 Create Demo Project"
    echo "10. 🧪 Run Integration Tests"
    echo "11. 📖 View Documentation"
    echo "12. 🛑 Exit"
    echo -e "${NC}"
    
    echo -n "Select option (1-12): "
    read choice
    
    case $choice in
        1)
            echo -e "${GREEN}🚀 Launching Complete THOR Platform...${NC}"
            $PYTHON_CMD thor_ultimate_launcher.py
            ;;
        2)
            echo -e "${GREEN}🌱 Launching Sync UI...${NC}"
            if [ -f "thor_sync_ui_system.py" ]; then
                $PYTHON_CMD thor_sync_ui_system.py
            else
                echo -e "${RED}❌ thor_sync_ui_system.py not found${NC}"
            fi
            ;;
        3)
            echo -e "${GREEN}🌐 Launching P2P Network...${NC}"
            if [ -f "thor_p2p_cloud_system.py" ]; then
                $PYTHON_CMD thor_p2p_cloud_system.py
            else
                echo -e "${RED}❌ thor_p2p_cloud_system.py not found${NC}"
            fi
            ;;
        4)
            echo -e "${GREEN}🤖 Launching AI Content Creator...${NC}"
            if [ -f "thor_ai_content_creator.py" ]; then
                $PYTHON_CMD thor_ai_content_creator.py
            else
                echo -e "${RED}❌ thor_ai_content_creator.py not found${NC}"
            fi
            ;;
        5)
            echo -e "${GREEN}🎮 Launching Game Tracker...${NC}"
            if [ -f "thor_game_tracker.py" ]; then
                $PYTHON_CMD thor_game_tracker.py
            else
                echo -e "${RED}❌ thor_game_tracker.py not found${NC}"
            fi
            ;;
        6)
            echo -e "${GREEN}📚 Launching Knowledge Base...${NC}"
            if [ -f "thor_knowledge_base.py" ]; then
                $PYTHON_CMD thor_knowledge_base.py
            else
                echo -e "${RED}❌ thor_knowledge_base.py not found${NC}"
            fi
            ;;
        7)
            echo -e "${GREEN}🔧 Launching Driver Manager...${NC}"
            if [ -f "thor_driver_manager.py" ]; then
                $PYTHON_CMD thor_driver_manager.py
            else
                echo -e "${RED}❌ thor_driver_manager.py not found${NC}"
            fi
            ;;
        8)
            echo -e "${GREEN}📊 System Status Check...${NC}"
            echo -e "${BLUE}🔍 Python Version: $($PYTHON_CMD --version)${NC}"
            echo -e "${BLUE}🔍 Working Directory: $(pwd)${NC}"
            echo -e "${BLUE}🔍 Available Files:${NC}"
            ls -la thor_*.py 2>/dev/null | head -10
            echo -e "${BLUE}🔍 System Memory:${NC}"
            if command -v free &> /dev/null; then
                free -h | head -2
            elif command -v vm_stat &> /dev/null; then
                vm_stat | head -5
            fi
            ;;
        9)
            echo -e "${GREEN}🎨 Creating Demo Project...${NC}"
            $PYTHON_CMD -c "
import os
from pathlib import Path

# Create demo project structure
demo_dir = Path('thor_demo_project')
demo_dir.mkdir(exist_ok=True)

files = {
    'README.md': '''# THOR Demo Project 🌱
    
Welcome to THOR Gamer OS demo!

## Features:
- Repository sync (\"Water your tree\")
- AI content generation
- P2P collaboration
- Game tracking
- Knowledge base

## Usage:
1. Open THOR Sync UI
2. Select this project
3. Click \"Water the Tree\" 🌱
4. Find the easter egg!
''',
    'demo_game.py': '''#!/usr/bin/env python3
print(\"🎮 THOR Demo Game Starting...\")
print(\"🌱 Connected to THOR Gamer OS\")
print(\"🌳 The tree never minds, water is water\")
''',
    'config.json': '''{
  \"name\": \"THOR Demo\",
  \"version\": \"1.0.0\",
  \"thor_features\": [\"sync\", \"ai\", \"p2p\", \"gaming\"]
}'''
}

for filename, content in files.items():
    with open(demo_dir / filename, 'w') as f:
        f.write(content)
    print(f'📄 Created: {filename}')

print('✅ Demo project created in thor_demo_project/')
"
            ;;
        10)
            echo -e "${GREEN}🧪 Running Integration Tests...${NC}"
            echo -e "${BLUE}🔍 Testing Python imports...${NC}"
            $PYTHON_CMD -c "
import sys
import asyncio
import json
import sqlite3
import pathlib
import datetime
import logging
import threading
import hashlib

try:
    import tkinter
    print('✅ tkinter available')
except ImportError:
    print('❌ tkinter not available')

try:
    import git
    print('✅ GitPython available')
except ImportError:
    print('⚠️  GitPython not available (optional)')

try:
    import websockets
    print('✅ websockets available')
except ImportError:
    print('⚠️  websockets not available (optional)')

try:
    import cryptography
    print('✅ cryptography available')
except ImportError:
    print('⚠️  cryptography not available (optional)')

print('🧪 Basic integration test completed')
"
            ;;
        11)
            echo -e "${GREEN}📖 THOR Gamer OS Documentation${NC}"
            echo -e "${BLUE}"
            echo "🌱 \"Water Your Tree\" Philosophy:"
            echo "   Every sync operation is like watering a tree"
            echo "   Your code grows and thrives through sharing"
            echo "   \"The tree never minds, water is water\""
            echo ""
            echo "🎯 Core Features:"
            echo "   • Repository Management & Sync"
            echo "   • P2P Cloud Collaboration"
            echo "   • AI Content Generation"
            echo "   • Universal Game Tracking"
            echo "   • Gaming Knowledge Base"
            echo "   • Automated Driver Updates"
            echo "   • Real-time Performance Monitoring"
            echo ""
            echo "🎨 UI Features:"
            echo "   • Interactive sync interface"
            echo "   • File selection with AI recommendations"
            echo "   • Progress tracking with animations"
            echo "   • Hidden easter egg (find the pixel!)"
            echo ""
            echo "🔐 Privacy Features:"
            echo "   • GDPR/CCPA compliant"
            echo "   • Local-first architecture"
            echo "   • End-to-end encryption"
            echo "   • Anonymous by default"
            echo -e "${NC}"
            ;;
        12)
            echo -e "${GREEN}🌳 Thank you for using THOR Gamer OS!${NC}"
            echo -e "${CYAN}🌱 Remember: The tree never minds, water is water${NC}"
            break
            ;;
        *)
            echo -e "${RED}❌ Invalid option. Please choose 1-12.${NC}"
            ;;
    esac
    
    echo ""
    echo -n "Press Enter to continue..."
    read
    clear
done

echo -e "${GREEN}🌱 THOR Gamer OS session ended. Keep growing! 🌳${NC}"
