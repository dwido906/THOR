#!/usr/bin/env python3
"""
ODIN - The All-Seeing Watcher, Knowledgebase & Cloud Orchestrator
Companion to THOR OS: ONE MAN ARMY EDITION

ODIN Features:
- System Health & Security Monitoring
- Universal Knowledge Base & Search
- Driver/Library Management & Distribution
- Cloud Infrastructure Orchestration (Vultr API)
- Resource Optimization & Cost Management
- Secure Networking & Firewall Management

"The All-Father watches over all THOR instances"
"""

import asyncio
import os
import sys
import json
import time
import sqlite3
import logging
import threading
import subprocess
import requests
import psutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, asdict
import socket
import hashlib
import schedule
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# ODIN Version Information
ODIN_VERSION = "1.0.0"
ODIN_CODENAME = "ALL_FATHER"
ODIN_ROLE = "WATCHER_ORCHESTRATOR"

@dataclass
class ODINSystemInfo:
    """ODIN System Information"""
    version: str = ODIN_VERSION
    codename: str = ODIN_CODENAME
    role: str = ODIN_ROLE
    boot_time: Optional[datetime] = None
    watched_thor_instances: int = 0
    knowledge_entries: int = 0
    managed_drivers: int = 0
    cloud_servers_managed: int = 0
    security_threats_blocked: int = 0
    cost_savings_achieved: float = 0.0
    watching_active: bool = False
    cloud_orchestration_active: bool = False
    knowledge_indexing_active: bool = False

@dataclass
class THORInstance:
    """Monitored THOR Instance"""
    instance_id: str
    name: str
    address: str
    port: int
    last_seen: datetime
    health_status: str  # healthy, warning, critical, offline
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    disk_usage: float = 0.0
    vault_repos: int = 0
    sync_operations: int = 0
    p2p_peers: int = 0
    version: str = "unknown"

@dataclass
class KnowledgeEntry:
    """Knowledge Base Entry"""
    entry_id: str
    title: str
    content: str
    category: str
    tags: List[str]
    created: datetime
    updated: datetime
    relevance_score: float = 0.0
    access_count: int = 0

@dataclass
class DriverPackage:
    """Driver/Library Package"""
    package_id: str
    name: str
    version: str
    description: str
    download_url: str
    checksum: str
    platform: str  # windows, linux, macos, universal
    category: str  # gpu, audio, network, development
    size_bytes: int
    install_count: int = 0
    rating: float = 0.0

@dataclass
class CloudServer:
    """Managed Cloud Server"""
    server_id: str
    provider: str  # vultr, digitalocean, aws, etc.
    name: str
    region: str
    size: str
    status: str  # active, stopped, destroyed
    ip_address: str
    created: datetime
    monthly_cost: float
    thor_instance_id: Optional[str] = None

@dataclass
class SecurityThreat:
    """Security Threat Detection"""
    threat_id: str
    source_ip: str
    threat_type: str  # brute_force, port_scan, malware, suspicious_activity
    severity: str  # low, medium, high, critical
    detected: datetime
    blocked: bool = False
    details: str = ""

