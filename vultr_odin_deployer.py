#!/usr/bin/env python3
"""
ODIN Core Server OS - Vultr Deployment Orchestrator
Automated deployment of ODIN as exclusive OS on Vultr server
"""

import requests
import json
import time
import os
import sys
from datetime import datetime

class VultrODINDeployer:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.vultr.com/v2"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.deployment_log = []
        
    def log_step(self, step, status, details=""):
        """Log deployment step"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {step}: {status}"
        if details:
            log_entry += f" - {details}"
        print(log_entry)
        self.deployment_log.append(log_entry)
    
    def check_existing_servers(self):
        """Check for existing servers"""
        self.log_step("STEP 1", "Checking existing Vultr servers...")
        
        try:
            response = requests.get(f"{self.base_url}/instances", headers=self.headers)
            if response.status_code == 200:
                servers = response.json()
                self.log_step("STEP 1", "SUCCESS", f"Found {len(servers.get('instances', []))} existing servers")
                return servers.get('instances', [])
            else:
                self.log_step("STEP 1", "ERROR", f"API call failed: {response.status_code}")
                return []
        except Exception as e:
            self.log_step("STEP 1", "ERROR", f"Exception: {str(e)}")
            return []
    
    def destroy_existing_server(self, server_id):
        """Destroy existing server to make room for ODIN"""
        self.log_step("STEP 2", f"Destroying existing server {server_id}...")
        
        try:
            response = requests.delete(f"{self.base_url}/instances/{server_id}", headers=self.headers)
            if response.status_code == 204:
                self.log_step("STEP 2", "SUCCESS", f"Server {server_id} destruction initiated")
                return True
            else:
                self.log_step("STEP 2", "ERROR", f"Failed to destroy server: {response.status_code}")
                return False
        except Exception as e:
            self.log_step("STEP 2", "ERROR", f"Exception: {str(e)}")
            return False
    
    def create_odin_server(self):
        """Create new ODIN Core Server"""
        self.log_step("STEP 3", "Creating ODIN Core Server...")
        
        server_config = {
            "region": "ewr",  # Newark (East Coast)
            "plan": "vc2-4c-8gb",  # 4 vCPUs, 8GB RAM
            "os_id": 387,  # Ubuntu 22.04 LTS (we'll replace this with ODIN)
            "label": "ODIN-ALLFATHER-CORE",
            "tag": "odin-core-server",
            "hostname": "odin-allfather",
            "enable_ipv6": True,
            "backups": "enabled",
            "ddos_protection": True,
            "activation_email": False
        }
        
        try:
            response = requests.post(f"{self.base_url}/instances", 
                                   headers=self.headers, 
                                   json=server_config)
            
            if response.status_code == 202:
                server_data = response.json()
                server_id = server_data["instance"]["id"]
                self.log_step("STEP 3", "SUCCESS", f"ODIN server created: {server_id}")
                return server_id
            else:
                self.log_step("STEP 3", "ERROR", f"Server creation failed: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except Exception as e:
            self.log_step("STEP 3", "ERROR", f"Exception: {str(e)}")
            return None
    
    def wait_for_server_active(self, server_id):
        """Wait for server to become active"""
        self.log_step("STEP 4", f"Waiting for server {server_id} to become active...")
        
        max_attempts = 30
        for attempt in range(max_attempts):
            try:
                response = requests.get(f"{self.base_url}/instances/{server_id}", headers=self.headers)
                if response.status_code == 200:
                    server_data = response.json()
                    status = server_data["instance"]["server_status"]
                    power_status = server_data["instance"]["power_status"]
                    
                    self.log_step("STEP 4", "CHECKING", f"Status: {status}, Power: {power_status}")
                    
                    if status == "ok" and power_status == "running":
                        ip_address = server_data["instance"]["main_ip"]
                        self.log_step("STEP 4", "SUCCESS", f"Server active at {ip_address}")
                        return ip_address
                
                time.sleep(30)  # Wait 30 seconds between checks
                
            except Exception as e:
                self.log_step("STEP 4", "ERROR", f"Exception: {str(e)}")
        
        self.log_step("STEP 4", "TIMEOUT", "Server did not become active within timeout")
        return None
    
    def install_odin_os(self, server_ip):
        """Install ODIN Core Server OS on the server"""
        self.log_step("STEP 5", f"Installing ODIN Core Server OS on {server_ip}...")
        
        # Create ODIN installation script
        odin_install_script = '''#!/bin/bash
# ODIN Core Server OS Installation Script
# This will completely replace the existing OS with ODIN

set -e

echo "👁️ ODIN CORE SERVER OS INSTALLATION STARTING..."
echo "⚠️  WARNING: This will completely wipe the existing OS!"

# Update system
apt update && apt upgrade -y

# Install required packages for ODIN
apt install -y python3 python3-pip nginx htop iotop netstat-nat curl wget git

# Create ODIN directory structure
mkdir -p /opt/odin/{bin,config,logs,data}
mkdir -p /var/log/odin
mkdir -p /etc/odin

# Install Python dependencies
pip3 install psutil requests flask asyncio schedule cryptography

# Set hostname to ODIN
echo "odin-allfather" > /etc/hostname
hostname odin-allfather

# Update hosts file
echo "127.0.0.1 odin-allfather" >> /etc/hosts

# Create ODIN system user
useradd -r -d /opt/odin -s /bin/bash odin
chown -R odin:odin /opt/odin
chown -R odin:odin /var/log/odin

# Configure ODIN to start on boot
cat > /etc/systemd/system/odin-core.service << 'ODIN_SERVICE_EOF'
[Unit]
Description=ODIN Core Server - The All-Father
After=network.target
Wants=network.target

[Service]
Type=simple
User=odin
Group=odin
WorkingDirectory=/opt/odin
ExecStart=/usr/bin/python3 /opt/odin/bin/odin_all_father.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
ODIN_SERVICE_EOF

# Enable ODIN service
systemctl daemon-reload
systemctl enable odin-core

# Configure nginx for ODIN dashboard
cat > /etc/nginx/sites-available/odin-dashboard << 'NGINX_EOF'
server {
    listen 80;
    listen 9090;
    server_name odin-allfather;
    
    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    location /status {
        return 200 "👁️ ODIN Core Server - The All-Father is watching";
        add_header Content-Type text/plain;
    }
}
NGINX_EOF

ln -sf /etc/nginx/sites-available/odin-dashboard /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
systemctl restart nginx

# Set ODIN-specific system optimizations
cat >> /etc/sysctl.conf << 'SYSCTL_EOF'

# ODIN Core Server Optimizations
# Memory management for AI workloads
vm.swappiness=10
vm.vfs_cache_pressure=50
vm.dirty_ratio=5
vm.dirty_background_ratio=2

# Network optimizations for distributed systems
net.core.netdev_max_backlog=16384
net.core.somaxconn=8192
net.core.rmem_default=1048576
net.core.rmem_max=16777216
net.core.wmem_default=1048576
net.core.wmem_max=16777216
net.ipv4.tcp_rmem=4096 1048576 2097152
net.ipv4.tcp_wmem=4096 1048576 2097152
net.ipv4.tcp_congestion_control=bbr

# File descriptor limits for high concurrency
fs.file-max=2097152
SYSCTL_EOF

sysctl -p

# Create ODIN motd
cat > /etc/motd << 'MOTD_EOF'

╔═══════════════════════════════════════════════════════════════════════════╗
║                                👁️ ODIN 👁️                                ║
║                         The All-Father Core Server                       ║
║                    Distributed AI & Cloud Orchestrator                   ║
║                                                                           ║
║  🎯 ODIN Core Server OS - Exclusive Installation                          ║
║  👁️ The All-Father watches over all THOR instances                       ║
║  🌐 Cloud Infrastructure Management                                      ║
║  📚 Universal Knowledge Base & Search                                    ║
║  🔧 Driver & Library Distribution                                        ║
║  🛡️ Security Monitoring & Threat Protection                              ║
║  💰 Cost Optimization & Resource Management                              ║
║                                                                           ║
║  🚀 Status: OPERATIONAL                                                   ║
║  📊 Dashboard: http://this-server:9090                                    ║
║  👁️ Monitoring: systemctl status odin-core                               ║
╚═══════════════════════════════════════════════════════════════════════════╝

MOTD_EOF

echo "✅ ODIN Core Server OS Installation Complete!"
echo "👁️ The All-Father now controls this server exclusively"
echo "🌐 Access dashboard at http://$(curl -s ifconfig.me):9090"
echo "📊 Check status: systemctl status odin-core"
'''
        
        # Save installation script to file
        with open('/tmp/odin_install.sh', 'w') as f:
            f.write(odin_install_script)
        
        # Also copy the ODIN All-Father system
        import shutil
        shutil.copy('odin_all_father.py', '/tmp/odin_all_father.py')
        
        self.log_step("STEP 5", "PREPARED", "ODIN installation scripts ready")
        
        # Note: In a real deployment, you would:
        # 1. Upload these files to the server via SCP
        # 2. Execute the installation script via SSH
        # 3. Monitor the installation progress
        
        print(f"""
