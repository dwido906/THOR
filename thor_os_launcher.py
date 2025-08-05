#!/usr/bin/env python3
"""
THOR-OS Ultimate Launcher & System Integrator
============================================

Complete integration launcher for the THOR-OS ecosystem.
Coordinates all components: Privacy, Gaming, AI, Monitoring, and Distributed Learning.

Components Launched:
- THOR-OS Core System (thor_os_complete.py)
- Tabby ML Distributed Learning (thor_os_tabby_ml.py)  
- System Performance Monitor (thor_os_monitor.py)
- Gaming Community Integration
- Privacy-First Data Management
- Automated Deployment & Updates

Legal Compliance:
- GDPR/CCPA privacy controls enabled by default
- User consent required for all data processing
- Privacy-first architecture throughout
- Audit trail for all data operations
"""

import os
import sys
import json
import time
import signal
import threading
import subprocess
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

# Component Paths
THOR_OS_DIR = Path(__file__).parent
THOR_OS_CORE = THOR_OS_DIR / "thor_os_complete.py"
THOR_OS_TABBY = THOR_OS_DIR / "thor_os_tabby_ml.py"
THOR_OS_MONITOR = THOR_OS_DIR / "thor_os_monitor.py"

# Configuration
LAUNCHER_VERSION = "1.0.0"
CONFIG_PATH = Path.home() / ".thor-os" / "launcher_config.json"
LOG_PATH = Path.home() / ".thor-os" / "logs"

# Default Configuration
DEFAULT_CONFIG = {
    "version": LAUNCHER_VERSION,
    "components": {
        "core_system": {
            "enabled": True,
            "auto_start": True,
            "privacy_mode": "strict",
            "gaming_features": True
        },
        "tabby_ml": {
            "enabled": True,
            "auto_start": False,
            "distributed_learning": True,
            "privacy_consent": False
        },
        "system_monitor": {
            "enabled": True,
            "auto_start": True,
            "gaming_metrics": True,
            "ai_metrics": True
        },
        "auto_updates": {
            "enabled": True,
            "check_interval_hours": 24,
            "backup_before_update": True
        }
    },
    "privacy": {
        "data_collection_consent": False,
        "analytics_consent": False,
        "ml_training_consent": False,
        "auto_anonymization": True,
        "local_only_mode": False
    },
    "gaming": {
        "performance_priority": True,
        "fps_monitoring": True,
        "latency_optimization": True,
        "gamer_ui": True
    },
    "advanced": {
        "debug_mode": False,
        "verbose_logging": False,
        "experimental_features": False
    }
}

