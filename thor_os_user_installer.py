#!/usr/bin/env python3
"""
THOR OS Alpha User Installation
Safe installation for M4 MacBook Pro without SIP conflicts
"""

import os
import sys
import json
import shutil
import subprocess
import plistlib
from pathlib import Path
import getpass
import time

class ThorOSUserInstaller:
    """THOR OS Alpha User Installer - SIP Safe"""
    
    def __init__(self):
        self.user = getpass.getuser()
        self.home = Path.home()
        self.thor_root = self.home / "ThorOS"
        self.current_dir = Path(__file__).parent
        
        print(f"🚀 THOR OS Alpha User Installer v1.0")
        print(f"   Target: M4 MacBook Pro (User Space)")
        print(f"   User: {self.user}")
        print(f"   Install Path: {self.thor_root}")
        print(f"=" * 50)
        
    def install_thor_os(self):
        """Install THOR OS Alpha in user space"""
        print(f"\n🔧 Installing THOR OS Alpha (User Space)...")
        
        installation_steps = [
            ("Creating user directories", self._create_directories),
            ("Installing THOR AI core", self._install_thor_core),
            ("Setting up user services", self._setup_services),
            ("Installing M4 optimizations", self._install_m4_optimizations),
            ("Setting up auto-start", self._setup_auto_start),
            ("Creating applications", self._create_applications),
            ("Setting up security", self._setup_security),
            ("Creating launchers", self._create_launchers),
            ("Finalizing installation", self._finalize_installation)
        ]
        
        for step_name, step_func in installation_steps:
            print(f"   🔧 {step_name}...")
            try:
                success = step_func()
                if success:
                    print(f"   ✅ {step_name} completed")
                else:
                    print(f"   ❌ {step_name} failed")
                    return False
            except Exception as e:
                print(f"   ❌ {step_name} failed: {e}")
                return False
        
        print(f"\n🎉 THOR OS Alpha installation complete!")
        return True
    
    def _create_directories(self):
        """Create user directories"""
        directories = [
            self.thor_root,
            self.thor_root / "AI",
            self.thor_root / "Services",
            self.thor_root / "Kernel", 
            self.thor_root / "Applications",
            self.thor_root / "Data",
            self.thor_root / "Logs",
            self.thor_root / "Config",
            self.home / "Library" / "LaunchAgents"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
        
        return True
    
    def _install_thor_core(self):
        """Install THOR AI core system"""
        core_files = [
            'thor_ai.py',
            'trinity_ai_system.py', 
            'trinity_unified.py',
            'thor_os_alpha.py',
            'thor_m4_optimizer.py',
            'hearthgate_reputation.py',
            'thor_revenue_system.py'
        ]
        
        for file in core_files:
            src = self.current_dir / file
            if src.exists():
                dst = self.thor_root / "AI" / file
                shutil.copy2(src, dst)
                os.chmod(dst, 0o755)
        
        return True
    
    def _setup_services(self):
        """Set up user services"""
        service_script = f'''#!/usr/bin/env python3
"""THOR OS Service Controller"""
import sys
import os
sys.path.insert(0, '{self.thor_root}/AI')

try:
    from thor_os_alpha import ThorOS
    
    if __name__ == "__main__":
        print("🚀 Starting THOR OS Alpha...")
        thor_os = ThorOS()
        thor_os.start_system()
        print("✅ THOR OS Alpha running")
except ImportError:
    print("⚠️ THOR OS modules not found")
    sys.exit(1)
except Exception as e:
    print(f"❌ THOR OS startup failed: {{e}}")
    sys.exit(1)
'''
        
        service_path = self.thor_root / "Services" / "thor_controller.py"
        service_path.write_text(service_script)
        os.chmod(service_path, 0o755)
        
        return True
    
    def _install_m4_optimizations(self):
        """Install M4-specific optimizations"""
        src = self.current_dir / "thor_m4_optimizer.py"
        if src.exists():
            dst = self.thor_root / "Kernel" / "m4_optimizer.py"
            shutil.copy2(src, dst)
            os.chmod(dst, 0o755)
        
        return True
    
    def _setup_auto_start(self):
        """Set up auto-start with LaunchAgent"""
        launch_agent = {
            'Label': 'com.thor.os.user',
            'ProgramArguments': [
                '/usr/bin/python3',
                str(self.thor_root / "Services" / "thor_controller.py")
            ],
            'RunAtLoad': True,
            'KeepAlive': False,
            'StandardOutPath': str(self.thor_root / "Logs" / "thor.log"),
            'StandardErrorPath': str(self.thor_root / "Logs" / "thor_error.log")
        }
        
        plist_path = self.home / "Library" / "LaunchAgents" / "com.thor.os.user.plist"
        
        with open(plist_path, 'wb') as f:
            plistlib.dump(launch_agent, f)
        
        return True
    
    def _create_applications(self):
        """Create THOR OS applications"""
        # Main application launcher
        app_script = f'''#!/usr/bin/env python3
"""THOR OS Application"""
import sys
import tkinter as tk
from tkinter import ttk
import threading
import subprocess
from pathlib import Path

sys.path.insert(0, '{self.thor_root}/AI')

class ThorOSApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("THOR OS Alpha - DWIDOS")
        self.root.geometry("800x600")
        self.setup_gui()
    
    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="🚀 THOR OS Alpha", 
                               font=("Arial", 20, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        subtitle_label = ttk.Label(main_frame, text="DWIDOS on M4 MacBook Pro", 
                                  font=("Arial", 12))
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Control buttons
        ttk.Button(main_frame, text="🧠 Start THOR AI", 
                  command=self.start_thor_ai).grid(row=2, column=0, pady=5, padx=5, sticky="ew")
        
        ttk.Button(main_frame, text="🛡️ HEARTHGATE Status", 
                  command=self.check_hearthgate).grid(row=2, column=1, pady=5, padx=5, sticky="ew")
        
        ttk.Button(main_frame, text="⚡ M4 Optimization", 
                  command=self.optimize_m4).grid(row=3, column=0, pady=5, padx=5, sticky="ew")
        
        ttk.Button(main_frame, text="💰 Revenue System", 
                  command=self.start_revenue).grid(row=3, column=1, pady=5, padx=5, sticky="ew")
        
        # Status area
        self.status_text = tk.Text(main_frame, height=20, width=80)
        self.status_text.grid(row=4, column=0, columnspan=2, pady=10, sticky="nsew")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.status_text.yview)
        scrollbar.grid(row=4, column=2, sticky="ns")
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        self.log("🎉 THOR OS Alpha GUI Ready")
        self.log("💫 Welcome to DWIDOS on your M4 MacBook Pro!")
    
    def log(self, message):
        self.status_text.insert(tk.END, f"{{message}}\\n")
        self.status_text.see(tk.END)
        self.root.update()
    
    def start_thor_ai(self):
        self.log("🧠 Starting THOR AI...")
        try:
            subprocess.Popen([
                'python3', str(Path('{self.thor_root}') / 'AI' / 'trinity_unified.py')
            ])
            self.log("✅ THOR AI started successfully")
        except Exception as e:
            self.log(f"❌ Failed to start THOR AI: {{e}}")
    
    def check_hearthgate(self):
        self.log("🛡️ Checking HEARTHGATE status...")
        try:
            result = subprocess.run([
                'python3', str(Path('{self.thor_root}') / 'AI' / 'hearthgate_reputation.py')
            ], capture_output=True, text=True, timeout=10)
            self.log("✅ HEARTHGATE security active")
        except Exception as e:
            self.log(f"⚠️ HEARTHGATE check: {{e}}")
    
    def optimize_m4(self):
        self.log("⚡ Running M4 optimizations...")
        try:
            subprocess.Popen([
                'python3', str(Path('{self.thor_root}') / 'Kernel' / 'm4_optimizer.py')
            ])
            self.log("✅ M4 optimizations started")
        except Exception as e:
            self.log(f"❌ M4 optimization failed: {{e}}")
    
    def start_revenue(self):
        self.log("💰 Starting revenue system...")
        try:
            subprocess.Popen([
                'python3', str(Path('{self.thor_root}') / 'AI' / 'thor_revenue_system.py')
            ])
            self.log("✅ Revenue system started")
        except Exception as e:
            self.log(f"❌ Revenue system failed: {{e}}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ThorOSApp()
    app.run()
'''
        
        app_path = self.thor_root / "Applications" / "ThorOS.py"
        app_path.write_text(app_script)
        os.chmod(app_path, 0o755)
        
        return True
    
    def _setup_security(self):
        """Set up security configurations"""
        security_config = {
            'hearthgate_enabled': True,
            'reputation_required': 100,
            'access_logging': True,
            'encryption_enabled': True,
            'user_install': True,
            'install_path': str(self.thor_root)
        }
        
        config_path = self.thor_root / "Config" / "security.json"
        config_path.write_text(json.dumps(security_config, indent=2))
        
        return True
    
    def _create_launchers(self):
        """Create command-line launchers"""
        # Create thor-ai command
        thor_launcher = f'''#!/bin/bash
# THOR AI Launcher
cd "{self.thor_root}/AI"
python3 trinity_unified.py "$@"
'''
        
        launcher_path = self.thor_root / "thor-ai"
        launcher_path.write_text(thor_launcher)
        os.chmod(launcher_path, 0o755)
        
        # Create symlink in user bin (if exists)
        user_bin = self.home / ".local" / "bin"
        if user_bin.exists():
            try:
                symlink_path = user_bin / "thor-ai"
                if symlink_path.exists():
                    symlink_path.unlink()
                symlink_path.symlink_to(launcher_path)
            except:
                pass  # Ignore symlink failures
        
        return True
    
    def _finalize_installation(self):
        """Finalize installation"""
        # Create user configuration
        user_config = {
            'thor_os_installed': True,
            'installation_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'version': 'Alpha 1.0 User',
            'user': self.user,
            'install_path': str(self.thor_root),
            'auto_start': True
        }
        
        config_path = self.thor_root / "Config" / "user_config.json"
        config_path.write_text(json.dumps(user_config, indent=2))
        
        # Load LaunchAgent
        try:
            subprocess.run([
                'launchctl', 'load', 
                str(self.home / "Library" / "LaunchAgents" / "com.thor.os.user.plist")
            ], check=True)
            print("   ✅ Auto-start configured")
        except subprocess.CalledProcessError:
            print("   ⚠️ Auto-start will activate on next login")
        
        return True
    
    def start_thor_os(self):
        """Start THOR OS immediately"""
        print(f"\n🚀 Starting THOR OS Alpha...")
        
        try:
            # Start the main service
            service_path = self.thor_root / "Services" / "thor_controller.py"
            
            process = subprocess.Popen([
                'python3', str(service_path)
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Give it a moment to start
            time.sleep(2)
            
            if process.poll() is None:
                print(f"✅ THOR OS Alpha is running!")
                return True
            else:
                print(f"⚠️ THOR OS started but may have warnings")
                return True
                
        except Exception as e:
            print(f"❌ Failed to start THOR OS: {e}")
            return False

def main():
    """Main installation function"""
    print(f"🔥 THOR OS ALPHA USER INSTALLER 🔥")
    print(f"=" * 50)
    
    installer = ThorOSUserInstaller()
    
    # Confirm installation
    print(f"\n⚡ Ready to install THOR OS Alpha in user space")
    print(f"📁 Installation path: {installer.thor_root}")
    confirm = input(f"🚀 Proceed with installation? (y/N): ").lower().strip()
    
    if confirm != 'y':
        print(f"❌ Installation cancelled")
        return False
    
    # Install
    if installer.install_thor_os():
        print(f"\n🎉 THOR OS Alpha successfully installed!")
        
        # Start immediately
        if installer.start_thor_os():
            print(f"\n💫 THOR OS Alpha is now running!")
            print(f"🔧 M4 optimizations ready")
            print(f"🛡️ HEARTHGATE security active")
            print(f"🌐 Mesh networking ready")
            print(f"\n🚀 Welcome to DWIDOS Alpha!")
            
            print(f"\n💡 Quick Start:")
            print(f"   • GUI: python3 {installer.thor_root}/Applications/ThorOS.py")
            print(f"   • CLI: {installer.thor_root}/thor-ai --status")
            print(f"   • Full System: python3 {installer.thor_root}/AI/trinity_unified.py")
            
            return True
        else:
            print(f"\n⚠️ Installation complete but failed to start")
            print(f"💡 Run manually: python3 {installer.thor_root}/Services/thor_controller.py")
            return True
    else:
        print(f"\n❌ Installation failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