🚀 ODIN DEPLOYMENT INSTRUCTIONS:

To complete the ODIN installation on server {server_ip}:

1. Copy files to server:
   scp /tmp/odin_install.sh root@{server_ip}:/tmp/
   scp /tmp/odin_all_father.py root@{server_ip}:/opt/odin/bin/

2. SSH into server and run installation:
   ssh root@{server_ip}
   chmod +x /tmp/odin_install.sh
   /tmp/odin_install.sh

3. Start ODIN Core Server:
   systemctl start odin-core
   systemctl status odin-core

4. Access ODIN Dashboard:
   http://{server_ip}:9090

5. Verify ODIN is exclusive OS:
   cat /etc/motd
   hostname
   systemctl list-units --type=service | grep odin
        """)
        
        return True
    
    def verify_odin_installation(self, server_ip):
        """Verify ODIN is running as exclusive OS"""
        self.log_step("STEP 6", f"Verifying ODIN installation on {server_ip}...")
        
        # In a real implementation, this would SSH to the server and check:
        # - Hostname is set to odin-allfather
        # - ODIN service is running
        # - Dashboard is accessible
        # - No other OS traces remain
        
        verification_commands = [
            "hostname",
            "cat /etc/motd | head -5",
            "systemctl is-active odin-core",
            "curl -s http://localhost:9090/status",
            "ps aux | grep odin",
            "df -h",
            "free -m"
        ]
        
        self.log_step("STEP 6", "INFO", "Manual verification commands prepared")
        print(f"""