# Setup logging
LOG_PATH.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_PATH / 'thor_os_launcher.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class ComponentManager:
    """
    Manages THOR-OS component lifecycle
    Handles starting, stopping, and monitoring components
    """
    
    def __init__(self):
        self.running_components = {}
        self.component_status = {}
        self.shutdown_requested = False
        
        logger.info("🔧 Component Manager initialized")
    
    def start_component(self, component_name: str, script_path: Path, 
                       args: Optional[List[str]] = None) -> bool:
        """Start a THOR-OS component"""
        if component_name in self.running_components:
            logger.warning(f"⚠️ Component {component_name} already running")
            return True
        
        try:
            # Prepare command
            cmd = [sys.executable, str(script_path)]
            if args:
                cmd.extend(args)
            
            # Start process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.running_components[component_name] = process
            self.component_status[component_name] = {
                'status': 'running',
                'pid': process.pid,
                'started_at': datetime.now(),
                'restarts': 0
            }
            
            logger.info(f"✅ Started {component_name} (PID: {process.pid})")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start {component_name}: {e}")
            return False
    
    def stop_component(self, component_name: str) -> bool:
        """Stop a THOR-OS component"""
        if component_name not in self.running_components:
            logger.warning(f"⚠️ Component {component_name} not running")
            return True
        
        try:
            process = self.running_components[component_name]
            
            # Graceful shutdown first
            process.terminate()
            
            # Wait for graceful shutdown
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                # Force kill if needed
                process.kill()
                process.wait()
            
            # Cleanup
            del self.running_components[component_name]
            self.component_status[component_name]['status'] = 'stopped'
            self.component_status[component_name]['stopped_at'] = datetime.now()
            
            logger.info(f"🛑 Stopped {component_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to stop {component_name}: {e}")
            return False
    
    def restart_component(self, component_name: str) -> bool:
        """Restart a THOR-OS component"""
        logger.info(f"🔄 Restarting {component_name}...")
        
        # Get original start parameters (simplified)
        component_config = {
            'core_system': (THOR_OS_CORE, []),
            'tabby_ml': (THOR_OS_TABBY, []),
            'system_monitor': (THOR_OS_MONITOR, [])
        }
        
        if component_name not in component_config:
            logger.error(f"❌ Unknown component: {component_name}")
            return False
        
        script_path, args = component_config[component_name]
        
        # Stop and start
        self.stop_component(component_name)
        time.sleep(2)  # Brief pause
        
        success = self.start_component(component_name, script_path, args)
        
        if success:
            self.component_status[component_name]['restarts'] += 1
        
        return success
    
    def monitor_components(self):
        """Monitor component health and restart if needed"""
        while not self.shutdown_requested:
            try:
                for component_name, process in list(self.running_components.items()):
                    # Check if process is still running
                    if process.poll() is not None:
                        logger.warning(f"⚠️ Component {component_name} stopped unexpectedly")
                        
                        # Clean up
                        del self.running_components[component_name]
                        self.component_status[component_name]['status'] = 'crashed'
                        
                        # Auto-restart if configured
                        if self.component_status[component_name]['restarts'] < 3:
                            logger.info(f"🔄 Auto-restarting {component_name}...")
                            self.restart_component(component_name)
                        else:
                            logger.error(f"💀 Component {component_name} failed too many times")
                
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"❌ Component monitoring error: {e}")
                time.sleep(60)
    
    def get_status_summary(self) -> Dict[str, Any]:
        """Get status summary of all components"""
        return {
            'running_components': len(self.running_components),
            'component_details': self.component_status,
            'timestamp': datetime.now().isoformat()
        }
    
    def shutdown_all(self):
        """Shutdown all components gracefully"""
        self.shutdown_requested = True
        
        logger.info("🛑 Shutting down all components...")
        
        for component_name in list(self.running_components.keys()):
            self.stop_component(component_name)
        
        logger.info("✅ All components stopped")

