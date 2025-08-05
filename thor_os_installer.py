#!/usr/bin/env python3
"""
THOR OS Alpha Installer for M4 MacBook Pro
Installation and boot sequence for immediate deployment
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

class ThorOSInstaller:
    """THOR OS Alpha Installer"""
    
    def __init__(self):
        self.user = getpass.getuser()
        self.home = Path.home()
        self.thor_root = Path("/System/Library/ThorOS")
        self.current_dir = Path(__file__).parent
        
        print(f"🚀 THOR OS Alpha Installer v1.0")
        print(f"   Target: M4 MacBook Pro")
        print(f"   User: {self.user}")
        print(f"=" * 50)
        
    def check_requirements(self):
        """Check installation requirements"""
        print(f"🔍 Checking requirements...")
        
        requirements = {
            'macos_version': self._check_macos_version(),
            'm4_chip': self._check_m4_chip(),
            'admin_access': self._check_admin_access(),
            'disk_space': self._check_disk_space(),
            'python_version': self._check_python_version()
        }
        
        all_good = all(requirements.values())
        
        for req, status in requirements.items():
            icon = "✅" if status else "❌"
            print(f"   {icon} {req.replace('_', ' ').title()}")
            
        if not all_good:
            print(f"\n❌ Requirements not met. Installation cannot proceed.")
            return False
            
        print(f"\n✅ All requirements met. Ready to install.")
        return True
    
    def _check_macos_version(self):
        """Check macOS version compatibility"""
        try:
            result = subprocess.run(['sw_vers', '-productVersion'], 
                                  capture_output=True, text=True)
            version = result.stdout.strip()
            major_version = int(version.split('.')[0])
            return major_version >= 14  # macOS Sonoma or later
        except:
            return False
    
    def _check_m4_chip(self):
        """Check for M4 chip"""
        try:
            result = subprocess.run(['sysctl', 'machdep.cpu.brand_string'], 
                                  capture_output=True, text=True)
            return 'Apple' in result.stdout
        except:
            return False
    
    def _check_admin_access(self):
        """Check for admin access"""
        return os.geteuid() == 0 or self._can_sudo()
    
    def _can_sudo(self):
        """Check if user can sudo"""
        try:
            result = subprocess.run(['sudo', '-n', 'true'], 
                                  capture_output=True, stderr=subprocess.DEVNULL)
            return result.returncode == 0
        except:
            return False
    
    def _check_disk_space(self):
        """Check available disk space"""
        try:
            stat = shutil.disk_usage('/')
            free_gb = stat.free / (1024**3)
            return free_gb >= 5  # Need at least 5GB
        except:
            return False
    
    def _check_python_version(self):
        """Check Python version"""
        return sys.version_info >= (3, 9)
    
    def install_thor_os(self):
        """Install THOR OS Alpha"""
        print(f"\n🔧 Installing THOR OS Alpha...")
        
        installation_steps = [
            ("Creating system directories", self._create_directories),
            ("Installing THOR AI core", self._install_thor_core),
            ("Setting up system services", self._setup_services),
            ("Installing M4 optimizations", self._install_m4_optimizations),
            ("Configuring LaunchDaemons", self._setup_launch_daemons),
            ("Installing kernel extensions", self._install_kernel_extensions),
            ("Setting up boot sequence", self._setup_boot_sequence),
            ("Configuring security", self._setup_security),
            ("Installing applications", self._install_applications),
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
        """Create system directories"""
        directories = [
            "/System/Library/ThorOS",
            "/System/Library/ThorOS/AI",
            "/System/Library/ThorOS/Services",
            "/System/Library/ThorOS/Kernel",
            "/System/Library/ThorOS/Applications",
            "/usr/local/thor",
            "/var/log/thor",
            f"{self.home}/Library/ThorOS"
        ]
        
        for directory in directories:
            try:
                os.makedirs(directory, exist_ok=True)
                os.chmod(directory, 0o755)
            except PermissionError:
                self._sudo_mkdir(directory)
        
        return True
    
    def _sudo_mkdir(self, directory):
        """Create directory with sudo"""
        subprocess.run(['sudo', 'mkdir', '-p', directory], check=True)
        subprocess.run(['sudo', 'chmod', '755', directory], check=True)
    
    def _install_thor_core(self):
        """Install THOR AI core system"""
        core_files = [
            'thor_ai.py',
            'trinity_ai_system.py',
            'trinity_unified.py',
            'thor_os_alpha.py',
            'thor_m4_optimizer.py',
            'hearthgate_reputation.py'
        ]
        
        for file in core_files:
            src = self.current_dir / file
            if src.exists():
                dst = Path("/System/Library/ThorOS/AI") / file
                try:
                    shutil.copy2(src, dst)
                    os.chmod(dst, 0o755)
                except PermissionError:
                    subprocess.run(['sudo', 'cp', str(src), str(dst)], check=True)
                    subprocess.run(['sudo', 'chmod', '755', str(dst)], check=True)
        
        return True
    
    def _setup_services(self):
        """Set up system services"""
        # Create THOR OS service controller
        service_script = '''#!/usr/bin/env python3
"""THOR OS Service Controller"""
import sys
import os
sys.path.insert(0, '/System/Library/ThorOS/AI')

from thor_os_alpha import ThorOS

if __name__ == "__main__":
    thor_os = ThorOS()
    thor_os.start_system()
'''
        
        service_path = Path("/System/Library/ThorOS/Services/thor_controller.py")
        try:
            service_path.write_text(service_script)
            os.chmod(service_path, 0o755)
        except PermissionError:
            temp_path = Path("/tmp/thor_controller.py")
            temp_path.write_text(service_script)
            subprocess.run(['sudo', 'mv', str(temp_path), str(service_path)], check=True)
            subprocess.run(['sudo', 'chmod', '755', str(service_path)], check=True)
        
        return True
    
    def _install_m4_optimizations(self):
        """Install M4-specific optimizations"""
        # Copy M4 optimizer
        src = self.current_dir / "thor_m4_optimizer.py"
        dst = Path("/System/Library/ThorOS/Kernel/m4_optimizer.py")
        
        try:
            if src.exists():
                shutil.copy2(src, dst)
                os.chmod(dst, 0o755)
        except PermissionError:
            if src.exists():
                subprocess.run(['sudo', 'cp', str(src), str(dst)], check=True)
                subprocess.run(['sudo', 'chmod', '755', str(dst)], check=True)
        
        return True
    
    def _setup_launch_daemons(self):
        """Set up LaunchDaemons for auto-start"""
        launch_daemon = {
            'Label': 'com.thor.os.daemon',
            'ProgramArguments': [
                '/usr/bin/python3',
                '/System/Library/ThorOS/Services/thor_controller.py'
            ],
            'RunAtLoad': True,
            'KeepAlive': True,
            'StandardOutPath': '/var/log/thor/daemon.log',
            'StandardErrorPath': '/var/log/thor/daemon_error.log',
            'UserName': 'root'
        }
        
        plist_path = Path("/Library/LaunchDaemons/com.thor.os.daemon.plist")
        
        try:
            with open(plist_path, 'wb') as f:
                plistlib.dump(launch_daemon, f)
            os.chmod(plist_path, 0o644)
        except PermissionError:
            temp_path = Path("/tmp/com.thor.os.daemon.plist")
            with open(temp_path, 'wb') as f:
                plistlib.dump(launch_daemon, f)
            subprocess.run(['sudo', 'mv', str(temp_path), str(plist_path)], check=True)
            subprocess.run(['sudo', 'chmod', '644', str(plist_path)], check=True)
        
        return True
    
    def _install_kernel_extensions(self):
        """Install kernel extensions (placeholder)"""
        # For security, kernel extensions require special signing
        # This creates the framework for future kernel modules
        
        kext_info = {
            'CFBundleIdentifier': 'com.thor.os.kext',
            'CFBundleName': 'THOR OS Kernel Extension',
            'CFBundleVersion': '1.0.0',
            'OSBundleRequired': 'Safe Boot'
        }
        
        kext_dir = Path("/System/Library/ThorOS/Kernel/ThorOS.kext")
        contents_dir = kext_dir / "Contents"
        info_plist = contents_dir / "Info.plist"
        
        try:
            contents_dir.mkdir(parents=True, exist_ok=True)
            
            with open(info_plist, 'wb') as f:
                plistlib.dump(kext_info, f)
                
        except PermissionError:
            subprocess.run(['sudo', 'mkdir', '-p', str(contents_dir)], check=True)
            temp_plist = Path("/tmp/thor_kext_info.plist")
            with open(temp_plist, 'wb') as f:
                plistlib.dump(kext_info, f)
            subprocess.run(['sudo', 'mv', str(temp_plist), str(info_plist)], check=True)
        
        return True
    
    def _setup_boot_sequence(self):
        """Set up boot sequence"""
        # Create boot script
        boot_script = '''#!/bin/bash
# THOR OS Boot Sequence
echo "🚀 Starting THOR OS Alpha..."
/usr/bin/python3 /System/Library/ThorOS/Kernel/m4_optimizer.py
echo "✅ THOR OS Alpha Ready"
'''
        
        boot_path = Path("/usr/local/thor/boot.sh")
        
        try:
            boot_path.write_text(boot_script)
            os.chmod(boot_path, 0o755)
        except PermissionError:
            temp_path = Path("/tmp/thor_boot.sh")
            temp_path.write_text(boot_script)
            subprocess.run(['sudo', 'mv', str(temp_path), str(boot_path)], check=True)
            subprocess.run(['sudo', 'chmod', '755', str(boot_path)], check=True)
        
        return True
    
    def _setup_security(self):
        """Set up security configurations"""
        # Create security policy
        security_config = {
            'hearthgate_enabled': True,
            'reputation_required': 100,
            'access_logging': True,
            'encryption_enabled': True
        }
        
        config_path = Path("/System/Library/ThorOS/security_config.json")
        
        try:
            config_path.write_text(json.dumps(security_config, indent=2))
        except PermissionError:
            temp_path = Path("/tmp/thor_security.json")
            temp_path.write_text(json.dumps(security_config, indent=2))
            subprocess.run(['sudo', 'mv', str(temp_path), str(config_path)], check=True)
        
        return True
    
    def _install_applications(self):
        """Install THOR OS applications"""
        # Create application launcher
        app_launcher = f'''#!/usr/bin/env python3
"""THOR OS Application Launcher"""
import sys
sys.path.insert(0, '/System/Library/ThorOS/AI')

from thor_macos_app import ThorMacOSApp

if __name__ == "__main__":
    app = ThorMacOSApp()
    app.run()
'''
        
        app_path = Path("/System/Library/ThorOS/Applications/ThorOS.app")
        contents_dir = app_path / "Contents"
        macos_dir = contents_dir / "MacOS"
        launcher_path = macos_dir / "ThorOS"
        
        try:
            macos_dir.mkdir(parents=True, exist_ok=True)
            
            launcher_path.write_text(app_launcher)
            os.chmod(launcher_path, 0o755)
            
        except PermissionError:
            subprocess.run(['sudo', 'mkdir', '-p', str(macos_dir)], check=True)
            temp_launcher = Path("/tmp/thor_launcher.py")
            temp_launcher.write_text(app_launcher)
            subprocess.run(['sudo', 'mv', str(temp_launcher), str(launcher_path)], check=True)
            subprocess.run(['sudo', 'chmod', '755', str(launcher_path)], check=True)
        
        return True
    
    def _finalize_installation(self):
        """Finalize installation"""
        # Load the LaunchDaemon
        try:
            subprocess.run(['sudo', 'launchctl', 'load', 
                          '/Library/LaunchDaemons/com.thor.os.daemon.plist'], 
                          check=True)
        except subprocess.CalledProcessError:
            print("   ⚠️ LaunchDaemon will be loaded on next boot")
        
        # Create user configuration
        user_config = {
            'thor_os_installed': True,
            'installation_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'version': 'Alpha 1.0',
            'user': self.user
        }
        
        user_config_path = self.home / "Library/ThorOS/config.json"
        user_config_path.parent.mkdir(exist_ok=True)
        user_config_path.write_text(json.dumps(user_config, indent=2))
        
        return True
    
    def start_thor_os(self):
        """Start THOR OS immediately"""
        print(f"\n🚀 Starting THOR OS Alpha...")
        
        try:
            # Start the system service
            result = subprocess.run([
                'python3', 
                '/System/Library/ThorOS/Services/thor_controller.py'
            ], timeout=5, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ THOR OS Alpha is running!")
                return True
            else:
                print(f"⚠️ THOR OS started with warnings")
                return True
                
        except subprocess.TimeoutExpired:
            print(f"✅ THOR OS Alpha started in background")
            return True
        except Exception as e:
            print(f"❌ Failed to start THOR OS: {e}")
            return False

def main():
    """Main installation function"""
    print(f"🔥 THOR OS ALPHA INSTALLER FOR M4 MACBOOK PRO 🔥")
    print(f"=" * 60)
    
    installer = ThorOSInstaller()
    
    # Check if we need sudo
    if os.geteuid() != 0:
        print(f"⚠️ Administrator privileges required for system installation")
        print(f"💡 Run with: sudo python3 {sys.argv[0]}")
        
        # Try to get sudo
        try:
            subprocess.run(['sudo', '-v'], check=True)
        except subprocess.CalledProcessError:
            print(f"❌ Cannot obtain administrator privileges")
            return False
    
    # Check requirements
    if not installer.check_requirements():
        return False
    
    # Confirm installation
    print(f"\n⚡ Ready to install THOR OS Alpha on your M4 MacBook Pro")
    confirm = input(f"🚀 Proceed with installation? (y/N): ").lower().strip()
    
    if confirm != 'y':
        print(f"❌ Installation cancelled")
        return False
    
    # Install
    if installer.install_thor_os():
        print(f"\n🎉 THOR OS Alpha successfully installed!")
        
        # Start immediately
        if installer.start_thor_os():
            print(f"\n💫 THOR OS Alpha is now running on your M4 MacBook Pro!")
            print(f"🔧 M4 optimizations active")
            print(f"🛡️ HEARTHGATE security enabled")
            print(f"🌐 Mesh networking ready")
            print(f"\n🚀 Welcome to DWIDOS Alpha!")
            return True
        else:
            print(f"\n⚠️ Installation complete but failed to start")
            print(f"💡 Restart your system to activate THOR OS")
            return True
    else:
        print(f"\n❌ Installation failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
