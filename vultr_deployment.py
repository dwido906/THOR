#!/usr/bin/env python3
"""
🚀 VULTR AUTO-DEPLOYMENT SYSTEM
Deploy THOR-AI to Vultr servers automatically with SSL and security
"""

import requests
import time
import os
import subprocess
from datetime import datetime
import json

class VultrDeployment:
    """Automated Vultr server deployment"""
    
    def __init__(self):
        self.api_key = "YOUR_VULTR_API_KEY"  # Get from Vultr dashboard
        self.base_url = "https://api.vultr.com/v2"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Server configurations
        self.server_configs = {
            'web_server': {
                'region': 'ewr',  # New Jersey (close to you)
                'plan': 'vc2-1c-1gb',  # $6/month - perfect for starting
                'os_id': 387,  # Ubuntu 20.04 LTS
                'label': 'thor-ai-web-server',
                'hostname': 'thor-web',
                'enable_ipv6': True,
                'enable_private_network': True,
                'ddos_protection': True
            },
            'database_server': {
                'region': 'ewr',
                'plan': 'vc2-2c-4gb',  # $24/month - database needs more resources
                'os_id': 387,
                'label': 'thor-ai-database',
                'hostname': 'thor-db',
                'enable_ipv6': True,
                'enable_private_network': True,
                'ddos_protection': True
            },
            'ai_processing': {
                'region': 'ewr',
                'plan': 'vhf-8c-32gb',  # $192/month - AI needs power
                'os_id': 387,
                'label': 'thor-ai-processing',
                'hostname': 'thor-ai',
                'enable_ipv6': True,
                'enable_private_network': True,
                'ddos_protection': True
            }
        }
        
    def create_server(self, server_type):
        """Create a new Vultr server"""
        print(f"🚀 Creating {server_type} server...")
        
        config = self.server_configs[server_type]
        
        # Create startup script
        startup_script = self.generate_startup_script(server_type)
        
        # Create server
        response = requests.post(
            f"{self.base_url}/instances",
            headers=self.headers,
            json={
                **config,
                'script_id': self.upload_startup_script(startup_script)
            }
        )
        
        if response.status_code == 201:
            server_data = response.json()
            server_id = server_data['instance']['id']
            print(f"✅ Server created! ID: {server_id}")
            return server_id
        else:
            print(f"❌ Failed to create server: {response.text}")
            return None
            
    def upload_startup_script(self, script_content):
        """Upload startup script to Vultr"""
        response = requests.post(
            f"{self.base_url}/startup-scripts",
            headers=self.headers,
            json={
                'name': f'thor-ai-setup-{int(time.time())}',
                'script': script_content,
                'type': 'boot'
            }
        )
        
        if response.status_code == 201:
            return response.json()['startup_script']['id']
        else:
            print(f"❌ Failed to upload script: {response.text}")
            return None
    
    def generate_startup_script(self, server_type):
        """Generate Ubuntu startup script for different server types"""
        
        base_setup = """#!/bin/bash
# THOR-AI Server Setup Script
set -e

# Update system
apt-get update -y
apt-get upgrade -y

# Install Python 3.9+
apt-get install -y python3.9 python3.9-pip python3.9-venv
ln -sf /usr/bin/python3.9 /usr/bin/python3
ln -sf /usr/bin/pip3 /usr/bin/pip

# Install essential packages
apt-get install -y git curl wget nginx certbot python3-certbot-nginx
apt-get install -y htop fail2ban ufw redis-server

# Configure firewall
ufw allow ssh
ufw allow http
ufw allow https
ufw --force enable

# Configure fail2ban for security
systemctl enable fail2ban
systemctl start fail2ban

# Create thor user
useradd -m -s /bin/bash thor
usermod -aG sudo thor

# Clone THOR-AI repository (you'll need to make this public or use deploy keys)
cd /home/thor
git clone https://github.com/yourusername/thor-ai.git || echo "Repository not available yet"

# Install Python dependencies
cd /home/thor/thor-ai || cd /home/thor
"""

        if server_type == 'web_server':
            return base_setup + """
# Web server specific setup
pip3 install flask flask-cors flask-limiter stripe gunicorn

# Configure nginx
cat > /etc/nginx/sites-available/thor-ai << 'EOF'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

ln -s /etc/nginx/sites-available/thor-ai /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl restart nginx

# Create systemd service
cat > /etc/systemd/system/thor-ai.service << 'EOF'
[Unit]
Description=THOR-AI Web Server
After=network.target

[Service]
User=thor
Group=thor
WorkingDirectory=/home/thor/thor-ai
Environment=PATH=/home/thor/thor-ai/venv/bin
ExecStart=/usr/bin/python3 /home/thor/thor-ai/production_server.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable thor-ai

echo "🚀 Web server setup complete!"
"""

        elif server_type == 'database_server':
            return base_setup + """
# Database server specific setup
apt-get install -y postgresql postgresql-contrib
systemctl start postgresql
systemctl enable postgresql

# Setup PostgreSQL for THOR-AI
sudo -u postgres createuser --interactive thor
sudo -u postgres createdb thor_ai
sudo -u postgres psql -c "ALTER USER thor PASSWORD 'secure_password_change_this';"

# Install SQLite for development
apt-get install -y sqlite3

# Configure PostgreSQL for remote connections (secure)
echo "host thor_ai thor 10.0.0.0/8 md5" >> /etc/postgresql/12/main/pg_hba.conf
echo "listen_addresses = '10.0.0.1'" >> /etc/postgresql/12/main/postgresql.conf
systemctl restart postgresql

echo "🗄️ Database server setup complete!"
"""

        elif server_type == 'ai_processing':
            return base_setup + """
# AI processing server setup
apt-get install -y python3-dev python3-numpy python3-scipy
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip3 install transformers datasets scikit-learn networkx

# Install AI dependencies
pip3 install openai anthropic langchain chromadb

# Create AI processing directories
mkdir -p /home/thor/ai_models
mkdir -p /home/thor/ai_data
mkdir -p /home/thor/ai_logs

# Configure for AI workload
echo 'vm.swappiness=10' >> /etc/sysctl.conf
echo 'net.core.rmem_max=134217728' >> /etc/sysctl.conf
echo 'net.core.wmem_max=134217728' >> /etc/sysctl.conf

# Create AI service
cat > /etc/systemd/system/thor-ai-processing.service << 'EOF'
[Unit]
Description=THOR-AI Processing Service
After=network.target

[Service]
User=thor
Group=thor
WorkingDirectory=/home/thor/thor-ai
ExecStart=/usr/bin/python3 /home/thor/thor-ai/trinity_ai_system.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable thor-ai-processing

echo "🤖 AI processing server setup complete!"
"""
        
        return base_setup

    def get_server_info(self, server_id):
        """Get server information"""
        response = requests.get(
            f"{self.base_url}/instances/{server_id}",
            headers=self.headers
        )
        
        if response.status_code == 200:
            return response.json()['instance']
        return None

    def wait_for_server(self, server_id, timeout=300):
        """Wait for server to be ready"""
        print(f"⏳ Waiting for server {server_id} to be ready...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            info = self.get_server_info(server_id)
            if info and info['status'] == 'active':
                print(f"✅ Server {server_id} is ready!")
                print(f"🌐 IP Address: {info['main_ip']}")
                return info
            
            time.sleep(30)
            print("⏳ Still waiting...")
        
        print(f"❌ Server {server_id} took too long to start")
        return None

    def setup_ssl_certificate(self, server_ip, domain):
        """Setup SSL certificate with Let's Encrypt"""
        print(f"🔒 Setting up SSL for {domain}...")
        
        # SSH command to setup SSL
        ssl_command = f"""
ssh root@{server_ip} '
certbot --nginx -d {domain} --non-interactive --agree-tos --email your-email@example.com
systemctl reload nginx
'
"""
        
        print("Run this command after DNS is configured:")
        print(ssl_command)

    def deploy_full_stack(self):
        """Deploy complete THOR-AI stack"""
        print("🚀 DEPLOYING THOR-AI TO VULTR CLOUD")
        print("=" * 50)
        
        deployment_log = {
            'started_at': datetime.now().isoformat(),
            'servers': {}
        }
        
        # Deploy each server type
        for server_type in ['web_server', 'database_server', 'ai_processing']:
            print(f"\n📦 Deploying {server_type}...")
            
            server_id = self.create_server(server_type)
            if server_id:
                server_info = self.wait_for_server(server_id)
                if server_info:
                    deployment_log['servers'][server_type] = {
                        'server_id': server_id,
                        'ip_address': server_info['main_ip'],
                        'status': 'deployed'
                    }
                    
                    print(f"✅ {server_type} deployed successfully!")
                    print(f"   Server ID: {server_id}")
                    print(f"   IP Address: {server_info['main_ip']}")
                else:
                    deployment_log['servers'][server_type] = {
                        'server_id': server_id,
                        'status': 'failed'
                    }
        
        # Save deployment log
        with open('/Users/dwido/TRINITY/vultr_deployment.json', 'w') as f:
            json.dump(deployment_log, f, indent=2)
        
        print("\n🎉 DEPLOYMENT COMPLETE!")
        print("=" * 50)
        print("💡 Next steps:")
        print("1. Configure your domain DNS to point to the web server IP")
        print("2. Run SSL setup script")
        print("3. Update Stripe webhook URLs")
        print("4. Configure database connections")
        print("5. Test all systems")
        
        return deployment_log

    def get_cost_estimate(self):
        """Calculate monthly costs"""
        costs = {
            'web_server': 6,     # $6/month
            'database_server': 24,  # $24/month
            'ai_processing': 192    # $192/month
        }
        
        total = sum(costs.values())
        
        print("💰 VULTR COST ESTIMATE")
        print("=" * 30)
        for server, cost in costs.items():
            print(f"{server.replace('_', ' ').title()}: ${cost}/month")
        print("-" * 30)
        print(f"Total Monthly Cost: ${total}/month")
        print(f"Daily Cost: ${total/30:.2f}/day")
        print()
        print("💡 Revenue needed to break even: 4 Gaming Pro subscribers ($15 each)")
        print("🚀 Target: 100+ subscribers = $1,500/month revenue")
        print(f"📈 Profit after server costs: ${1500 - total}/month")

if __name__ == "__main__":
    deployer = VultrDeployment()
    
    print("🚀 THOR-AI VULTR DEPLOYMENT SYSTEM")
    print("=" * 40)
    print()
    
    # Show cost estimate first
    deployer.get_cost_estimate()
    
    print("\n⚠️  BEFORE DEPLOYING:")
    print("1. Set your VULTR_API_KEY in this script")
    print("2. Make sure you have enough Vultr credits")
    print("3. Prepare your domain for DNS configuration")
    print()
    
    choice = input("Deploy to Vultr? (y/N): ").lower()
    
    if choice == 'y':
        deployment_result = deployer.deploy_full_stack()
        print(f"\n📄 Deployment details saved to: /Users/dwido/TRINITY/vultr_deployment.json")
    else:
        print("🛑 Deployment cancelled. Ready when you are!")