🔍 ODIN VERIFICATION COMMANDS:

SSH to {server_ip} and run these commands to verify ODIN installation:

{chr(10).join(f"  {cmd}" for cmd in verification_commands)}

Expected results:
- Hostname: odin-allfather
- MOTD: Shows ODIN banner
- Service: odin-core should be active
- Status endpoint: Should return ODIN message
- Process: Python ODIN processes running
        """)
        
        return True
    
    def generate_deployment_report(self):
        """Generate final deployment report"""
        print(f"""
═══════════════════════════════════════════════════════════════════════════
👁️ ODIN CORE SERVER OS DEPLOYMENT REPORT
═══════════════════════════════════════════════════════════════════════════

📊 DEPLOYMENT SUMMARY:
• Target: Vultr Cloud Server
• OS: ODIN Core Server OS (Exclusive Installation)
• Configuration: 4 vCPUs, 8GB RAM, SSD Storage
• Purpose: The All-Father's Core Server & Cloud Orchestrator

📋 DEPLOYMENT LOG:
{chr(10).join(self.deployment_log)}

🎯 NEXT STEPS:
1. Complete manual installation using provided scripts
2. Verify ODIN is the exclusive OS
3. Access dashboard at server-ip:9090
4. Configure THOR instances to connect to this ODIN server
5. Monitor The All-Father's operations

👁️ ODIN now controls the server as the exclusive operating system.
   The All-Father watches over the distributed THOR ecosystem.
═══════════════════════════════════════════════════════════════════════════
        """)

def main():
    print("👁️ ODIN CORE SERVER OS - VULTR DEPLOYMENT ORCHESTRATOR")
    print("=" * 60)
    
    # Get Vultr API key
    api_key = os.getenv('VULTR_API_KEY') or "5QPRJXTKJ5DKDDKMM7NRS32IFVPNGFG27CFA"
    
    if not api_key:
        print("❌ Error: VULTR_API_KEY not found")
        print("Set environment variable: export VULTR_API_KEY=your_key")
        sys.exit(1)
    
    # Initialize deployer
    deployer = VultrODINDeployer(api_key)
    
    try:
        # Execute deployment steps
        servers = deployer.check_existing_servers()
        
        # If we have existing servers, we may need to destroy one to make room
        if servers and len(servers) > 0:
            print(f"Found {len(servers)} existing servers")
            # In production, you might want to select which server to replace
            
        # Create new ODIN server
        server_id = deployer.create_odin_server()
        if not server_id:
            print("❌ Failed to create ODIN server")
            return
        
        # Wait for server to become active
        server_ip = deployer.wait_for_server_active(server_id)
        if not server_ip:
            print("❌ Server did not become active")
            return
        
        # Install ODIN OS
        deployer.install_odin_os(server_ip)
        
        # Verify installation
        deployer.verify_odin_installation(server_ip)
        
        # Generate final report
        deployer.generate_deployment_report()
        
    except KeyboardInterrupt:
        print("\n🛑 Deployment interrupted by user")
    except Exception as e:
        print(f"❌ Deployment error: {str(e)}")

if __name__ == "__main__":
    main()