class PrivacyManager:
    """
    Privacy management and consent handling
    Ensures GDPR/CCPA compliance across all components
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.consent_given = {}
        
        logger.info("🔒 Privacy Manager initialized")
    
    def check_privacy_compliance(self) -> bool:
        """Check if privacy settings are compliant"""
        privacy_config = self.config.get('privacy', {})
        
        # Ensure auto-anonymization is enabled
        if not privacy_config.get('auto_anonymization', True):
            logger.warning("⚠️ Auto-anonymization disabled - privacy risk")
            return False
        
        # Check consent for data processing
        if privacy_config.get('data_collection_consent', False):
            if not self._verify_consent('data_collection'):
                return False
        
        return True
    
    def _verify_consent(self, consent_type: str) -> bool:
        """Verify user consent for specific data processing"""
        consent_file = CONFIG_PATH.parent / f"{consent_type}_consent.json"
        
        if consent_file.exists():
            try:
                with open(consent_file, 'r') as f:
                    consent_data = json.load(f)
                
                # Check if consent is still valid (not older than 1 year)
                consent_date = datetime.fromisoformat(consent_data.get('timestamp', '2000-01-01'))
                if (datetime.now() - consent_date).days > 365:
                    return False
                
                return consent_data.get('consent_given', False)
                
            except Exception:
                return False
        
        return False
    
    def request_consent(self, consent_type: str, description: str) -> bool:
        """Request user consent for data processing"""
        print(f"\n🔒 PRIVACY CONSENT REQUEST")
        print("="*40)
        print(f"Type: {consent_type}")
        print(f"Description: {description}")
        print("\nYour privacy rights:")
        print("• You can withdraw consent at any time")
        print("• Data is automatically anonymized")
        print("• Local-only processing when possible")
        print("• Full data deletion available on request")
        
        response = input(f"\nGrant consent for {consent_type}? (y/N): ").lower()
        consent_given = response in ['y', 'yes']
        
        # Save consent
        consent_file = CONFIG_PATH.parent / f"{consent_type}_consent.json"
        consent_data = {
            'consent_given': consent_given,
            'timestamp': datetime.now().isoformat(),
            'description': description,
            'version': LAUNCHER_VERSION
        }
        
        with open(consent_file, 'w') as f:
            json.dump(consent_data, f, indent=2)
        
        self.consent_given[consent_type] = consent_given
        return consent_given

class ThorOSLauncher:
    """
    Main THOR-OS launcher and coordinator
    Manages the entire THOR-OS ecosystem
    """
    
    def __init__(self):
        self.config = self._load_config()
        self.component_manager = ComponentManager()
        self.privacy_manager = PrivacyManager(self.config)
        self.running = False
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        logger.info("🚀 THOR-OS Launcher initialized")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load launcher configuration"""
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        if CONFIG_PATH.exists():
            try:
                with open(CONFIG_PATH, 'r') as f:
                    config = json.load(f)
                
                # Merge with defaults for any missing keys
                return {**DEFAULT_CONFIG, **config}
                
            except Exception as e:
                logger.warning(f"⚠️ Failed to load config: {e}, using defaults")
        
        # Save default config
        self._save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    
    def _save_config(self, config: Dict[str, Any]):
        """Save launcher configuration"""
        try:
            with open(CONFIG_PATH, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            logger.error(f"❌ Failed to save config: {e}")
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"📡 Received signal {signum}, shutting down...")
        self.shutdown()
    
    def start_system(self):
        """Start the complete THOR-OS system"""
        logger.info("🚀 Starting THOR-OS Ultimate System...")
        
        # Privacy compliance check
        if not self.privacy_manager.check_privacy_compliance():
            logger.error("❌ Privacy compliance check failed")
            return False
        
        self.running = True
        
        # Start component monitoring thread
        monitor_thread = threading.Thread(
            target=self.component_manager.monitor_components, 
            daemon=True
        )
        monitor_thread.start()
        
        # Start enabled components
        components_config = self.config.get('components', {})
        
        # Core System
        if components_config.get('core_system', {}).get('enabled', True):
            if components_config['core_system'].get('auto_start', True):
                self.component_manager.start_component('core_system', THOR_OS_CORE)
        
        # Tabby ML (with consent check)
        tabby_config = components_config.get('tabby_ml', {})
        if tabby_config.get('enabled', True):
            if tabby_config.get('distributed_learning', True):
                # Request ML consent if needed
                if not tabby_config.get('privacy_consent', False):
                    consent = self.privacy_manager.request_consent(
                        'ml_training',
                        'Machine learning training on anonymized code snippets'
                    )
                    
                    if consent:
                        tabby_config['privacy_consent'] = True
                        self.config['components']['tabby_ml'] = tabby_config
                        self._save_config(self.config)
            
            if tabby_config.get('auto_start', False) and tabby_config.get('privacy_consent', False):
                self.component_manager.start_component('tabby_ml', THOR_OS_TABBY)
        
        # System Monitor
        if components_config.get('system_monitor', {}).get('enabled', True):
            if components_config['system_monitor'].get('auto_start', True):
                self.component_manager.start_component('system_monitor', THOR_OS_MONITOR)
        
        logger.info("✅ THOR-OS system startup complete")
        return True
    
    def display_status(self):
        """Display system status"""
        status = self.component_manager.get_status_summary()
        
        print("\n🔥 THOR-OS SYSTEM STATUS 🔥")
        print("="*50)
        print(f"Components Running: {status['running_components']}")
        print(f"Last Update: {datetime.now().strftime('%H:%M:%S')}")
        print()
        
        for component, details in status['component_details'].items():
            status_emoji = {
                'running': '✅',
                'stopped': '⏹️',
                'crashed': '💀'
            }
            
            emoji = status_emoji.get(details['status'], '❓')
            print(f"{emoji} {component}: {details['status']}")
            
            if details['status'] == 'running':
                print(f"   PID: {details['pid']}")
                uptime = datetime.now() - details['started_at']
                print(f"   Uptime: {uptime}")
            
            if details.get('restarts', 0) > 0:
                print(f"   Restarts: {details['restarts']}")
        
        print()
    
    def interactive_mode(self):
        """Run in interactive mode"""
        print("\n🎮 THOR-OS Interactive Control")
        print("="*30)
        print("Commands:")
        print("  status  - Show system status")
        print("  start   - Start component")
        print("  stop    - Stop component")
        print("  restart - Restart component")
        print("  config  - Show configuration")
        print("  privacy - Privacy settings")
        print("  quit    - Exit")
        
        while self.running:
            try:
                command = input("\nTHOR-OS> ").strip().lower()
                
                if command == 'status':
                    self.display_status()
                
                elif command == 'start':
                    component = input("Component name: ").strip()
                    if component in ['core_system', 'tabby_ml', 'system_monitor']:
                        script_map = {
                            'core_system': THOR_OS_CORE,
                            'tabby_ml': THOR_OS_TABBY,
                            'system_monitor': THOR_OS_MONITOR
                        }
                        self.component_manager.start_component(component, script_map[component])
                    else:
                        print("❌ Unknown component")
                
                elif command == 'stop':
                    component = input("Component name: ").strip()
                    self.component_manager.stop_component(component)
                
                elif command == 'restart':
                    component = input("Component name: ").strip()
                    self.component_manager.restart_component(component)
                
                elif command == 'config':
                    print(json.dumps(self.config, indent=2))
                
                elif command == 'privacy':
                    self._privacy_menu()
                
                elif command in ['quit', 'exit', 'q']:
                    break
                
                else:
                    print("❓ Unknown command")
                    
            except (EOFError, KeyboardInterrupt):
                break
    
    def _privacy_menu(self):
        """Privacy settings menu"""
        print("\n🔒 Privacy Settings")
        print("1. View current settings")
        print("2. Revoke ML training consent")
        print("3. Enable local-only mode")
        print("4. Request data deletion")
        
        choice = input("Select option (1-4): ").strip()
        
        if choice == '1':
            privacy_config = self.config.get('privacy', {})
            print(json.dumps(privacy_config, indent=2))
        
        elif choice == '2':
            # Revoke ML consent
            consent_file = CONFIG_PATH.parent / "ml_training_consent.json"
            if consent_file.exists():
                consent_file.unlink()
                print("✅ ML training consent revoked")
                
                # Stop Tabby ML if running
                self.component_manager.stop_component('tabby_ml')
        
        elif choice == '3':
            self.config['privacy']['local_only_mode'] = True
            self._save_config(self.config)
            print("✅ Local-only mode enabled")
        
        elif choice == '4':
            print("🗑️ Data deletion will remove all THOR-OS data")
            confirm = input("Are you sure? (yes/no): ").lower()
            if confirm == 'yes':
                self._delete_all_data()
                print("✅ All data deleted")
    
    def _delete_all_data(self):
        """Delete all THOR-OS data"""
        thor_os_data = Path.home() / ".thor-os"
        if thor_os_data.exists():
            import shutil
            shutil.rmtree(thor_os_data)
    
    def shutdown(self):
        """Shutdown the THOR-OS system"""
        logger.info("🛑 Shutting down THOR-OS...")
        self.running = False
        self.component_manager.shutdown_all()
        logger.info("✅ THOR-OS shutdown complete")