class ODINWatcher:
    """ODIN System Monitor - Watches all THOR instances"""
    
    def __init__(self):
        self.watched_instances: Dict[str, THORInstance] = {}
        self.is_watching = False
        self.watch_thread = None
        self.security_threats: Dict[str, SecurityThreat] = {}
        self.blocked_ips: Set[str] = set()
        
    def start_watching(self):
        """Start monitoring THOR instances"""
        self.is_watching = True
        self.watch_thread = threading.Thread(target=self._watch_loop, daemon=True)
        self.watch_thread.start()
        logging.info("👁️ ODIN Watcher started - Monitoring all THOR instances")
    
    def _watch_loop(self):
        """Main monitoring loop"""
        while self.is_watching:
            try:
                # Monitor system health
                self._monitor_system_health()
                
                # Monitor THOR instances
                self._monitor_thor_instances()
                
                # Monitor security threats
                self._monitor_security_threats()
                
                # Check resource usage
                self._monitor_resource_usage()
                
                time.sleep(30)  # Monitor every 30 seconds
                
            except Exception as e:
                logging.error(f"Watcher error: {e}")
    
    def _monitor_system_health(self):
        """Monitor overall system health"""
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        if cpu_percent > 90:
            logging.warning(f"🔥 High CPU usage detected: {cpu_percent}%")
        
        # Memory usage
        memory = psutil.virtual_memory()
        if memory.percent > 90:
            logging.warning(f"🔥 High memory usage detected: {memory.percent}%")
        
        # Disk usage
        disk = psutil.disk_usage('/')
        disk_percent = (disk.used / disk.total) * 100
        if disk_percent > 90:
            logging.warning(f"🔥 High disk usage detected: {disk_percent:.1f}%")
    
    def _monitor_thor_instances(self):
        """Monitor connected THOR instances"""
        # This would connect to THOR instances and check their health
        # For demo, simulate monitoring
        for instance_id, instance in self.watched_instances.items():
            try:
                # Simulate health check
                instance.last_seen = datetime.now()
                instance.health_status = "healthy"
                
            except Exception:
                instance.health_status = "offline"
    
    def _monitor_security_threats(self):
        """Monitor for security threats"""
        # This would implement actual threat detection
        # For demo, simulate threat monitoring
        pass
    
    def _monitor_resource_usage(self):
        """Monitor resource usage across all instances"""
        total_cpu = sum(instance.cpu_usage for instance in self.watched_instances.values())
        total_memory = sum(instance.memory_usage for instance in self.watched_instances.values())
        
        if total_cpu > 80:
            logging.warning(f"⚠️ High total CPU usage across instances: {total_cpu:.1f}%")
        
        if total_memory > 80:
            logging.warning(f"⚠️ High total memory usage across instances: {total_memory:.1f}%")
    
    def register_thor_instance(self, instance: THORInstance):
        """Register a THOR instance for monitoring"""
        self.watched_instances[instance.instance_id] = instance
        logging.info(f"📋 Registered THOR instance: {instance.name}")
    
    def get_health_report(self) -> dict:
        """Get comprehensive health report"""
        healthy_count = sum(1 for i in self.watched_instances.values() if i.health_status == "healthy")
        total_count = len(self.watched_instances)
        
        return {
            'instances_monitored': total_count,
            'healthy_instances': healthy_count,
            'unhealthy_instances': total_count - healthy_count,
            'security_threats_detected': len(self.security_threats),
            'blocked_ips': len(self.blocked_ips),
            'system_health': 'good' if healthy_count == total_count else 'needs_attention'
        }
    
    def stop_watching(self):
        """Stop monitoring"""
        self.is_watching = False
        if self.watch_thread:
            self.watch_thread.join()

