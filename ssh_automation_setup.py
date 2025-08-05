#!/usr/bin/env python3
"""
🔐 SSH KEY AUTOMATION SETUP
Generate SSH keys and configure automatic server access for AI agents
"""

import subprocess
import os
import json
from datetime import datetime

class SSHAutomationSetup:
    """Setup SSH automation for AI agents"""
    
    def __init__(self):
        self.ssh_dir = os.path.expanduser("~/.ssh")
        self.key_name = "trinity_ai_key"
        self.server_ip = "207.246.95.179"
        
        print("🔐 SSH AUTOMATION SETUP")
        print("🤖 Enabling AI agents for automatic server access")
        
    def generate_ssh_key(self):
        """Generate SSH key pair for automation"""
        print("🔑 Generating SSH key pair...")
        
        key_path = os.path.join(self.ssh_dir, self.key_name)
        
        try:
            # Create .ssh directory if it doesn't exist
            os.makedirs(self.ssh_dir, exist_ok=True)
            
            # Generate SSH key
            cmd = [
                "ssh-keygen",
                "-t", "rsa",
                "-b", "4096", 
                "-f", key_path,
                "-N", "",  # No passphrase for automation
                "-C", "trinity-ai@northbaystudios.io"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ SSH key generated successfully!")
                print(f"🔑 Private key: {key_path}")
                print(f"🔓 Public key: {key_path}.pub")
                
                # Read public key
                with open(f"{key_path}.pub", 'r') as f:
                    public_key = f.read().strip()
                    
                print("\n📋 PUBLIC KEY (copy this to server):")
                print("=" * 60)
                print(public_key)
                print("=" * 60)
                
                return True
            else:
                print(f"❌ Key generation failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ SSH key generation error: {e}")
            return False
            
    def create_ssh_config(self):
        """Create SSH config for easy server access"""
        print("⚙️ Creating SSH configuration...")
        
        config_path = os.path.join(self.ssh_dir, "config")
        key_path = os.path.join(self.ssh_dir, self.key_name)
        
        ssh_config = f"""
# TRINITY AI Server Configuration
Host northbay-server
    HostName {self.server_ip}
    User root
    IdentityFile {key_path}
    ServerAliveInterval 60
    ServerAliveCountMax 3
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null

# Aliases for AI agents
Host thor-deploy
    HostName {self.server_ip}
    User root
    IdentityFile {key_path}
    
Host loki-hunt
    HostName {self.server_ip}
    User root
    IdentityFile {key_path}
    
Host hela-learn
    HostName {self.server_ip}
    User root
    IdentityFile {key_path}
"""
        
        try:
            with open(config_path, 'w') as f:
                f.write(ssh_config)
                
            # Set proper permissions
            os.chmod(config_path, 0o600)
            
            print("✅ SSH config created!")
            print(f"📄 Config file: {config_path}")
            
            return True
            
        except Exception as e:
            print(f"❌ SSH config creation failed: {e}")
            return False
            
    def create_deployment_automation(self):
        """Create scripts for automated deployment"""
        print("🤖 Creating AI deployment automation...")
        
        # Auto-deploy script
        deploy_script = """#!/bin/bash
# 🤖 TRINITY AI AUTO-DEPLOYMENT
# Automatically deploy to server without manual intervention

echo "🚀 TRINITY AI Auto-Deployment Starting..."

# Copy deployment script to server
echo "📄 Uploading deployment script..."
scp deploy_server.sh northbay-server:/tmp/

# Execute deployment on server
echo "⚡ Executing deployment..."
ssh northbay-server "bash /tmp/deploy_server.sh"

# Verify deployment
echo "✅ Verifying deployment..."
ssh northbay-server "systemctl status northbaystudios"

echo "🎮 Auto-deployment complete!"
"""
        
        with open('auto_deploy.sh', 'w') as f:
            f.write(deploy_script)
            
        # Make executable
        os.chmod('auto_deploy.sh', 0o755)
        
        # AI agent wrapper
        ai_deploy_script = """#!/usr/bin/env python3
# 🤖 AI Agent Auto-Deployment Wrapper

import subprocess
import time

def thor_auto_deploy():
    print("🤖 THOR-AI initiating auto-deployment...")
    
    try:
        result = subprocess.run(['./auto_deploy.sh'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ THOR-AI deployment successful!")
            print(result.stdout)
        else:
            print("❌ THOR-AI deployment failed!")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ THOR-AI deployment error: {e}")

if __name__ == "__main__":
    thor_auto_deploy()
"""
        
        with open('thor_auto_deploy.py', 'w') as f:
            f.write(ai_deploy_script)
            
        print("✅ Automation scripts created!")
        print("📄 auto_deploy.sh - Shell deployment script")
        print("📄 thor_auto_deploy.py - AI agent wrapper")
        
    def generate_setup_instructions(self):
        """Generate setup instructions for server"""
        instructions = f"""
🔐 SSH AUTOMATION SETUP INSTRUCTIONS
=====================================

1. COPY PUBLIC KEY TO SERVER:
   ssh root@{self.server_ip}
   mkdir -p ~/.ssh
   echo "YOUR_PUBLIC_KEY_HERE" >> ~/.ssh/authorized_keys
   chmod 600 ~/.ssh/authorized_keys
   chmod 700 ~/.ssh

2. TEST SSH CONNECTION:
   ssh northbay-server
   
3. ENABLE AI AUTO-DEPLOYMENT:
   python3 thor_auto_deploy.py

4. FUTURE DEPLOYMENTS:
   AI agents can now automatically:
   - Deploy code changes
   - Update configurations  
   - Monitor server health
   - Scale services
   
🎯 BENEFITS:
✅ No manual SSH needed
✅ AI agents work autonomously  
✅ Instant deployments
✅ 24/7 automation capability

🚀 Once setup, just run:
   ./auto_deploy.sh
   
And THOR-AI handles everything!
"""
        
        with open('ssh_setup_instructions.txt', 'w') as f:
            f.write(instructions)
            
        print("📋 Setup instructions saved to: ssh_setup_instructions.txt")
        
        return instructions

def main():
    """Setup SSH automation for AI agents"""
    setup = SSHAutomationSetup()
    
    print("\n🔑 GENERATING SSH KEYS...")
    if setup.generate_ssh_key():
        
        print("\n⚙️ CREATING SSH CONFIG...")
        setup.create_ssh_config()
        
        print("\n🤖 CREATING AUTOMATION SCRIPTS...")
        setup.create_deployment_automation()
        
        print("\n📋 GENERATING INSTRUCTIONS...")
        instructions = setup.generate_setup_instructions()
        
        print("\n" + instructions)
        
        print("\n🎮 SSH AUTOMATION SETUP COMPLETE!")
        print("🤖 AI agents ready for autonomous deployment!")
        
    else:
        print("❌ SSH automation setup failed!")

if __name__ == "__main__":
    main()
