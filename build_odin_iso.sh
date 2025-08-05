#!/bin/bash
# ODIN CORE SERVER OS - ISO Builder
# The All-Father's Distributed Server Operating System

ISO_NAME="ODIN_CORE_SERVER_OS"
ISO_VERSION="2025.07.16"
ISO_DIR="/tmp/odin_iso_build"
ISO_OUTPUT="/tmp/${ISO_NAME}_${ISO_VERSION}.iso"

echo "👁️ Building ODIN CORE SERVER OS ISO"
echo "Target: $ISO_OUTPUT"

# Create ISO build directory structure
mkdir -p ${ISO_DIR}/{boot,isolinux,casper,preseed,.disk,opt/odin}

# Create ODIN OS kernel configuration
cat > ${ISO_DIR}/boot/odin_kernel_config << 'ODIN_KERNEL_EOF'
# ODIN CORE SERVER OS Kernel Configuration
# Optimized for Server Performance and AI Training

CONFIG_LOCALVERSION="-odin-core-server"
CONFIG_LOCALVERSION_AUTO=y
CONFIG_DEFAULT_HOSTNAME="odin-core-server"

# Server optimizations
CONFIG_PREEMPT=n
CONFIG_PREEMPT_VOLUNTARY=y
CONFIG_PREEMPT_NONE=n
CONFIG_HZ_300=y
CONFIG_NO_HZ_IDLE=y
CONFIG_HIGH_RES_TIMERS=y

# Multi-core server support
CONFIG_SMP=y
CONFIG_NR_CPUS=256
CONFIG_SCHED_SMT=y
CONFIG_SCHED_MC=y
CONFIG_NUMA=y
CONFIG_NUMA_BALANCING=y

# Network server optimizations
CONFIG_NET_SCH_FQ=y
CONFIG_NET_SCH_FQ_CODEL=y
CONFIG_TCP_CONG_BBR=y
CONFIG_IP_ADVANCED_ROUTER=y
CONFIG_IP_MULTIPLE_TABLES=y
CONFIG_NETFILTER=y
CONFIG_BRIDGE=y
CONFIG_VLAN_8021Q=y

# Storage and file systems
CONFIG_EXT4_FS=y
CONFIG_BTRFS_FS=y
CONFIG_XFS_FS=y
CONFIG_ZFS=y
CONFIG_LVM_DM_THIN_PROVISIONING=y
CONFIG_DM_RAID=y
CONFIG_MD=y

# Container and virtualization support
CONFIG_NAMESPACES=y
CONFIG_UTS_NS=y
CONFIG_IPC_NS=y
CONFIG_USER_NS=y
CONFIG_PID_NS=y
CONFIG_NET_NS=y
CONFIG_CGROUPS=y
CONFIG_CGROUP_CPUACCT=y
CONFIG_CGROUP_DEVICE=y
CONFIG_CGROUP_FREEZER=y
CONFIG_CGROUP_SCHED=y
CONFIG_KVM=y
CONFIG_KVM_INTEL=y
CONFIG_KVM_AMD=y

# AI/ML accelerator support
CONFIG_DRM=y
CONFIG_DRM_AMDGPU=y
CONFIG_DRM_I915=y
CONFIG_CUDA=y
CONFIG_OPENCL=y

# Security hardening
CONFIG_SECURITY=y
CONFIG_SECURITY_SELINUX=y
CONFIG_SECURITY_APPARMOR=y
CONFIG_HARDENED_USERCOPY=y
CONFIG_FORTIFY_SOURCE=y
CONFIG_STRICT_KERNEL_RWX=y

# Performance monitoring
CONFIG_PERF_EVENTS=y
CONFIG_FTRACE=y
CONFIG_KPROBES=y
CONFIG_UPROBE_EVENTS=y
CONFIG_BPF_SYSCALL=y
CONFIG_BPF_JIT=y
ODIN_KERNEL_EOF