class ODINKnowledgeBase:
    """ODIN Knowledge Base - Universal search and indexing"""
    
    def __init__(self, kb_path: str = "odin_knowledge"):
        self.kb_path = Path(kb_path)
        self.kb_path.mkdir(parents=True, exist_ok=True)
        self.db_path = self.kb_path / "knowledge.db"
        self.entries: Dict[str, KnowledgeEntry] = {}
        self._init_database()
        self._load_knowledge()
    
    def _init_database(self):
        """Initialize knowledge database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS knowledge_entries (
                    entry_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    category TEXT NOT NULL,
                    tags TEXT,
                    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    relevance_score REAL DEFAULT 0.0,
                    access_count INTEGER DEFAULT 0
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS search_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT NOT NULL,
                    results_count INTEGER,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
    
    def _load_knowledge(self):
        """Load knowledge entries from database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM knowledge_entries")
            for row in cursor:
                entry = KnowledgeEntry(
                    entry_id=row['entry_id'],
                    title=row['title'],
                    content=row['content'],
                    category=row['category'],
                    tags=json.loads(row['tags']) if row['tags'] else [],
                    created=datetime.fromisoformat(row['created']),
                    updated=datetime.fromisoformat(row['updated']),
                    relevance_score=row['relevance_score'],
                    access_count=row['access_count']
                )
                self.entries[entry.entry_id] = entry
    
    def add_knowledge(self, title: str, content: str, category: str, tags: Optional[List[str]] = None) -> KnowledgeEntry:
        """Add knowledge entry"""
        entry_id = hashlib.md5(f"{title}{content}".encode()).hexdigest()
        
        entry = KnowledgeEntry(
            entry_id=entry_id,
            title=title,
            content=content,
            category=category,
            tags=tags or [],
            created=datetime.now(),
            updated=datetime.now()
        )
        
        # Save to database
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO knowledge_entries 
                (entry_id, title, content, category, tags, created, updated)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                entry.entry_id, entry.title, entry.content, entry.category,
                json.dumps(entry.tags), entry.created.isoformat(), entry.updated.isoformat()
            ))
        
        self.entries[entry_id] = entry
        return entry
    
    def search_knowledge(self, query: str, category: Optional[str] = None) -> List[KnowledgeEntry]:
        """Search knowledge base"""
        results = []
        query_lower = query.lower()
        
        for entry in self.entries.values():
            score = 0.0
            
            # Title match (highest weight)
            if query_lower in entry.title.lower():
                score += 10.0
            
            # Content match
            if query_lower in entry.content.lower():
                score += 5.0
            
            # Tag match
            for tag in entry.tags:
                if query_lower in tag.lower():
                    score += 3.0
            
            # Category filter
            if category and entry.category != category:
                continue
            
            if score > 0:
                entry.relevance_score = score
                entry.access_count += 1
                results.append(entry)
        
        # Sort by relevance
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        
        # Save search history
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO search_history (query, results_count)
                VALUES (?, ?)
            """, (query, len(results)))
        
        return results
    
    def get_categories(self) -> List[str]:
        """Get all knowledge categories"""
        return list(set(entry.category for entry in self.entries.values()))
    
    def get_popular_entries(self, limit: int = 10) -> List[KnowledgeEntry]:
        """Get most accessed entries"""
        sorted_entries = sorted(self.entries.values(), key=lambda x: x.access_count, reverse=True)
        return sorted_entries[:limit]

class ODINDriverManager:
    """ODIN Driver/Library Manager"""
    
    def __init__(self, driver_path: str = "odin_drivers"):
        self.driver_path = Path(driver_path)
        self.driver_path.mkdir(parents=True, exist_ok=True)
        self.db_path = self.driver_path / "drivers.db"
        self.drivers: Dict[str, DriverPackage] = {}
        self._init_database()
        self._load_drivers()
    
    def _init_database(self):
        """Initialize driver database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS drivers (
                    package_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    version TEXT NOT NULL,
                    description TEXT,
                    download_url TEXT,
                    checksum TEXT,
                    platform TEXT,
                    category TEXT,
                    size_bytes INTEGER,
                    install_count INTEGER DEFAULT 0,
                    rating REAL DEFAULT 0.0,
                    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
    
    def _load_drivers(self):
        """Load drivers from database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM drivers")
            for row in cursor:
                driver = DriverPackage(
                    package_id=row['package_id'],
                    name=row['name'],
                    version=row['version'],
                    description=row['description'],
                    download_url=row['download_url'],
                    checksum=row['checksum'],
                    platform=row['platform'],
                    category=row['category'],
                    size_bytes=row['size_bytes'],
                    install_count=row['install_count'],
                    rating=row['rating']
                )
                self.drivers[driver.package_id] = driver
    
    def add_driver(self, name: str, version: str, description: str, 
                  download_url: str, platform: str, category: str, 
                  size_bytes: int) -> DriverPackage:
        """Add driver package"""
        package_id = hashlib.md5(f"{name}{version}{platform}".encode()).hexdigest()
        
        # Calculate checksum (in real implementation, download and verify)
        checksum = hashlib.sha256(f"{name}{version}".encode()).hexdigest()
        
        driver = DriverPackage(
            package_id=package_id,
            name=name,
            version=version,
            description=description,
            download_url=download_url,
            checksum=checksum,
            platform=platform,
            category=category,
            size_bytes=size_bytes
        )
        
        # Save to database
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO drivers 
                (package_id, name, version, description, download_url, checksum, 
                 platform, category, size_bytes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                driver.package_id, driver.name, driver.version, driver.description,
                driver.download_url, driver.checksum, driver.platform, 
                driver.category, driver.size_bytes
            ))
        
        self.drivers[package_id] = driver
        return driver
    
    def search_drivers(self, query: Optional[str] = None, category: Optional[str] = None, 
                      platform: Optional[str] = None) -> List[DriverPackage]:
        """Search for drivers"""
        results = []
        
        for driver in self.drivers.values():
            # Apply filters
            if category and driver.category != category:
                continue
            if platform and driver.platform != platform and driver.platform != "universal":
                continue
            
            # Text search
            if query:
                query_lower = query.lower()
                if (query_lower in driver.name.lower() or 
                    query_lower in driver.description.lower()):
                    results.append(driver)
            else:
                results.append(driver)
        
        # Sort by rating and install count
        results.sort(key=lambda x: (x.rating, x.install_count), reverse=True)
        return results
    
    def download_driver(self, package_id: str, thor_instance_id: str) -> bool:
        """Download and install driver for THOR instance"""
        if package_id not in self.drivers:
            return False
        
        driver = self.drivers[package_id]
        
        # Simulate download and installation
        logging.info(f"📦 Downloading {driver.name} v{driver.version} for THOR instance {thor_instance_id}")
        
        # Update install count
        driver.install_count += 1
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE drivers SET install_count = ? WHERE package_id = ?
            """, (driver.install_count, package_id))
        
        return True

