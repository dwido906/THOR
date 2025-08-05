#!/usr/bin/env python3
"""
THOR & ODIN: Simple Integration Launcher
ONE MAN ARMY EDITION - Ultimate Developer & Gamer Platform

This script launches both THOR OS and ODIN systems together.
Simplified version with robust error handling.
"""

import os
import sys
import time
import logging
import subprocess
from pathlib import Path
from datetime import datetime

def print_integration_banner():
    """Print the ultimate integration banner"""
    banner = f"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                    ⚡ THOR & ODIN INTEGRATION ⚡                          ║
║                    ONE MAN ARMY ULTIMATE EDITION                          ║
║                                                                           ║
║    🌱 THOR OS                           👁️ ODIN SYSTEM                    ║
║    ─────────                           ──────────────                    ║
║    • Local Hosting & Repo Sync        • System Monitoring                ║
║    • "Water Your Tree" Philosophy     • Knowledge Base                   ║
║    • P2P Cloud Collaboration          • Driver Management                ║
║    • AI-Powered Development           • Cloud Orchestration              ║
║    • Universal Game Tracking          • Security & Firewall              ║
║    • Privacy-First Design             • Cost Optimization                ║
║                                                                           ║
║                    🤝 PERFECT INTEGRATION 🤝                             ║
║                                                                           ║
║  🎯 Complete Developer & Gamer Platform                                  ║
║  🌐 Local + Cloud Hybrid Architecture                                    ║
║  🔐 End-to-End Security & Privacy                                        ║
║  💰 Cost-Optimized Cloud Resources                                       ║
║  🤖 AI-Assisted Everything                                               ║
║  🌳 Growth-Oriented Philosophy                                           ║
║                                                                           ║
║  🌱 "The tree never minds, water is water"                               ║
║  👁️ "The All-Father watches over all THOR instances"                     ║
╚═══════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_system_requirements():
    """Check basic system requirements"""
    print("🔍 Checking system requirements...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version < (3, 7):
        print("❌ Python 3.7+ required")
        return False
    else:
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check if THOR and ODIN files exist
    thor_file = Path("thor_os_one_man_army.py")
    odin_file = Path("odin_all_father.py")
    
    if not thor_file.exists():
        print("❌ thor_os_one_man_army.py not found")
        return False
    else:
        print("✅ THOR OS file found")
    
    if not odin_file.exists():
        print("❌ odin_all_father.py not found")
        return False
    else:
        print("✅ ODIN file found")
    
    return True

def run_thor_os():
    """Run THOR OS"""
    print("🌱 Launching THOR OS...")
    try:
        subprocess.run([sys.executable, "thor_os_one_man_army.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ THOR OS failed to run: {e}")
    except KeyboardInterrupt:
        print("🛑 THOR OS interrupted by user")

def run_odin_system():
    """Run ODIN System"""
    print("👁️ Launching ODIN...")
    try:
        subprocess.run([sys.executable, "odin_all_father.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ ODIN failed to run: {e}")
    except KeyboardInterrupt:
        print("🛑 ODIN interrupted by user")

def run_both_parallel():
    """Run both systems in parallel"""
    print("🤝 Starting both THOR and ODIN in parallel...")
    print("💡 Use Ctrl+C to stop both systems")
    
    import threading
    
    # Start THOR in background thread
    thor_thread = threading.Thread(target=run_thor_os, daemon=True)
    odin_thread = threading.Thread(target=run_odin_system, daemon=True)
    
    thor_thread.start()
    time.sleep(2)  # Give THOR a head start
    odin_thread.start()
    
    try:
        # Keep main thread alive
        while thor_thread.is_alive() or odin_thread.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping both systems...")

def create_docker_setup():
    """Create Docker setup files"""
    print("🐳 Creating Docker configuration...")
    
    # Simple docker-compose.yml
    docker_compose = """version: '3.8'

services:
  thor-os:
    build:
      context: .
      dockerfile: Dockerfile.thor
    container_name: thor-os-one-man-army
    ports:
      - "8080:8080"
      - "8888:8888"
    volumes:
      - thor_data:/app/data
      - ./thor_os_one_man_army.py:/app/thor_os_one_man_army.py
    restart: unless-stopped
    networks:
      - thor-odin-network

  odin-system:
    build:
      context: .
      dockerfile: Dockerfile.odin
    container_name: odin-all-father
    ports:
      - "9090:9090"
    volumes:
      - odin_data:/app/data
      - ./odin_all_father.py:/app/odin_all_father.py
    environment:
      - VULTR_API_KEY=${VULTR_API_KEY}
    restart: unless-stopped
    networks:
      - thor-odin-network
    depends_on:
      - thor-os

volumes:
  thor_data:
  odin_data:

networks:
  thor-odin-network:
    driver: bridge
"""
    
    # Simple Dockerfile for THOR
    thor_dockerfile = """FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY thor_os_one_man_army.py .

RUN pip install asyncio sqlite3 tkinter

EXPOSE 8080 8888

CMD ["python", "thor_os_one_man_army.py"]
"""
    
    # Simple Dockerfile for ODIN
    odin_dockerfile = """FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY odin_all_father.py .

RUN pip install requests psutil schedule

EXPOSE 9090

CMD ["python", "odin_all_father.py"]
"""
    
    # Write files
    Path("docker-compose.yml").write_text(docker_compose)
    Path("Dockerfile.thor").write_text(thor_dockerfile)
    Path("Dockerfile.odin").write_text(odin_dockerfile)
    
    print("✅ Docker configuration created!")
    print("💡 Run 'docker-compose up' to start containerized systems")

def deploy_to_vultr():
    """Simple Vultr deployment instructions"""
    print("☁️ Vultr Deployment Instructions:")
    print("""
1. Create a Vultr account and get API key
2. Set environment variable: export VULTR_API_KEY=your_key_here
3. Use the ODIN system to deploy to cloud
4. Or manually create a server and copy files:
   
   # Create server on Vultr
   # SSH into server
   ssh root@your_server_ip
   
   # Install requirements
   apt update && apt install python3 python3-pip git -y
   
   # Clone your repository or copy files
   git clone your_repo_url
   cd your_repo
   
   # Run THOR + ODIN
   python3 thor_odin_integration.py
""")

def integration_menu():
    """Main integration menu"""
    while True:
        print("\n" + "="*80)
        print("⚡ THOR & ODIN INTEGRATION - Main Menu")
        print("="*80)
        print("1. 🌱 Launch THOR OS Only")
        print("2. 👁️ Launch ODIN Only")
        print("3. 🤝 Run Both Systems in Parallel")
        print("4. 🐳 Create Docker Configuration")
        print("5. ☁️ Show Vultr Deployment Instructions")
        print("6. 📊 System Status")
        print("7. 🛑 Exit")
        print()
        
        choice = input("Select option (1-7): ").strip()
        
        if choice == "1":
            run_thor_os()
            
        elif choice == "2":
            run_odin_system()
            
        elif choice == "3":
            run_both_parallel()
            
        elif choice == "4":
            create_docker_setup()
            
        elif choice == "5":
            deploy_to_vultr()
            
        elif choice == "6":
            print("📊 System Status:")
            print(f"✅ THOR OS file: {'Found' if Path('thor_os_one_man_army.py').exists() else 'Missing'}")
            print(f"✅ ODIN file: {'Found' if Path('odin_all_father.py').exists() else 'Missing'}")
            print(f"✅ Python version: {sys.version}")
            print(f"✅ Working directory: {Path.cwd()}")
            print(f"✅ Vultr API key: {'Set' if os.getenv('VULTR_API_KEY') else 'Not set'}")
            
        elif choice == "7":
            print("🛑 Goodbye! May your tree grow tall! 🌱")
            break
            
        else:
            print("❌ Invalid choice. Please select 1-7.")
        
        if choice != "7":
            input("\nPress Enter to continue...")

def main():
    """Main entry point"""
    print("⚡ THOR & ODIN Integration Starting...")
    
    # Print banner
    print_integration_banner()
    
    # Check requirements
    if not check_system_requirements():
        print("❌ System requirements not met.")
        return False
    
    # Show environment info
    vultr_api_key = os.getenv('VULTR_API_KEY')
    if not vultr_api_key:
        print("💡 Tip: Set VULTR_API_KEY environment variable for cloud features")
        print("💡 You can still use all local features without it")
    else:
        print("✅ Vultr API key detected")
    
    print("\n🌟 Welcome to the ONE MAN ARMY EDITION!")
    print("🌱 Ready to water your tree of knowledge!")
    print("👁️ The All-Father watches over all...")
    
    try:
        # Run integration menu
        integration_menu()
        return True
        
    except KeyboardInterrupt:
        print("\n🛑 Integration cancelled by user")
        return False
    except Exception as e:
        print(f"\n💥 Critical integration error: {e}")
        return False

if __name__ == "__main__":
    main()