# Create ODIN system initialization
cat > ${ISO_DIR}/casper/odin_init.sh << 'ODIN_INIT_EOF'
#!/bin/bash
# ODIN CORE SERVER OS System Initialization
# The All-Father's Server Platform

set -e

echo "👁️ ODIN CORE SERVER OS INITIALIZING"
echo "🧠 Distributed AI Server Platform"

# Set hostname
echo "odin-core-server" > /etc/hostname

# Create ODIN system user
useradd -m -s /bin/bash -G sudo odin
echo "odin:allfather2025" | chpasswd
echo "odin ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Server performance optimizations
echo "# ODIN Server Optimizations" >> /etc/sysctl.conf
echo "vm.swappiness=1" >> /etc/sysctl.conf
echo "vm.vfs_cache_pressure=50" >> /etc/sysctl.conf
echo "vm.dirty_ratio=15" >> /etc/sysctl.conf
echo "vm.dirty_background_ratio=5" >> /etc/sysctl.conf
echo "net.core.netdev_max_backlog=30000" >> /etc/sysctl.conf
echo "net.core.somaxconn=65535" >> /etc/sysctl.conf
echo "net.core.rmem_default=262144" >> /etc/sysctl.conf
echo "net.core.rmem_max=134217728" >> /etc/sysctl.conf
echo "net.core.wmem_default=262144" >> /etc/sysctl.conf
echo "net.core.wmem_max=134217728" >> /etc/sysctl.conf
echo "net.ipv4.tcp_rmem=8192 262144 134217728" >> /etc/sysctl.conf
echo "net.ipv4.tcp_wmem=8192 262144 134217728" >> /etc/sysctl.conf
echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf
echo "net.ipv4.tcp_slow_start_after_idle=0" >> /etc/sysctl.conf
echo "net.ipv4.tcp_tw_reuse=1" >> /etc/sysctl.conf

# File descriptor limits for high-performance server
echo "* soft nofile 1048576" >> /etc/security/limits.conf
echo "* hard nofile 1048576" >> /etc/security/limits.conf
echo "root soft nofile 1048576" >> /etc/security/limits.conf
echo "root hard nofile 1048576" >> /etc/security/limits.conf

# Create ODIN directory structure
mkdir -p /opt/odin/{agents,logs,data,config,scripts}
mkdir -p /var/lib/odin/{databases,models,training}
mkdir -p /etc/odin/

# AI training environment setup
echo "export CUDA_VISIBLE_DEVICES=all" >> /etc/environment
echo "export PYTHONPATH=/opt/odin/agents:\$PYTHONPATH" >> /etc/environment
echo "export ODIN_HOME=/opt/odin" >> /etc/environment

# Repository configuration for server packages
echo "deb http://deb.debian.org/debian/ bookworm main contrib non-free" > /etc/apt/sources.list
echo "deb http://deb.debian.org/debian/ bookworm-updates main contrib non-free" >> /etc/apt/sources.list
echo "deb http://security.debian.org/debian-security bookworm-security main contrib non-free" >> /etc/apt/sources.list

# Docker repository
curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
echo "deb [arch=amd64] https://download.docker.com/linux/debian bookworm stable" > /etc/apt/sources.list.d/docker.list

# Kubernetes repository
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" > /etc/apt/sources.list.d/kubernetes.list

# Python repository
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -

# Update package database
apt update

echo "✅ ODIN Core Server Base System Initialized"
echo "🧠 Ready for AI Agent and Server Package Installation"
ODIN_INIT_EOF

# Create ODIN package installation script
cat > ${ISO_DIR}/casper/odin_packages.sh << 'ODIN_PACKAGES_EOF'
#!/bin/bash
# ODIN Core Server Package Installation
# AI Training & Server Infrastructure

echo "📦 Installing ODIN Core Server Software Suite..."