class ODINCloudOrchestrator:
    """ODIN Cloud Orchestrator - Manages cloud infrastructure"""
    
    def __init__(self, vultr_api_key: Optional[str] = None):
        self.vultr_api_key = vultr_api_key
        self.servers: Dict[str, CloudServer] = {}
        self.cost_tracking: Dict[str, float] = {}
        self.monthly_budget = 300.0  # $300 Vultr credit
        self.cost_alerts_enabled = True
        
    def provision_thor_server(self, name: str, region: str = "ewr", 
                             plan: str = "vc2-1c-1gb") -> Optional[CloudServer]:
        """Provision new THOR server on Vultr"""
        if not self.vultr_api_key:
            logging.error("❌ Vultr API key not configured")
            return None
        
        # Simulate server provisioning
        server_id = f"vultr_{int(time.time())}"
        
        server = CloudServer(
            server_id=server_id,
            provider="vultr",
            name=name,
            region=region,
            size=plan,
            status="active",
            ip_address=f"192.0.2.{len(self.servers) + 1}",  # Example IP
            created=datetime.now(),
            monthly_cost=5.0  # Example cost
        )
        
        self.servers[server_id] = server
        logging.info(f"🚀 Provisioned THOR server: {name} ({server_id})")
        
        return server
    
    def migrate_thor_instance(self, old_server_id: str, new_server_config: dict) -> bool:
        """Migrate THOR instance to new server"""
        if old_server_id not in self.servers:
            return False
        
        old_server = self.servers[old_server_id]
        
        # Provision new server
        new_server = self.provision_thor_server(
            name=f"{old_server.name}_migrated",
            region=new_server_config.get('region', 'ewr'),
            plan=new_server_config.get('plan', 'vc2-1c-1gb')
        )
        
        if not new_server:
            return False
        
        # Simulate migration process
        logging.info(f"🔄 Migrating THOR instance from {old_server_id} to {new_server.server_id}")
        
        # Copy THOR instance ID
        new_server.thor_instance_id = old_server.thor_instance_id
        
        # Mark old server for destruction
        old_server.status = "migrating"
        
        # Schedule old server destruction
        schedule.every(10).minutes.do(self._destroy_server, old_server_id)
        
        return True
    
    def _destroy_server(self, server_id: str):
        """Destroy server and clean up resources"""
        if server_id in self.servers:
            server = self.servers[server_id]
            server.status = "destroyed"
            logging.info(f"💥 Destroyed server: {server_id}")
            
            # Remove from active tracking
            del self.servers[server_id]
    
    def get_cost_report(self) -> dict:
        """Get cost analysis and optimization report"""
        total_monthly_cost = sum(server.monthly_cost for server in self.servers.values() 
                               if server.status == "active")
        
        remaining_budget = self.monthly_budget - total_monthly_cost
        budget_usage_percent = (total_monthly_cost / self.monthly_budget) * 100
        
        return {
            'total_monthly_cost': total_monthly_cost,
            'remaining_budget': remaining_budget,
            'budget_usage_percent': budget_usage_percent,
            'active_servers': len([s for s in self.servers.values() if s.status == "active"]),
            'cost_per_server': total_monthly_cost / max(len(self.servers), 1),
            'projected_3_month_cost': total_monthly_cost * 3,
            'optimization_recommendations': self._get_cost_optimizations()
        }
    
    def _get_cost_optimizations(self) -> List[str]:
        """Get cost optimization recommendations"""
        recommendations = []
        
        total_cost = sum(server.monthly_cost for server in self.servers.values() 
                        if server.status == "active")
        
        if total_cost > self.monthly_budget * 0.8:
            recommendations.append("⚠️ Approaching budget limit - consider downsizing instances")
        
        # Check for underutilized servers
        for server in self.servers.values():
            if server.status == "active" and server.monthly_cost > 20:
                recommendations.append(f"💰 {server.name} might be oversized - consider smaller instance")
        
        if len(self.servers) > 5:
            recommendations.append("🔄 Consider consolidating workloads to reduce server count")
        
        return recommendations