def main():
    """Main entry point for THOR-OS Launcher"""
    parser = argparse.ArgumentParser(description="THOR-OS Ultimate Launcher")
    parser.add_argument('--mode', choices=['auto', 'interactive', 'status'], 
                       default='interactive', help='Launch mode')
    parser.add_argument('--config', help='Configuration file path')
    parser.add_argument('--privacy-strict', action='store_true', 
                       help='Enable strict privacy mode')
    
    args = parser.parse_args()
    
    # ASCII Art Banner
    print("""
    ████████╗██╗  ██╗ ██████╗ ██████╗        ██████╗ ███████╗
    ╚══██╔══╝██║  ██║██╔═══██╗██╔══██╗      ██╔═══██╗██╔════╝
       ██║   ███████║██║   ██║██████╔╝█████╗██║   ██║███████╗
       ██║   ██╔══██║██║   ██║██╔══██╗╚════╝██║   ██║╚════██║
       ██║   ██║  ██║╚██████╔╝██║  ██║      ╚██████╔╝███████║
       ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝       ╚═════╝ ╚══════╝
    
    🔥 Ultimate Gaming & AI Operating System 🔥
    🔒 Privacy-First • 🎮 Gaming-Optimized • 🤖 AI-Powered
    """)
    
    launcher = ThorOSLauncher()
    
    try:
        if args.mode == 'auto':
            # Auto mode - start system and run in background
            if launcher.start_system():
                print("✅ THOR-OS started in auto mode")
                print("Use '--mode interactive' for control interface")
                
                # Keep running until shutdown signal
                while launcher.running:
                    time.sleep(60)
        
        elif args.mode == 'status':
            # Status mode - show status and exit
            launcher.display_status()
        
        else:
            # Interactive mode (default)
            if launcher.start_system():
                launcher.interactive_mode()
    
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
    
    finally:
        launcher.shutdown()

if __name__ == "__main__":
    main()