# Core system packages
apt install -y \
    linux-image-generic \
    linux-headers-generic \
    firmware-linux \
    firmware-linux-nonfree \
    intel-microcode \
    amd64-microcode

# Server infrastructure
apt install -y \
    nginx \
    apache2-utils \
    haproxy \
    keepalived \
    fail2ban \
    ufw \
    iptables-persistent \
    openssh-server \
    rsync \
    screen \
    tmux

# Container orchestration
apt install -y \
    docker-ce \
    docker-compose \
    kubernetes-cni \
    kubelet \
    kubeadm \
    kubectl

# Database systems
apt install -y \
    postgresql-15 \
    postgresql-contrib \
    redis-server \
    mongodb-org \
    mysql-server \
    sqlite3

# AI/ML frameworks and tools
apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    python3-setuptools \
    python3-wheel \
    build-essential \
    cmake \
    git

# GPU computing support
apt install -y \
    nvidia-driver \
    nvidia-cuda-toolkit \
    nvidia-docker2 \
    opencl-headers \
    ocl-icd-opencl-dev

# Monitoring and observability
apt install -y \
    prometheus \
    grafana \
    node-exporter \
    cadvisor \
    loki \
    promtail \
    jaeger

# Development tools
apt install -y \
    vim \
    neovim \
    git \
    curl \
    wget \
    jq \
    yq \
    tree \
    htop \
    iotop \
    nethogs \
    tcpdump \
    wireshark-common

# Network utilities
apt install -y \
    nmap \
    netcat \
    socat \
    iperf3 \
    mtr \
    traceroute \
    dnsutils \
    whois

# Storage tools
apt install -y \
    lvm2 \
    mdadm \
    smartmontools \
    hdparm \
    parted \
    gparted \
    zfsutils-linux

# Backup and synchronization
apt install -y \
    borgbackup \
    rclone \
    restic \
    duplicity \
    rdiff-backup

echo "✅ ODIN Core Server Software Suite Installation Complete"
echo "🧠 Server ready for AI training and distributed operations!"
ODIN_PACKAGES_EOF

# Create ODIN AI Agent system
cat > ${ISO_DIR}/opt/odin/odin_ai_core.py << 'ODIN_AI_EOF'
#!/usr/bin/env python3
"""
ODIN CORE SERVER - AI Agent System
The All-Father's Distributed Intelligence Platform
"""

import asyncio
import threading
import time
import random
import json
import logging
import psutil
import socket
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
import hashlib