class ODINSecurityManager:
    """ODIN Security Manager - Firewall and threat protection"""
    
    def __init__(self):
        self.firewall_rules: Dict[str, dict] = {}
        self.blocked_ips: Set[str] = set()
        self.security_events: List[SecurityThreat] = []
        self.monitoring_enabled = True
    
    def add_firewall_rule(self, rule_name: str, source_ip: str, port: int, 
                         action: str = "allow", protocol: str = "tcp"):
        """Add firewall rule"""
        rule = {
            'source_ip': source_ip,
            'port': port,
            'action': action,
            'protocol': protocol,
            'created': datetime.now()
        }
        
        self.firewall_rules[rule_name] = rule
        logging.info(f"🔒 Added firewall rule: {rule_name}")
    
    def block_ip(self, ip_address: str, reason: str = "Security threat"):
        """Block IP address"""
        self.blocked_ips.add(ip_address)
        
        threat = SecurityThreat(
            threat_id=hashlib.md5(f"{ip_address}{datetime.now()}".encode()).hexdigest(),
            source_ip=ip_address,
            threat_type="manual_block",
            severity="medium",
            detected=datetime.now(),
            blocked=True,
            details=reason
        )
        
        self.security_events.append(threat)
        logging.warning(f"🚫 Blocked IP: {ip_address} - {reason}")
    
    def get_security_report(self) -> dict:
        """Get security status report"""
        recent_threats = [t for t in self.security_events 
                         if t.detected > datetime.now() - timedelta(hours=24)]
        
        return {
            'firewall_rules_count': len(self.firewall_rules),
            'blocked_ips_count': len(self.blocked_ips),
            'recent_threats_24h': len(recent_threats),
            'monitoring_enabled': self.monitoring_enabled,
            'security_level': self._calculate_security_level(),
            'recommendations': self._get_security_recommendations()
        }
    
    def _calculate_security_level(self) -> str:
        """Calculate overall security level"""
        if len(self.blocked_ips) > 100:
            return "high_threat"
        elif len(self.blocked_ips) > 10:
            return "medium_threat"
        else:
            return "secure"
    
    def _get_security_recommendations(self) -> List[str]:
        """Get security recommendations"""
        recommendations = []
        
        if len(self.firewall_rules) < 5:
            recommendations.append("🔒 Consider adding more specific firewall rules")
        
        if not self.monitoring_enabled:
            recommendations.append("👁️ Enable continuous security monitoring")
        
        recent_blocks = len([ip for ip in self.blocked_ips])
        if recent_blocks > 50:
            recommendations.append("⚠️ High number of blocked IPs - investigate attack patterns")
        
        return recommendations

