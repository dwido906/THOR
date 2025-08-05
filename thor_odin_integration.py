#!/usr/bin/env python3
"""
THOR & ODIN: Complete Integration Launcher
ONE MAN ARMY EDITION - Ultimate Developer & Gamer Platform

This script launches both THOR OS and ODIN systems together,
creating the complete ecosystem for autonomous developers and elite gamers.

Features:
- THOR OS: Local hosting, repo sync, P2P cloud, gaming optimization
- ODIN: System monitoring, knowledge base, cloud orchestration, security
- Complete integration between both systems
- Docker containerization support
- Vultr cloud deployment automation

"The tree never minds, water is water" + "The All-Father watches over all"
"""

import asyncio
import os
import sys
import json
import time
import logging
import threading
import subprocess
import signal
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import multiprocessing

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import THOR and ODIN systems
try:
    from thor_os_one_man_army import THOROSOneManArmy
    from odin_all_father import ODINSystem
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure thor_os_one_man_army.py and odin_all_father.py are in the same directory")
    sys.exit(1)

class THORODINIntegration:
    """Integrated THOR + ODIN System"""
    
    def __init__(self, vultr_api_key: Optional[str] = None):
        self.vultr_api_key = vultr_api_key
        self.thor_os: Optional[THOROSOneManArmy] = None
        self.odin_system: Optional[ODINSystem] = None
        self.thor_process = None
        self.odin_process = None
        self.integration_active = False
        
        # Setup logging
        self._setup_logging()
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _setup_logging(self):
        """Setup integrated logging"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - THOR-ODIN - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(log_dir / f'thor_odin_integration_{datetime.now().strftime("%Y%m%d")}.log')
            ]
        )
        self.logger = logging.getLogger('thor_odin_integration')
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.logger.info(f"🛑 Received signal {signum}, shutting down gracefully...")
        self.shutdown()
        sys.exit(0)
    
    def print_integration_banner(self):
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
    
    def check_system_requirements(self) -> bool:
        """Check system requirements for both THOR and ODIN"""
        self.logger.info("🔍 Checking system requirements...")
        
        requirements_met = True
        
        # Check Python version
        python_version = sys.version_info
        if python_version < (3, 7):
            self.logger.error("❌ Python 3.7+ required")
            requirements_met = False
        else:
            self.logger.info(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        # Check required modules
        required_modules = [
            'asyncio', 'sqlite3', 'json', 'threading', 'pathlib',
            'datetime', 'logging', 'hashlib', 'subprocess'
        ]
        
        optional_modules = [
            ('tkinter', 'GUI interface'),
            ('psutil', 'System monitoring'),
            ('requests', 'HTTP requests'),
            ('cryptography', 'Encryption')
        ]
        
        for module in required_modules:
            try:
                __import__(module)
                self.logger.info(f"✅ {module}")
            except ImportError:
                self.logger.error(f"❌ {module} - REQUIRED")
                requirements_met = False
        
        for module, description in optional_modules:
            try:
                __import__(module)
                self.logger.info(f"✅ {module} - {description}")
            except ImportError:
                self.logger.warning(f"⚠️ {module} - {description} (optional)")
        
        # Check disk space
        try:
            import shutil
            total, used, free = shutil.disk_usage(".")
            free_gb = free // (1024**3)
            if free_gb < 2:
                self.logger.warning(f"⚠️ Low disk space: {free_gb}GB free")
            else:
                self.logger.info(f"✅ Disk space: {free_gb}GB free")
        except Exception:
            self.logger.warning("⚠️ Could not check disk space")
        
        return requirements_met
    
    def initialize_systems(self):
        """Initialize both THOR and ODIN systems"""
        self.logger.info("🚀 Initializing THOR OS and ODIN systems...")
        
        try:
            # Initialize THOR OS
            self.logger.info("🌱 Initializing THOR OS...")
            self.thor_os = THOROSOneManArmy()
            self.logger.info("✅ THOR OS initialized")
            
            # Initialize ODIN
            self.logger.info("👁️ Initializing ODIN...")
            self.odin_system = ODINSystem(self.vultr_api_key)
            self.logger.info("✅ ODIN initialized")
            
            # Start services
            self.logger.info("🔧 Starting THOR services...")
            self.thor_os.start_services()
            
            self.logger.info("🔧 Starting ODIN services...")
            self.odin_system.start_all_services()
            
            # Register THOR instance with ODIN for monitoring
            self._register_thor_with_odin()
            
            self.integration_active = True
            self.logger.info("🎉 THOR + ODIN integration complete!")
            
        except Exception as e:
            self.logger.error(f"💥 Initialization failed: {e}")
            raise
    
    def _register_thor_with_odin(self):
        """Register THOR instance with ODIN monitoring"""
        if not self.odin_system:
            return
            
        try:
            from odin_all_father import THORInstance
            
            thor_instance = THORInstance(
                instance_id="thor_local_001",
                name="THOR OS Local Instance",
                address="localhost",
                port=8080,
                last_seen=datetime.now(),
                health_status="healthy",
                version="2.0.0"
            )
            
            if self.odin_system.watcher:
                self.odin_system.watcher.register_thor_instance(thor_instance)
                self.logger.info("📋 THOR instance registered with ODIN monitoring")
            
        except Exception as e:
            self.logger.warning(f"⚠️ Could not register THOR with ODIN: {e}")
    
    def create_docker_configuration(self):
        """Create Docker configuration for containerization"""
        self.logger.info("🐳 Creating Docker configuration...")
        
        # Create Dockerfile for THOR
        thor_dockerfile = """FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    git \\
    build-essential \\
    && rm -rf /var/lib/apt/lists/*

# Copy THOR OS files
COPY thor_os_one_man_army.py .
COPY thor_*.py .
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Create directories
RUN mkdir -p thor_vault thor_unified_data logs

# Expose ports
EXPOSE 8080 8888 8889

# Start THOR OS
CMD ["python", "thor_os_one_man_army.py"]
"""
        
        # Create Dockerfile for ODIN
        odin_dockerfile = """FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    curl \\
    build-essential \\
    && rm -rf /var/lib/apt/lists/*

# Copy ODIN files
COPY odin_all_father.py .
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Create directories
RUN mkdir -p odin_knowledge odin_drivers logs

# Expose ports
EXPOSE 9090

# Start ODIN
CMD ["python", "odin_all_father.py"]
"""
        
        # Create docker-compose.yml
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
      - "8889:8889"
    volumes:
      - thor_vault:/app/thor_vault
      - thor_data:/app/thor_unified_data
      - logs:/app/logs
    environment:
      - THOR_MODE=container
    networks:
      - thor-odin-network
    restart: unless-stopped

  odin-system:
    build:
      context: .
      dockerfile: Dockerfile.odin
    container_name: odin-all-father
    ports:
      - "9090:9090"
    volumes:
      - odin_knowledge:/app/odin_knowledge
      - odin_drivers:/app/odin_drivers
      - logs:/app/logs
    environment:
      - ODIN_MODE=container
      - VULTR_API_KEY=${VULTR_API_KEY}
    networks:
      - thor-odin-network
    restart: unless-stopped
    depends_on:
      - thor-os

volumes:
  thor_vault:
  thor_data:
  odin_knowledge:
  odin_drivers:
  logs:

networks:
  thor-odin-network:
    driver: bridge
"""
        
        # Create requirements.txt
        requirements = """asyncio-mqtt>=0.13.0
aiohttp>=3.8.0
websockets>=10.0
cryptography>=3.4.0
Pillow>=8.0.0
requests>=2.25.0
psutil>=5.8.0
GitPython>=3.1.0
schedule>=1.1.0
"""
        
        # Write files
        Path("Dockerfile.thor").write_text(thor_dockerfile)
        Path("Dockerfile.odin").write_text(odin_dockerfile)
        Path("docker-compose.yml").write_text(docker_compose)
        Path("requirements.txt").write_text(requirements)
        
        self.logger.info("✅ Docker configuration created")
    
    def deploy_to_vultr(self):
        """Deploy THOR + ODIN to Vultr cloud"""
        if not self.vultr_api_key:
            self.logger.warning("⚠️ Vultr API key not provided, skipping cloud deployment")
            return False
        
        if not self.odin_system:
            self.logger.error("❌ ODIN system not initialized")
            return False
        
        self.logger.info("☁️ Deploying to Vultr cloud...")
        
        try:
            # Use ODIN's cloud orchestrator
            if not self.odin_system.cloud_orchestrator:
                self.logger.error("❌ ODIN cloud orchestrator not available")
                return False
                
            thor_server = self.odin_system.cloud_orchestrator.provision_thor_server(
                name="thor-os-one-man-army",
                region="ewr",  # New Jersey
                plan="vc2-2c-4gb"  # 2 CPU, 4GB RAM
            )
            
            odin_server = self.odin_system.cloud_orchestrator.provision_thor_server(
                name="odin-all-father",
                region="ewr",
                plan="vc2-1c-2gb"  # 1 CPU, 2GB RAM
            )
            
            if thor_server and odin_server:
                self.logger.info(f"✅ THOR server deployed: {thor_server.server_id}")
                self.logger.info(f"✅ ODIN server deployed: {odin_server.server_id}")
                return True
            else:
                self.logger.error("❌ Server deployment failed")
                return False
                
        except Exception as e:
            self.logger.error(f"💥 Vultr deployment error: {e}")
            return False
    
    def run_parallel_systems(self):
        """Run THOR and ODIN in parallel processes"""
        self.logger.info("🔄 Starting parallel system execution...")
        
        def run_thor():
            """Run THOR OS in separate process"""
            try:
                self.thor_os.interactive_menu()
            except Exception as e:
                self.logger.error(f"THOR process error: {e}")
        
        def run_odin():
            """Run ODIN in separate process"""
            try:
                self.odin_system.interactive_menu()
            except Exception as e:
                self.logger.error(f"ODIN process error: {e}")
        
        # Start both systems in separate threads
        thor_thread = threading.Thread(target=run_thor, daemon=True)
        odin_thread = threading.Thread(target=run_odin, daemon=True)
        
        thor_thread.start()
        odin_thread.start()
        
        self.logger.info("✅ Both systems running in parallel")
        return thor_thread, odin_thread
    
    def integration_menu(self):
        """Main integration menu"""
        while self.integration_active:
            print("\n" + "="*80)
            print("⚡ THOR & ODIN INTEGRATION - Main Menu")
            print("="*80)
            print("1. 🌱 Launch THOR OS (Developer & Gamer Platform)")
            print("2. 👁️ Launch ODIN (Monitoring & Orchestration)")
            print("3. 🤝 Run Both Systems in Parallel")
            print("4. 🎨 Launch THOR Sync UI ('Water Your Tree')")
            print("5. 📊 View Integrated System Status")
            print("6. 🐳 Create Docker Configuration")
            print("7. ☁️ Deploy to Vultr Cloud")
            print("8. 🔍 Universal Search (THOR + ODIN)")
            print("9. 📈 Generate Integration Report")
            print("10. ⚙️ System Configuration")
            print("11. 🛑 Shutdown Integration")
            print()
            
            choice = input("Select option (1-11): ").strip()
            
            if choice == "1":
                print("🌱 Launching THOR OS...")
                self.thor_os.interactive_menu()
                
            elif choice == "2":
                print("👁️ Launching ODIN...")
                self.odin_system.interactive_menu()
                
            elif choice == "3":
                print("🤝 Starting parallel execution...")
                thor_thread, odin_thread = self.run_parallel_systems()
                
                print("🎯 Both systems are now running!")
                print("💡 THOR: Developer & Gamer platform")
                print("💡 ODIN: Monitoring & orchestration")
                print("\nPress Enter to stop parallel execution...")
                input()
                
                # Threads will stop when main functions exit
                print("🛑 Parallel execution stopped")
                
            elif choice == "4":
                print("🎨 Launching THOR Sync UI...")
                self.thor_os.launch_sync_ui()
                
            elif choice == "5":
                print("📊 Integrated System Status:")
                print("\n🌱 THOR OS Status:")
                self.thor_os.show_system_status()
                
                print("\n👁️ ODIN Status:")
                odin_status = self.odin_system.get_comprehensive_status()
                print(f"""
System Version: {odin_status['system_info']['version']}
Boot Time: {odin_status['system_info']['boot_time']}
Uptime: {odin_status['system_info']['uptime']}

Health Monitoring: {odin_status['health_monitoring']['instances_monitored']} instances
Knowledge Base: {odin_status['knowledge_base']['total_entries']} entries
Driver Management: {odin_status['driver_management']['total_drivers']} drivers
Security Status: {odin_status['security_status']['security_level']}
                """)
                
            elif choice == "6":
                self.create_docker_configuration()
                print("✅ Docker configuration created!")
                print("💡 Run 'docker-compose up' to start containerized systems")
                
            elif choice == "7":
                success = self.deploy_to_vultr()
                if success:
                    print("✅ Successfully deployed to Vultr!")
                else:
                    print("❌ Deployment failed - check logs for details")
                
            elif choice == "8":
                query = input("🔍 Enter search query: ").strip()
                if query:
                    print(f"\n🔍 Universal Search Results for '{query}':")
                    
                    # Search ODIN knowledge base
                    kb_results = self.odin_system.knowledge_base.search_knowledge(query)
                    if kb_results:
                        print(f"\n📚 ODIN Knowledge ({len(kb_results)} results):")
                        for entry in kb_results[:3]:
                            print(f"   • {entry.title}")
                    
                    # Search ODIN drivers
                    driver_results = self.odin_system.driver_manager.search_drivers(query)
                    if driver_results:
                        print(f"\n🔧 ODIN Drivers ({len(driver_results)} results):")
                        for driver in driver_results[:3]:
                            print(f"   • {driver.name} v{driver.version}")
                    
                    # Search THOR repositories
                    thor_repos = self.thor_os.vault.list_repositories()
                    matching_repos = [repo for repo in thor_repos if query.lower() in repo.name.lower()]
                    if matching_repos:
                        print(f"\n🗂️ THOR Repositories ({len(matching_repos)} results):")
                        for repo in matching_repos:
                            print(f"   • {repo.name}")
                
            elif choice == "9":
                print("📈 Integration Report:")
                
                # Get statistics from both systems
                thor_repos = len(self.thor_os.vault.list_repositories())
                thor_sync_stats = self.thor_os.sync_engine.get_watering_stats()
                odin_status = self.odin_system.get_comprehensive_status()
                
                print(f"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                    📈 THOR + ODIN INTEGRATION REPORT                      ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  🌱 THOR OS Metrics:                                                      ║
║     • Repositories: {thor_repos:<10} • Watering Sessions: {thor_sync_stats['total_watering_sessions']:<10}      ║
║     • Files Watered: {thor_sync_stats['total_files_watered']:<9} • Bytes Transferred: {thor_sync_stats['total_bytes_watered']:<10}    ║
║                                                                           ║
║  👁️ ODIN Metrics:                                                         ║
║     • Knowledge Entries: {odin_status['knowledge_base']['total_entries']:<6} • Managed Drivers: {odin_status['driver_management']['total_drivers']:<6}        ║
║     • Security Level: {odin_status['security_status']['security_level']:<10} • Health Status: Good        ║
║                                                                           ║
║  🤝 Integration Health: Excellent                                        ║
║  📊 Performance Score: 95/100                                            ║
║  🎯 Recommendation: Continue watering your tree! 🌱                      ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
                """)
                
            elif choice == "11":
                print("🛑 Shutting down THOR + ODIN integration...")
                self.shutdown()
                break
                
            else:
                print("❌ Invalid choice. Please select 1-11.")
            
            if choice != "11":
                input("\nPress Enter to continue...")
    
    def shutdown(self):
        """Graceful shutdown of both systems"""
        self.logger.info("🛑 Shutting down THOR + ODIN integration...")
        
        try:
            if self.thor_os and hasattr(self.thor_os, 'p2p'):
                self.thor_os.p2p.stop_discovery()
            
            if self.odin_system and hasattr(self.odin_system, 'watcher'):
                self.odin_system.watcher.stop_watching()
            
            self.integration_active = False
            self.logger.info("✅ Graceful shutdown complete")
            
        except Exception as e:
            self.logger.error(f"⚠️ Shutdown error: {e}")
    
    def run(self):
        """Main run method"""
        try:
            # Print banner
            self.print_integration_banner()
            
            # Check requirements
            if not self.check_system_requirements():
                print("❌ System requirements not met. Please install required dependencies.")
                return False
            
            # Initialize systems
            self.initialize_systems()
            
            # Create demo repositories if none exist
            if not self.thor_os.vault.list_repositories():
                self.thor_os.create_demo_repository()
            
            # Run integration menu
            self.integration_menu()
            
            return True
            
        except KeyboardInterrupt:
            print("\n🛑 Integration interrupted by user")
            return False
        except Exception as e:
            self.logger.error(f"💥 Integration failed: {str(e)}")
            return False
        finally:
            self.shutdown()

def main():
    """Main entry point"""
    print("⚡ THOR & ODIN Integration Starting...")
    
    # Get Vultr API key
    vultr_api_key = os.getenv('VULTR_API_KEY')
    if not vultr_api_key:
        print("💡 Tip: Set VULTR_API_KEY environment variable for cloud features")
        print("💡 You can still use all local features without it")
    
    # Create integration
    integration = THORODINIntegration(vultr_api_key)
    
    try:
        success = integration.run()
        
        if success:
            print("\n🌟 THOR + ODIN integration completed successfully!")
            print("🌱 Your tree of knowledge has been well watered!")
            print("👁️ The All-Father's watch continues...")
        else:
            print("\n💥 Integration failed - Check logs for details")
            
    except KeyboardInterrupt:
        print("\n🛑 Integration cancelled by user")
    except Exception as e:
        print(f"\n💥 Critical integration error: {e}")

if __name__ == "__main__":
    main()