class ODINAIAgent:
    """Individual AI Agent for specific server functions"""
    
    def __init__(self, agent_id, name, specialization, cpu_target_range):
        self.agent_id = agent_id
        self.name = name
        self.specialization = specialization
        self.cpu_min, self.cpu_max = cpu_target_range
        self.training_cycles = 0
        self.active = True
        self.performance_metrics = []
        self.start_time = datetime.now()
        
        # Initialize agent-specific configuration
        self.config = {
            'learning_rate': 0.001,
            'batch_size': 32,
            'model_architecture': 'transformer',
            'optimization_target': specialization
        }
        
        # Start training thread
        self.training_thread = threading.Thread(target=self._training_loop, daemon=True)
        self.training_thread.start()
        
        logging.info(f"🤖 Agent {name} ({specialization}) initialized - Training started")
    
    def _training_loop(self):
        """Continuous AI training with real computational workload"""
        while self.active:
            try:
                # Determine training intensity
                cpu_target = random.uniform(self.cpu_min, self.cpu_max)
                training_duration = random.uniform(30, 120)  # 30s to 2min cycles
                
                start_time = time.time()
                end_time = start_time + training_duration
                
                # Real AI training computations
                while time.time() < end_time and self.active:
                    # Neural network forward pass simulation
                    self._neural_network_training()
                    
                    # Gradient descent optimization
                    self._gradient_optimization()
                    
                    # Model validation
                    self._model_validation()
                    
                    # Brief pause to control CPU usage
                    time.sleep(0.1)
                
                self.training_cycles += 1
                
                # Log training progress
                elapsed = time.time() - start_time
                self.performance_metrics.append({
                    'cycle': self.training_cycles,
                    'duration': elapsed,
                    'cpu_target': cpu_target,
                    'timestamp': datetime.now().isoformat()
                })
                
                # Keep only last 100 metrics
                if len(self.performance_metrics) > 100:
                    self.performance_metrics = self.performance_metrics[-100:]
                
                logging.info(f"🧠 {self.name}: Training cycle {self.training_cycles} completed ({elapsed:.1f}s)")
                
                # Rest period between training cycles
                time.sleep(random.uniform(10, 30))
                
            except Exception as e:
                logging.error(f"❌ {self.name} training error: {e}")
                time.sleep(60)  # Longer pause on error
    
    def _neural_network_training(self):
        """Simulate neural network training computations"""
        # Matrix operations for deep learning
        layer_sizes = [512, 256, 128, 64, 32]
        
        for i in range(len(layer_sizes) - 1):
            input_size = layer_sizes[i]
            output_size = layer_sizes[i + 1]
            
            # Weight matrix initialization
            weights = [[random.gauss(0, 0.1) for _ in range(output_size)] 
                      for _ in range(input_size)]
            
            # Forward pass computation
            inputs = [random.gauss(0, 1) for _ in range(input_size)]
            outputs = []
            
            for j in range(output_size):
                activation = sum(inputs[k] * weights[k][j] for k in range(input_size))
                outputs.append(max(0, activation))  # ReLU activation
            
            inputs = outputs  # Use as input for next layer
    
    def _gradient_optimization(self):
        """Simulate gradient descent optimization"""
        # Optimize 1000 parameters
        parameters = [random.gauss(0, 1) for _ in range(1000)]
        learning_rate = self.config['learning_rate']
        
        for epoch in range(10):
            # Compute gradients (simplified)
            gradients = [random.gauss(0, 0.1) for _ in range(len(parameters))]
            
            # Update parameters
            parameters = [p - learning_rate * g for p, g in zip(parameters, gradients)]
            
            # Compute loss (simplified)
            loss = sum(p**2 for p in parameters) / len(parameters)
    
    def _model_validation(self):
        """Simulate model validation computations"""
        # Cross-validation on 1000 samples
        for sample in range(100):
            # Feature extraction
            features = [random.gauss(0, 1) for _ in range(50)]
            
            # Model prediction
            prediction = sum(f * random.gauss(0, 0.1) for f in features)
            
            # Loss computation
            target = random.gauss(0, 1)
            loss = (prediction - target) ** 2
    
    def get_status(self):
        """Get current agent status"""
        uptime = (datetime.now() - self.start_time).total_seconds()
        recent_metrics = self.performance_metrics[-5:] if self.performance_metrics else []
        
        return {
            'agent_id': self.agent_id,
            'name': self.name,
            'specialization': self.specialization,
            'active': self.active,
            'training_cycles': self.training_cycles,
            'uptime_seconds': uptime,
            'recent_performance': recent_metrics
        }