class ODINSystem:
    """ODIN - The All-Father System"""
    
    def __init__(self, vultr_api_key: Optional[str] = None):
        self.system_info = ODINSystemInfo()
        self.system_info.boot_time = datetime.now()
        
        # Initialize subsystems
        self.watcher = ODINWatcher()
        self.knowledge_base = ODINKnowledgeBase()
        self.driver_manager = ODINDriverManager()
        self.cloud_orchestrator = ODINCloudOrchestrator(vultr_api_key)
        self.security_manager = ODINSecurityManager()
        
        # Setup logging
        self._setup_logging()
        
        # Initialize knowledge base with default entries
        self._init_default_knowledge()
        
        # Initialize default drivers
        self._init_default_drivers()
    
    def _setup_logging(self):
        """Setup ODIN logging system"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - ODIN - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(log_dir / f'odin_{datetime.now().strftime("%Y%m%d")}.log')
            ]
        )
        self.logger = logging.getLogger('odin')
    
    def _init_default_knowledge(self):
        """Initialize knowledge base with default entries"""
        default_entries = [
            {
                'title': 'THOR OS Installation Guide',
                'content': 'Complete guide for installing THOR OS ONE MAN ARMY EDITION...',
                'category': 'installation',
                'tags': ['thor', 'installation', 'setup']
            },
            {
                'title': 'Water Your Tree - Sync Philosophy',
                'content': 'The core philosophy behind THOR sync operations: "The tree never minds, water is water"...',
                'category': 'philosophy',
                'tags': ['sync', 'philosophy', 'collaboration']
            },
            {
                'title': 'P2P Network Troubleshooting',
                'content': 'Common issues and solutions for THOR P2P networking...',
                'category': 'troubleshooting',
                'tags': ['p2p', 'network', 'troubleshooting']
            },
            {
                'title': 'ODIN Cloud Orchestration Best Practices',
                'content': 'Best practices for managing cloud infrastructure with ODIN...',
                'category': 'cloud',
                'tags': ['cloud', 'orchestration', 'best-practices']
            }
        ]
        
        for entry_data in default_entries:
            self.knowledge_base.add_knowledge(**entry_data)
    
    def _init_default_drivers(self):
        """Initialize driver manager with default drivers"""
        default_drivers = [
            {
                'name': 'NVIDIA Gaming Driver',
                'version': '545.92',
                'description': 'Latest NVIDIA gaming driver optimized for THOR OS',
                'download_url': 'https://example.com/nvidia-driver.exe',
                'platform': 'windows',
                'category': 'gpu',
                'size_bytes': 750 * 1024 * 1024  # 750MB
            },
            {
                'name': 'AMD Radeon Driver',
                'version': '23.11.1',
                'description': 'AMD Radeon graphics driver with THOR optimizations',
                'download_url': 'https://example.com/amd-driver.exe',
                'platform': 'windows',
                'category': 'gpu',
                'size_bytes': 650 * 1024 * 1024  # 650MB
            },
            {
                'name': 'THOR Development Kit',
                'version': '2.0.0',
                'description': 'Complete development toolkit for THOR OS applications',
                'download_url': 'https://example.com/thor-dev-kit.tar.gz',
                'platform': 'universal',
                'category': 'development',
                'size_bytes': 200 * 1024 * 1024  # 200MB
            }
        ]
        
        for driver_data in default_drivers:
            self.driver_manager.add_driver(**driver_data)
    
    def print_boot_banner(self):
        """Print ODIN boot banner with ASCII eye"""
        banner = f"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                👁️ ODIN 👁️                                ║
║                         The All-Father Watcher                           ║
║                    System Monitor & Cloud Orchestrator                   ║
║                                                                           ║
║                              ,-.   ,-.                                   ║
║                             /   \\_/   \\                                  ║
║                            |  o     o  |                                 ║
║                             \\    ∩    /                                   ║
║                              '.  ∇  .'                                    ║
║                                '---'                                      ║
║                                                                           ║
║  🎯 Version: {self.system_info.version} "{self.system_info.codename}"                                    ║
║  👁️ Role: {self.system_info.role}                          ║
║                                                                           ║
║  ✅ Watcher: Monitoring {self.system_info.watched_thor_instances} THOR instances                         ║
║  ✅ Knowledge: {self.system_info.knowledge_entries} indexed entries                            ║
║  ✅ Drivers: {self.system_info.managed_drivers} packages managed                             ║
║  ✅ Cloud: {self.system_info.cloud_servers_managed} servers orchestrated                            ║
║  ✅ Security: {self.system_info.security_threats_blocked} threats blocked                             ║
║                                                                           ║
║  🌐 Cloud Infrastructure Management                                      ║
║  📚 Universal Knowledge Base & Search                                    ║
║  🔧 Driver & Library Distribution                                        ║
║  🛡️ Security Monitoring & Threat Protection                              ║
║  💰 Cost Optimization & Resource Management                              ║
║                                                                           ║
║           👁️ The All-Father watches over all THOR instances 👁️            ║
╚═══════════════════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def start_all_services(self):
        """Start all ODIN services"""
        self.logger.info("🚀 Starting ODIN services...")
        
        # Start watcher
        self.watcher.start_watching()
        self.system_info.watching_active = True
        
        # Enable knowledge indexing
        self.system_info.knowledge_indexing_active = True
        
        # Enable cloud orchestration
        self.system_info.cloud_orchestration_active = True
        
        # Update system info
        self.system_info.knowledge_entries = len(self.knowledge_base.entries)
        self.system_info.managed_drivers = len(self.driver_manager.drivers)
        self.system_info.cloud_servers_managed = len(self.cloud_orchestrator.servers)
        
        self.logger.info("✅ All ODIN services started successfully")
    
    def get_comprehensive_status(self) -> dict:
        """Get comprehensive ODIN status"""
        boot_time_str = self.system_info.boot_time.strftime("%Y-%m-%d %H:%M:%S") if self.system_info.boot_time else "Unknown"
        uptime_str = str(datetime.now() - self.system_info.boot_time) if self.system_info.boot_time else "Unknown"
        
        health_report = self.watcher.get_health_report()
        cost_report = self.cloud_orchestrator.get_cost_report()
        security_report = self.security_manager.get_security_report()
        
        return {
            'system_info': {
                'version': self.system_info.version,
                'codename': self.system_info.codename,
                'boot_time': boot_time_str,
                'uptime': uptime_str
            },
            'health_monitoring': health_report,
            'cost_management': cost_report,
            'security_status': security_report,
            'knowledge_base': {
                'total_entries': len(self.knowledge_base.entries),
                'categories': len(self.knowledge_base.get_categories()),
                'popular_entries': len(self.knowledge_base.get_popular_entries())
            },
            'driver_management': {
                'total_drivers': len(self.driver_manager.drivers),
                'platforms_supported': len(set(d.platform for d in self.driver_manager.drivers.values())),
                'categories': len(set(d.category for d in self.driver_manager.drivers.values()))
            }
        }
    
    def interactive_menu(self):
        """Interactive ODIN menu"""
        while True:
            print("\n" + "="*70)
            print("👁️ ODIN - The All-Father Interactive Menu")
            print("="*70)
            print("1. 📊 System Status Dashboard")
            print("2. 👁️ THOR Instance Monitoring")
            print("3. 📚 Knowledge Base Search")
            print("4. 🔧 Driver Management")
            print("5. ☁️ Cloud Orchestration")
            print("6. 🛡️ Security Management")
            print("7. 💰 Cost Analysis")
            print("8. 🔍 Search Everything")
            print("9. 📈 Generate Reports")
            print("10. ⚙️ System Configuration")
            print("11. 🛑 Exit")
            print()
            
            choice = input("Select option (1-11): ").strip()
            
            if choice == "1":
                status = self.get_comprehensive_status()
                print(f"""