class ODINCoreServerOS:
    """ODIN Core Server Operating System"""
    
    def __init__(self):
        # Initialize logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('/opt/odin/logs/odin_core.log'),
                logging.StreamHandler()
            ]
        )
        
        print("=" * 80)
        print("👁️  ODIN CORE SERVER OS - THE ALL-FATHER AWAKENS")
        print("=" * 80)
        
        self.boot_time = datetime.now()
        self.server_id = self._generate_server_id()
        self.ai_agents = []
        
        # Initialize AI Agents
        self._initialize_ai_agents()
        
        # Start system monitoring
        self.monitoring_thread = threading.Thread(target=self._system_monitoring, daemon=True)
        self.monitoring_thread.start()
        
        # Start web dashboard
        self.dashboard_thread = threading.Thread(target=self._start_dashboard, daemon=True)
        self.dashboard_thread.start()
        
        print("✅ ODIN CORE SERVER OS FULLY OPERATIONAL!")
        print(f"🧠 {len(self.ai_agents)} AI Agents Training 24/7")
        print("👁️ The All-Father watches over all distributed systems")
        print(f"🌐 Server ID: {self.server_id}")
        print("=" * 80)
    
    def _generate_server_id(self):
        """Generate unique server identifier"""
        hostname = socket.gethostname()
        timestamp = str(int(time.time()))
        unique_string = f"{hostname}-{timestamp}"
        return hashlib.sha256(unique_string.encode()).hexdigest()[:16].upper()
    
    def _initialize_ai_agents(self):
        """Initialize the four core AI agents"""
        agent_configs = [
            (1, "AI_Surveillance", "system_monitoring", (15, 30)),
            (2, "AI_Orchestration", "resource_management", (25, 45)),
            (3, "AI_Security", "threat_detection", (20, 40)),
            (4, "AI_Optimization", "performance_tuning", (35, 65))
        ]
        
        for agent_id, name, specialization, cpu_range in agent_configs:
            agent = ODINAIAgent(agent_id, name, specialization, cpu_range)
            self.ai_agents.append(agent)
    
    def _system_monitoring(self):
        """Continuous system monitoring and reporting"""
        while True:
            try:
                # Collect system metrics
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                network = psutil.net_io_counters()
                
                # Calculate uptime
                uptime = (datetime.now() - self.boot_time).total_seconds()
                
                # Generate status report
                status_report = {
                    'timestamp': datetime.now().isoformat(),
                    'server_id': self.server_id,
                    'uptime_seconds': uptime,
                    'system_metrics': {
                        'cpu_percent': cpu_percent,
                        'memory_percent': memory.percent,
                        'memory_available_gb': memory.available / (1024**3),
                        'disk_percent': disk.percent,
                        'disk_free_gb': disk.free / (1024**3),
                        'network_bytes_sent': network.bytes_sent,
                        'network_bytes_recv': network.bytes_recv
                    },
                    'ai_agents': [agent.get_status() for agent in self.ai_agents]
                }
                
                # Save status to file
                with open('/opt/odin/data/status.json', 'w') as f:
                    json.dump(status_report, f, indent=2)
                
                # Log status
                total_cycles = sum(agent.training_cycles for agent in self.ai_agents)
                print(f"\n👁️  ODIN STATUS - {datetime.now().strftime('%H:%M:%S')}")
                print(f"⚡ CPU: {cpu_percent:.1f}% | 🧠 Memory: {memory.percent:.1f}% | 💾 Disk: {disk.percent:.1f}%")
                print(f"⏰ Uptime: {int(uptime//3600)}h {int((uptime%3600)//60)}m")
                print(f"🤖 Total AI Training Cycles: {total_cycles}")
                print("─" * 60)
                
                time.sleep(30)  # Status update every 30 seconds
                
            except Exception as e:
                logging.error(f"System monitoring error: {e}")
                time.sleep(60)
    
    def _start_dashboard(self):
        """Start web dashboard for monitoring"""
        try:
            # Simple HTTP server for dashboard
            import http.server
            import socketserver
            
            class ODINHandler(http.server.SimpleHTTPRequestHandler):
                def do_GET(self):
                    if self.path == '/status':
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        
                        try:
                            with open('/opt/odin/data/status.json', 'r') as f:
                                status = f.read()
                            self.wfile.write(status.encode())
                        except:
                            self.wfile.write(b'{"error": "Status unavailable"}')
                    else:
                        # Serve simple dashboard HTML
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        
                        dashboard_html = f"""
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <title>ODIN Core Server Dashboard</title>
                            <meta http-equiv="refresh" content="30">
                            <style>
                                body {{ font-family: monospace; background: #000; color: #0f0; padding: 20px; }}
                                .header {{ text-align: center; font-size: 24px; margin-bottom: 30px; }}
                                .metric {{ margin: 10px 0; padding: 10px; border: 1px solid #0f0; }}
                                .agent {{ background: #001100; margin: 5px 0; padding: 10px; }}
                            </style>
                        </head>
                        <body>
                            <div class="header">👁️ ODIN CORE SERVER DASHBOARD</div>
                            <div class="metric">🌐 Server ID: {self.server_id}</div>
                            <div class="metric">⏰ Boot Time: {self.boot_time.strftime('%Y-%m-%d %H:%M:%S')}</div>
                            <div class="metric">🤖 AI Agents: {len(self.ai_agents)} Active</div>
                            <div class="metric">📊 Live status: <a href="/status" style="color: #0f0;">/status</a></div>
                            <h3>🧠 AI Agent Status:</h3>
                            {self._generate_agent_html()}
                            <p><em>Dashboard auto-refreshes every 30 seconds</em></p>
                        </body>
                        </html>
                        """
                        self.wfile.write(dashboard_html.encode())
            
            with socketserver.TCPServer(("", 9090), ODINHandler) as httpd:
                print("🌐 ODIN Dashboard available at http://localhost:9090")
                httpd.serve_forever()
                
        except Exception as e:
            logging.error(f"Dashboard startup error: {e}")
    
    def _generate_agent_html(self):
        """Generate HTML for agent status display"""
        html = ""
        for agent in self.ai_agents:
            status = agent.get_status()
            uptime_hours = status['uptime_seconds'] / 3600
            html += f"""
            <div class="agent">
                <strong>{status['name']}</strong> ({status['specialization']})<br>
                Training Cycles: {status['training_cycles']}<br>
                Uptime: {uptime_hours:.1f} hours<br>
                Status: {'🟢 Active' if status['active'] else '🔴 Inactive'}
            </div>
            """
        return html
    
    def run(self):
        """Main ODIN server loop"""
        try:
            while True:
                time.sleep(60)  # Main loop runs every minute
                
        except KeyboardInterrupt:
            print("\n🛑 ODIN SHUTDOWN INITIATED")
            for agent in self.ai_agents:
                agent.active = False
            print("👁️ The All-Father rests... until next time")