👁️ ODIN System Status Dashboard
==============================

🖥️  System Information:
   • Version: {status['system_info']['version']}
   • Boot Time: {status['system_info']['boot_time']}
   • Uptime: {status['system_info']['uptime']}

👁️ Health Monitoring:
   • THOR Instances: {status['health_monitoring']['instances_monitored']}
   • Healthy: {status['health_monitoring']['healthy_instances']}
   • System Health: {status['health_monitoring']['system_health']}

📚 Knowledge Base:
   • Total Entries: {status['knowledge_base']['total_entries']}
   • Categories: {status['knowledge_base']['categories']}

🔧 Driver Management:
   • Total Drivers: {status['driver_management']['total_drivers']}
   • Platforms: {status['driver_management']['platforms_supported']}

☁️ Cloud Management:
   • Monthly Cost: ${status['cost_management']['total_monthly_cost']:.2f}
   • Budget Usage: {status['cost_management']['budget_usage_percent']:.1f}%
   • Active Servers: {status['cost_management']['active_servers']}

🛡️ Security:
   • Firewall Rules: {status['security_status']['firewall_rules_count']}
   • Blocked IPs: {status['security_status']['blocked_ips_count']}
   • Security Level: {status['security_status']['security_level']}
                """)
                
            elif choice == "2":
                health_report = self.watcher.get_health_report()
                print(f"""
👁️ THOR Instance Monitoring
==========================

📊 Overview:
   • Instances Monitored: {health_report['instances_monitored']}
   • Healthy Instances: {health_report['healthy_instances']}
   • Unhealthy Instances: {health_report['unhealthy_instances']}
   • Security Threats: {health_report['security_threats_detected']}
   • Blocked IPs: {health_report['blocked_ips']}

🎯 Instance Details:
                """)
                
                for instance_id, instance in self.watcher.watched_instances.items():
                    status_icon = "✅" if instance.health_status == "healthy" else "❌"
                    print(f"   {status_icon} {instance.name} ({instance_id})")
                    print(f"      Address: {instance.address}:{instance.port}")
                    print(f"      Status: {instance.health_status}")
                    print(f"      Last Seen: {instance.last_seen.strftime('%Y-%m-%d %H:%M:%S')}")
                    print()
                
            elif choice == "3":
                query = input("Enter search query: ").strip()
                if query:
                    results = self.knowledge_base.search_knowledge(query)
                    print(f"\n📚 Knowledge Search Results ({len(results)} found):")
                    for i, entry in enumerate(results[:5], 1):
                        print(f"{i}. {entry.title}")
                        print(f"   Category: {entry.category}")
                        print(f"   Relevance: {entry.relevance_score:.1f}")
                        print(f"   {entry.content[:100]}...")
                        print()
                
            elif choice == "4":
                print("\n🔧 Driver Management")
                print("1. Search Drivers")
                print("2. List All Drivers")
                print("3. Driver Categories")
                
                sub_choice = input("Select option: ").strip()
                
                if sub_choice == "1":
                    search_query = input("Enter driver search query: ").strip()
                    results = self.driver_manager.search_drivers(search_query)
                    print(f"\n📦 Driver Search Results ({len(results)} found):")
                    for driver in results[:5]:
                        print(f"• {driver.name} v{driver.version}")
                        print(f"  Platform: {driver.platform} | Category: {driver.category}")
                        print(f"  Size: {driver.size_bytes / (1024*1024):.1f}MB | Installs: {driver.install_count}")
                        print()
                
                elif sub_choice == "2":
                    drivers = list(self.driver_manager.drivers.values())
                    print(f"\n📦 All Drivers ({len(drivers)} total):")
                    for driver in drivers:
                        print(f"• {driver.name} v{driver.version} ({driver.platform})")
                
            elif choice == "5":
                cost_report = self.cloud_orchestrator.get_cost_report()
                print(f"""
☁️ Cloud Orchestration Dashboard
===============================

💰 Cost Analysis:
   • Total Monthly Cost: ${cost_report['total_monthly_cost']:.2f}
   • Remaining Budget: ${cost_report['remaining_budget']:.2f}
   • Budget Usage: {cost_report['budget_usage_percent']:.1f}%
   • Active Servers: {cost_report['active_servers']}
   • Cost per Server: ${cost_report['cost_per_server']:.2f}

📈 Projections:
   • 3-Month Projected Cost: ${cost_report['projected_3_month_cost']:.2f}

🎯 Optimization Recommendations:
                """)
                
                for rec in cost_report['optimization_recommendations']:
                    print(f"   {rec}")
                
            elif choice == "6":
                security_report = self.security_manager.get_security_report()
                print(f"""
🛡️ Security Management Dashboard
==============================

🔒 Current Status:
   • Firewall Rules: {security_report['firewall_rules_count']}
   • Blocked IPs: {security_report['blocked_ips_count']}
   • Recent Threats (24h): {security_report['recent_threats_24h']}
   • Security Level: {security_report['security_level']}
   • Monitoring: {'🟢 Active' if security_report['monitoring_enabled'] else '🔴 Inactive'}

🎯 Recommendations:
                """)
                
                for rec in security_report['recommendations']:
                    print(f"   {rec}")
                
            elif choice == "8":
                query = input("🔍 Search everything (knowledge, drivers, etc.): ").strip()
                if query:
                    print(f"\n🔍 Universal Search Results for '{query}':")
                    
                    # Search knowledge
                    kb_results = self.knowledge_base.search_knowledge(query)
                    if kb_results:
                        print(f"\n📚 Knowledge ({len(kb_results)} results):")
                        for entry in kb_results[:3]:
                            print(f"   • {entry.title}")
                    
                    # Search drivers
                    driver_results = self.driver_manager.search_drivers(query)
                    if driver_results:
                        print(f"\n🔧 Drivers ({len(driver_results)} results):")
                        for driver in driver_results[:3]:
                            print(f"   • {driver.name} v{driver.version}")
                
            elif choice == "11":
                print("👁️ ODIN shutting down gracefully...")
                print("🌳 The All-Father continues to watch from the digital realm")
                break
            else:
                print("❌ Invalid choice. Please select 1-11.")
            
            input("\nPress Enter to continue...")

def main():
    """Main entry point for ODIN"""
    # Get Vultr API key from environment or user input
    vultr_api_key = os.getenv('VULTR_API_KEY')
    if not vultr_api_key:
        print("💡 Tip: Set VULTR_API_KEY environment variable for cloud orchestration")
    
    # Initialize ODIN
    odin = ODINSystem(vultr_api_key)
    
    # Print boot banner
    odin.print_boot_banner()
    
    # Start all services
    odin.start_all_services()
    
    # Run interactive menu
    try:
        odin.interactive_menu()
    except KeyboardInterrupt:
        print("\n\n🛑 ODIN interrupted by user")
    finally:
        # Cleanup
        odin.watcher.stop_watching()
        print("👁️ ODIN shutdown complete. The All-Father's watch continues...")

if __name__ == "__main__":
    main()