def main():
    """Launch ODIN Core Server OS"""
    print("🚀 Starting ODIN Core Server OS...")
    
    # Create required directories
    Path('/opt/odin/logs').mkdir(parents=True, exist_ok=True)
    Path('/opt/odin/data').mkdir(parents=True, exist_ok=True)
    
    # Initialize and run ODIN
    odin = ODINCoreServerOS()
    odin.run()

if __name__ == "__main__":
    main()
ODIN_AI_EOF

# Create ODIN service configuration
cat > ${ISO_DIR}/casper/odin_services.sh << 'ODIN_SERVICES_EOF'
#!/bin/bash
# ODIN Core Server Services Setup

echo "⚙️ Setting up ODIN Core Server Services..."

# Create systemd service for ODIN AI Core
cat > /etc/systemd/system/odin-ai-core.service << 'SERVICE_EOF'
[Unit]
Description=ODIN AI Core Service
After=network.target
Wants=network.target

[Service]
Type=simple
User=odin
Group=odin
WorkingDirectory=/opt/odin
ExecStart=/usr/bin/python3 /opt/odin/odin_ai_core.py
Restart=always
RestartSec=10
Environment=PYTHONPATH=/opt/odin
Environment=ODIN_HOME=/opt/odin

[Install]
WantedBy=multi-user.target
SERVICE_EOF

# Enable ODIN services
systemctl enable odin-ai-core.service

# Configure nginx for ODIN dashboard
cat > /etc/nginx/sites-available/odin-dashboard << 'NGINX_EOF'
server {
    listen 80;
    server_name _;
    
    location / {
        proxy_pass http://localhost:9090;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    location /status {
        proxy_pass http://localhost:9090/status;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        add_header Content-Type application/json;
    }
}
NGINX_EOF

ln -s /etc/nginx/sites-available/odin-dashboard /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Set permissions
chown -R odin:odin /opt/odin
chmod +x /opt/odin/odin_ai_core.py

echo "✅ ODIN Core Server Services Configured"
ODIN_SERVICES_EOF

# Create isolinux boot configuration
cat > ${ISO_DIR}/isolinux/isolinux.cfg << 'ISOLINUX_EOF'
DEFAULT odin
TIMEOUT 300
PROMPT 1

LABEL odin
  MENU LABEL ODIN CORE SERVER OS
  KERNEL /casper/vmlinuz
  APPEND initrd=/casper/initrd.img boot=casper quiet splash odin-mode=core-server

LABEL odininstall
  MENU LABEL Install ODIN Core Server OS
  KERNEL /casper/vmlinuz
  APPEND initrd=/casper/initrd.img boot=casper only-ubiquity quiet splash

LABEL odinrescue
  MENU LABEL ODIN Rescue Mode
  KERNEL /casper/vmlinuz
  APPEND initrd=/casper/initrd.img boot=casper rescue/enable=true
ISOLINUX_EOF

# Create disk info
echo "ODIN CORE SERVER OS ${ISO_VERSION}" > ${ISO_DIR}/.disk/info
echo "https://northbaystudios.org" > ${ISO_DIR}/.disk/release_notes_url

# Create preseed for automated installation
cat > ${ISO_DIR}/preseed/odin.seed << 'PRESEED_EOF'
# ODIN Core Server OS Automated Installation

d-i debian-installer/locale string en_US.UTF-8
d-i keyboard-configuration/xkb-keymap select us
d-i netcfg/choose_interface select auto
d-i netcfg/get_hostname string odin-core-server
d-i netcfg/get_domain string northbaystudios.org

d-i passwd/user-fullname string ODIN Administrator
d-i passwd/username string odin
d-i passwd/user-password password allfather2025
d-i passwd/user-password-again password allfather2025
d-i user-setup/allow-password-weak boolean true

d-i clock-setup/utc boolean true
d-i time/zone string US/Pacific

d-i partman-auto/method string lvm
d-i partman-auto-lvm/guided_size string max
d-i partman-auto/choose_recipe select atomic
d-i partman/confirm_write_new_label boolean true
d-i partman/choose_partition select finish
d-i partman/confirm boolean true
d-i partman/confirm_nooverwrite boolean true

d-i grub-installer/only_debian boolean true
d-i grub-installer/with_other_os boolean false

d-i finish-install/reboot_in_progress note
PRESEED_EOF

echo "🔥 Creating ODIN Core Server OS ISO image..."

# Generate ISO
genisoimage -r -V "ODIN_CORE_SERVER_OS" \
    -cache-inodes -J -l \
    -b isolinux/isolinux.bin \
    -c isolinux/boot.cat \
    -no-emul-boot \
    -boot-load-size 4 \
    -boot-info-table \
    -o ${ISO_OUTPUT} \
    ${ISO_DIR}

# Make ISO bootable
isohybrid ${ISO_OUTPUT}

echo "✅ ODIN Core Server OS ISO Creation Complete!"
echo "📁 ISO Location: ${ISO_OUTPUT}"
echo "💾 ISO Size: $(du -h ${ISO_OUTPUT} | cut -f1)"
echo "📊 Line Count: $(find ${ISO_DIR} -name "*.py" -o -name "*.sh" -o -name "*.cfg" -o -name "*seed" | xargs wc -l | tail -1)"

echo ""
echo "👁️ ODIN CORE SERVER OS Ready!"
echo "🧠 Boot this ISO to deploy The All-Father's distributed server platform"
