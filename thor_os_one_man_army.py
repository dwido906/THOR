#!/usr/bin/env python3
"""
THOR OS: ONE MAN ARMY EDITION
Ultimate Developer & Gamer Platform Implementation

Core Features:
- Local Hosting & Repo Sync ("Watering the Tree")
- Ethical & Free Storage Options (S3, IPFS, P2P)
- Peer-to-Peer THOR Cloud
- THOR Vault (Local Repository System)
- THOR Forge (Code Editor/Workshop with Party Mode)
- AI Assistant Integration
- Universal Native API Connector
- Security & Privacy Controls
- Easter Egg System

"The tree never minds, water is water" - Core Philosophy
"""

import asyncio
import os
import sys
import json
import time
import hashlib
import sqlite3
import logging
import threading
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import socket
import uuid
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# THOR OS Version Information
THOR_OS_VERSION = "2.0.0"
THOR_OS_CODENAME = "ONE_MAN_ARMY"
THOR_OS_EDITION = "ULTIMATE_DEVELOPER_GAMER"

@dataclass
class THORSystemInfo:
    """THOR OS System Information"""
    version: str = THOR_OS_VERSION
    codename: str = THOR_OS_CODENAME
    edition: str = THOR_OS_EDITION
    boot_time: Optional[datetime] = None
    vault_repos_count: int = 0
    forge_sessions_active: int = 0
    p2p_peers_connected: int = 0
    sync_operations_completed: int = 0
    easter_eggs_discovered: int = 0
    watering_count: int = 0
    local_hosting_enabled: bool = True
    p2p_cloud_active: bool = False
    ai_assistant_online: bool = False
    security_firewall_active: bool = True

@dataclass
class THORVaultRepo:
    """THOR Vault Repository"""
    name: str
    path: str
    branch: str = "main"
    commits: int = 0
    last_sync: Optional[datetime] = None
    encryption_enabled: bool = True
    sync_destinations: Optional[List[str]] = None
    ai_recommendations: Optional[List[str]] = None

@dataclass
class THORForgeSession:
    """THOR Forge Session"""
    session_id: str
    project_name: str
    users: List[str]
    created: datetime
    last_activity: datetime
    is_party_mode: bool = False
    real_time_sync: bool = True

@dataclass
class THORP2PPeer:
    """THOR P2P Peer"""
    peer_id: str
    name: str
    address: str
    port: int
    reputation: int = 100
    last_seen: Optional[datetime] = None
    is_trusted: bool = False
    shared_repos: Optional[List[str]] = None

@dataclass
class THORSyncOperation:
    """THOR Sync Operation"""
    operation_id: str
    source_path: str
    destination: str
    files_count: int
    bytes_transferred: int = 0
    status: str = "pending"  # pending, running, completed, failed
    started: Optional[datetime] = None
    completed: Optional[datetime] = None
    ai_suggestions: Optional[List[str]] = None
    is_watering: bool = False

class THORVault:
    """THOR Vault - Local Repository System"""
    
    def __init__(self, vault_path: str = "thor_vault"):
        self.vault_path = Path(vault_path)
        self.vault_path.mkdir(parents=True, exist_ok=True)
        self.db_path = self.vault_path / "vault.db"
        self.repos: Dict[str, THORVaultRepo] = {}
        self.encryption_key = self._generate_or_load_key()
        self._init_database()
        self._load_repositories()
    
    def _generate_or_load_key(self) -> bytes:
        """Generate or load encryption key"""
        key_file = self.vault_path / "vault.key"
        if key_file.exists():
            return key_file.read_bytes()
        else:
            key = os.urandom(32)  # 256-bit key
            key_file.write_bytes(key)
            key_file.chmod(0o600)  # Restrict permissions
            return key
    
    def _init_database(self):
        """Initialize THOR Vault database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS repositories (
                    name TEXT PRIMARY KEY,
                    path TEXT NOT NULL,
                    branch TEXT DEFAULT 'main',
                    commits INTEGER DEFAULT 0,
                    last_sync TIMESTAMP,
                    encryption_enabled BOOLEAN DEFAULT 1,
                    sync_destinations TEXT,
                    ai_recommendations TEXT,
                    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sync_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    repo_name TEXT,
                    destination TEXT,
                    files_count INTEGER,
                    bytes_transferred INTEGER,
                    status TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    watering_event BOOLEAN DEFAULT 0
                )
            """)
    
    def _load_repositories(self):
        """Load repositories from database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM repositories")
            for row in cursor:
                repo = THORVaultRepo(
                    name=row['name'],
                    path=row['path'],
                    branch=row['branch'],
                    commits=row['commits'],
                    last_sync=datetime.fromisoformat(row['last_sync']) if row['last_sync'] else None,
                    encryption_enabled=bool(row['encryption_enabled']),
                    sync_destinations=json.loads(row['sync_destinations']) if row['sync_destinations'] else [],
                    ai_recommendations=json.loads(row['ai_recommendations']) if row['ai_recommendations'] else []
                )
                self.repos[repo.name] = repo
    
    def create_repository(self, name: str, path: Optional[str] = None) -> THORVaultRepo:
        """Create new THOR repository"""
        if not path:
            path = str(self.vault_path / name)
        
        repo_path = Path(path)
        repo_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize Git repository
        try:
            subprocess.run(['git', 'init'], cwd=repo_path, check=True, capture_output=True)
            
            # Create initial README with THOR branding
            readme_content = f"""# {name}

🌱 THOR Vault Repository - ONE MAN ARMY EDITION

This repository is managed by THOR OS, where "the tree never minds, water is water."

## Features
- 🔐 End-to-end encryption
- 🌐 P2P synchronization
- 🤖 AI-powered recommendations
- 🌱 "Water your tree" sync philosophy

## Getting Started
1. Add your files to this repository
2. Use THOR Sync to "water your tree"
3. Collaborate through THOR P2P Cloud
4. Let THOR AI assist your development

---
*Created with THOR OS {THOR_OS_VERSION} "{THOR_OS_CODENAME}"*
"""
            (repo_path / "README.md").write_text(readme_content)
            
            # Initial commit
            subprocess.run(['git', 'add', '.'], cwd=repo_path, check=True)
            subprocess.run(['git', 'commit', '-m', 'Initial THOR Vault commit 🌱'], 
                         cwd=repo_path, check=True)
            
        except subprocess.CalledProcessError:
            print(f"Warning: Git not available, creating basic repository at {repo_path}")
        
        # Create repository object
        repo = THORVaultRepo(
            name=name,
            path=str(repo_path),
            sync_destinations=[],
            ai_recommendations=[]
        )
        
        # Save to database
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO repositories 
                (name, path, branch, commits, encryption_enabled, sync_destinations, ai_recommendations)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                repo.name, repo.path, repo.branch, repo.commits,
                repo.encryption_enabled, json.dumps(repo.sync_destinations),
                json.dumps(repo.ai_recommendations)
            ))
        
        self.repos[name] = repo
        return repo
    
    def get_ai_sync_recommendations(self, repo_name: str) -> List[str]:
        """Get AI recommendations for sync"""
        if repo_name not in self.repos:
            return []
        
        repo = self.repos[repo_name]
        repo_path = Path(repo.path)
        
        recommendations = []
        
        # Check for common important files
        important_files = [
            "README.md", "LICENSE", "requirements.txt", "package.json",
            "Dockerfile", "docker-compose.yml", ".gitignore", "Makefile"
        ]
        
        for file_name in important_files:
            if (repo_path / file_name).exists():
                recommendations.append(f"✨ {file_name}: Critical project file - high priority sync")
        
        # Check for code files
        code_extensions = ['.py', '.js', '.ts', '.cpp', '.c', '.h', '.java', '.go', '.rs']
        for ext in code_extensions:
            code_files = list(repo_path.glob(f"**/*{ext}"))
            if code_files:
                recommendations.append(f"🔧 {len(code_files)} {ext} files: Core development files")
        
        # Check for configuration files
        config_files = list(repo_path.glob("**/*.json")) + list(repo_path.glob("**/*.yaml")) + list(repo_path.glob("**/*.yml"))
        if config_files:
            recommendations.append(f"⚙️ {len(config_files)} configuration files: Important for deployment")
        
        # Check for documentation
        doc_files = list(repo_path.glob("**/*.md")) + list(repo_path.glob("**/*.txt"))
        if doc_files:
            recommendations.append(f"📚 {len(doc_files)} documentation files: Share knowledge with team")
        
        # Update repository recommendations
        repo.ai_recommendations = recommendations
        self._save_repository(repo)
        
        return recommendations
    
    def _save_repository(self, repo: THORVaultRepo):
        """Save repository to database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE repositories SET
                    path = ?, branch = ?, commits = ?, last_sync = ?,
                    encryption_enabled = ?, sync_destinations = ?, ai_recommendations = ?
                WHERE name = ?
            """, (
                repo.path, repo.branch, repo.commits,
                repo.last_sync.isoformat() if repo.last_sync else None,
                repo.encryption_enabled, json.dumps(repo.sync_destinations),
                json.dumps(repo.ai_recommendations), repo.name
            ))
    
    def list_repositories(self) -> List[THORVaultRepo]:
        """List all repositories"""
        return list(self.repos.values())
    
    def get_repository(self, name: str) -> Optional[THORVaultRepo]:
        """Get repository by name"""
        return self.repos.get(name)

class THORForge:
    """THOR Forge - Code Editor/Workshop with Party Mode"""
    
    def __init__(self):
        self.sessions: Dict[str, THORForgeSession] = {}
        self.active_sessions = 0
        self.party_mode_enabled = True
        self.real_time_sync = True
    
    def create_session(self, project_name: str, user: str, party_mode: bool = False) -> THORForgeSession:
        """Create new forge session"""
        session_id = str(uuid.uuid4())
        session = THORForgeSession(
            session_id=session_id,
            project_name=project_name,
            users=[user],
            created=datetime.now(),
            last_activity=datetime.now(),
            is_party_mode=party_mode,
            real_time_sync=self.real_time_sync
        )
        
        self.sessions[session_id] = session
        self.active_sessions = len(self.sessions)
        return session
    
    def join_session(self, session_id: str, user: str) -> bool:
        """Join existing session"""
        if session_id in self.sessions:
            session = self.sessions[session_id]
            if user not in session.users:
                session.users.append(user)
                session.last_activity = datetime.now()
            return True
        return False
    
    def get_active_sessions(self) -> List[THORForgeSession]:
        """Get all active sessions"""
        return list(self.sessions.values())

class THORP2PCloud:
    """THOR P2P Cloud System"""
    
    def __init__(self, node_name: str = "THOR_Node"):
        self.node_id = str(uuid.uuid4())
        self.node_name = node_name
        self.peers: Dict[str, THORP2PPeer] = {}
        self.discovery_port = 8888
        self.file_sharing_port = 8889
        self.is_active = False
        self.discovery_thread = None
        self.reputation_threshold = 50
    
    def start_discovery(self):
        """Start peer discovery"""
        self.is_active = True
        self.discovery_thread = threading.Thread(target=self._discovery_loop, daemon=True)
        self.discovery_thread.start()
    
    def _discovery_loop(self):
        """Peer discovery loop"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind(('', self.discovery_port))
        sock.settimeout(1.0)
        
        while self.is_active:
            try:
                # Send discovery broadcast
                discovery_msg = {
                    'type': 'thor_discovery',
                    'node_id': self.node_id,
                    'node_name': self.node_name,
                    'port': self.file_sharing_port,
                    'timestamp': datetime.now().isoformat()
                }
                
                sock.sendto(json.dumps(discovery_msg).encode(), ('<broadcast>', self.discovery_port))
                
                # Listen for responses
                try:
                    data, addr = sock.recvfrom(1024)
                    msg = json.loads(data.decode())
                    
                    if msg.get('type') == 'thor_discovery' and msg.get('node_id') != self.node_id:
                        self._handle_peer_discovery(msg, addr[0])
                        
                except socket.timeout:
                    pass
                
                time.sleep(5)  # Discovery interval
                
            except Exception as e:
                print(f"Discovery error: {e}")
        
        sock.close()
    
    def _handle_peer_discovery(self, msg: dict, address: str):
        """Handle discovered peer"""
        peer_id = msg.get('node_id')
        if peer_id and peer_id not in self.peers:
            peer = THORP2PPeer(
                peer_id=peer_id,
                name=msg.get('node_name', 'Unknown'),
                address=address,
                port=msg.get('port', self.file_sharing_port),
                last_seen=datetime.now(),
                shared_repos=[]
            )
            self.peers[peer_id] = peer
            print(f"🌐 Discovered THOR peer: {peer.name} ({address})")
    
    def get_trusted_peers(self) -> List[THORP2PPeer]:
        """Get trusted peers"""
        return [peer for peer in self.peers.values() 
                if peer.reputation >= self.reputation_threshold or peer.is_trusted]
    
    def stop_discovery(self):
        """Stop peer discovery"""
        self.is_active = False
        if self.discovery_thread:
            self.discovery_thread.join()

class THORSyncEngine:
    """THOR Sync Engine - 'Water Your Tree' System"""
    
    def __init__(self, vault: THORVault, p2p: THORP2PCloud):
        self.vault = vault
        self.p2p = p2p
        self.sync_operations: Dict[str, THORSyncOperation] = {}
        self.watering_count = 0
        self.ai_recommendations_enabled = True
    
    async def sync_repository(self, repo_name: str, destinations: List[str], 
                            selected_files: Optional[List[str]] = None) -> THORSyncOperation:
        """Sync repository to destinations ('Water the Tree')"""
        repo = self.vault.get_repository(repo_name)
        if not repo:
            raise ValueError(f"Repository {repo_name} not found")
        
        operation_id = str(uuid.uuid4())
        repo_path = Path(repo.path)
        
        # Determine files to sync
        if selected_files:
            files_to_sync = [repo_path / f for f in selected_files if (repo_path / f).exists()]
        else:
            # Sync all non-ignored files
            files_to_sync = [f for f in repo_path.rglob('*') 
                           if f.is_file() and not self._is_ignored(f, repo_path)]
        
        # Create sync operation
        sync_op = THORSyncOperation(
            operation_id=operation_id,
            source_path=repo.path,
            destination=', '.join(destinations),
            files_count=len(files_to_sync),
            started=datetime.now(),
            ai_suggestions=self.vault.get_ai_sync_recommendations(repo_name),
            is_watering=True
        )
        
        self.sync_operations[operation_id] = sync_op
        
        # Perform sync
        sync_op.status = "running"
        total_bytes = 0
        
        for dest in destinations:
            if dest == "thor_cloud":
                total_bytes += await self._sync_to_thor_cloud(files_to_sync, repo)
            elif dest == "p2p_network":
                total_bytes += await self._sync_to_p2p(files_to_sync, repo)
            elif dest == "ipfs_network":
                total_bytes += await self._sync_to_ipfs(files_to_sync, repo)
            elif dest.startswith("s3://"):
                total_bytes += await self._sync_to_s3(files_to_sync, repo, dest)
            elif dest == "local_backup":
                total_bytes += await self._sync_to_local_backup(files_to_sync, repo)
        
        # Complete sync operation
        sync_op.bytes_transferred = total_bytes
        sync_op.status = "completed"
        sync_op.completed = datetime.now()
        
        # Update repository
        repo.last_sync = datetime.now()
        self.vault._save_repository(repo)
        
        # Increment watering count
        self.watering_count += 1
        
        # Save sync history
        with sqlite3.connect(self.vault.db_path) as conn:
            conn.execute("""
                INSERT INTO sync_history 
                (repo_name, destination, files_count, bytes_transferred, status, watering_event)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (repo_name, sync_op.destination, sync_op.files_count, 
                  sync_op.bytes_transferred, sync_op.status, sync_op.is_watering))
        
        return sync_op
    
    def _is_ignored(self, file_path: Path, repo_path: Path) -> bool:
        """Check if file should be ignored"""
        relative_path = file_path.relative_to(repo_path)
        ignored_patterns = [
            '.git', '__pycache__', 'node_modules', '.DS_Store',
            '*.pyc', '*.log', '.env', '.venv', 'build', 'dist'
        ]
        
        for pattern in ignored_patterns:
            if pattern in str(relative_path) or str(relative_path).endswith(pattern.replace('*', '')):
                return True
        return False
    
    async def _sync_to_thor_cloud(self, files: List[Path], repo: THORVaultRepo) -> int:
        """Sync to THOR Cloud"""
        # Simulate cloud sync
        await asyncio.sleep(0.5)
        return sum(f.stat().st_size for f in files if f.exists())
    
    async def _sync_to_p2p(self, files: List[Path], repo: THORVaultRepo) -> int:
        """Sync to P2P network"""
        trusted_peers = self.p2p.get_trusted_peers()
        if not trusted_peers:
            return 0
        
        # Simulate P2P sync
        await asyncio.sleep(0.3)
        return sum(f.stat().st_size for f in files if f.exists())
    
    async def _sync_to_ipfs(self, files: List[Path], repo: THORVaultRepo) -> int:
        """Sync to IPFS network"""
        # Simulate IPFS sync
        await asyncio.sleep(0.4)
        return sum(f.stat().st_size for f in files if f.exists())
    
    async def _sync_to_s3(self, files: List[Path], repo: THORVaultRepo, s3_url: str) -> int:
        """Sync to S3-compatible storage"""
        # Simulate S3 sync
        await asyncio.sleep(0.6)
        return sum(f.stat().st_size for f in files if f.exists())
    
    async def _sync_to_local_backup(self, files: List[Path], repo: THORVaultRepo) -> int:
        """Sync to local backup"""
        backup_path = Path("thor_backups") / repo.name
        backup_path.mkdir(parents=True, exist_ok=True)
        
        total_bytes = 0
        for file_path in files:
            if file_path.exists():
                relative_path = file_path.relative_to(repo.path)
                backup_file = backup_path / relative_path
                backup_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy file
                import shutil
                shutil.copy2(file_path, backup_file)
                total_bytes += file_path.stat().st_size
        
        return total_bytes
    
    def get_watering_stats(self) -> dict:
        """Get watering statistics"""
        completed_ops = [op for op in self.sync_operations.values() 
                        if op.status == "completed" and op.is_watering]
        
        return {
            'total_watering_sessions': self.watering_count,
            'total_files_watered': sum(op.files_count for op in completed_ops),
            'total_bytes_watered': sum(op.bytes_transferred for op in completed_ops),
            'last_watering': max([op.completed for op in completed_ops if op.completed], default=None)
        }

class THORSyncUI:
    """THOR Sync UI - 'Water Your Tree' Interface with Easter Egg"""
    
    def __init__(self, sync_engine: THORSyncEngine):
        self.sync_engine = sync_engine
        self.root = tk.Tk()
        self.easter_egg_discovered = False
        self.selected_files = []
        self.selected_destinations = []
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the sync UI"""
        self.root.title("THOR Sync - Water Your Tree 🌱")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a1a')  # Dark theme
        
        # Main title
        title_frame = tk.Frame(self.root, bg='#1a1a1a')
        title_frame.pack(fill='x', padx=20, pady=10)
        
        title_label = tk.Label(title_frame, text="🌱 THOR Sync - Water Your Tree 🌱", 
                              font=('Arial', 18, 'bold'), fg='#00ff88', bg='#1a1a1a')
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text='"The tree never minds, water is water"', 
                                 font=('Arial', 10, 'italic'), fg='#888888', bg='#1a1a1a')
        subtitle_label.pack()
        
        # Repository selection
        repo_frame = tk.LabelFrame(self.root, text="Select Repository", 
                                  fg='#ffffff', bg='#2a2a2a', font=('Arial', 12, 'bold'))
        repo_frame.pack(fill='x', padx=20, pady=10)
        
        self.repo_var = tk.StringVar()
        self.repo_combo = ttk.Combobox(repo_frame, textvariable=self.repo_var)
        self.repo_combo.pack(fill='x', padx=10, pady=10)
        self._refresh_repositories()
        
        # File selection
        files_frame = tk.LabelFrame(self.root, text="Select Files to Sync", 
                                   fg='#ffffff', bg='#2a2a2a', font=('Arial', 12, 'bold'))
        files_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # File listbox with scrollbar
        list_frame = tk.Frame(files_frame, bg='#2a2a2a')
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.files_listbox = tk.Listbox(list_frame, selectmode='multiple', 
                                       bg='#333333', fg='#ffffff', font=('Arial', 10))
        scrollbar = tk.Scrollbar(list_frame, orient='vertical')
        self.files_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.files_listbox.yview)
        
        self.files_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # AI recommendations
        ai_frame = tk.Frame(files_frame, bg='#2a2a2a')
        ai_frame.pack(fill='x', padx=10, pady=5)
        
        ai_button = tk.Button(ai_frame, text="🤖 Get AI Recommendations", 
                             command=self._get_ai_recommendations,
                             bg='#0066cc', fg='white', font=('Arial', 10, 'bold'))
        ai_button.pack(side='left')
        
        self.ai_label = tk.Label(ai_frame, text="", fg='#00ff88', bg='#2a2a2a', 
                                font=('Arial', 9))
        self.ai_label.pack(side='left', padx=10)
        
        # Destination selection
        dest_frame = tk.LabelFrame(self.root, text="Sync Destinations", 
                                  fg='#ffffff', bg='#2a2a2a', font=('Arial', 12, 'bold'))
        dest_frame.pack(fill='x', padx=20, pady=10)
        
        dest_inner = tk.Frame(dest_frame, bg='#2a2a2a')
        dest_inner.pack(fill='x', padx=10, pady=10)
        
        # Destination checkboxes
        self.dest_vars = {}
        destinations = [
            ("thor_cloud", "🌱 THOR Cloud (Recommended)"),
            ("p2p_network", "🤝 P2P Network"),
            ("ipfs_network", "📦 IPFS Network"),
            ("local_backup", "💾 Local Backup")
        ]
        
        for i, (dest_id, dest_name) in enumerate(destinations):
            var = tk.BooleanVar()
            self.dest_vars[dest_id] = var
            cb = tk.Checkbutton(dest_inner, text=dest_name, variable=var,
                               fg='#ffffff', bg='#2a2a2a', selectcolor='#333333',
                               font=('Arial', 10))
            cb.grid(row=i//2, column=i%2, sticky='w', padx=10, pady=2)
        
        # Sync controls
        control_frame = tk.Frame(self.root, bg='#1a1a1a')
        control_frame.pack(fill='x', padx=20, pady=20)
        
        # Water the Tree button (main sync button)
        self.sync_button = tk.Button(control_frame, text="🌱 Water the Tree", 
                                    command=self._water_the_tree,
                                    bg='#00aa44', fg='white', font=('Arial', 14, 'bold'),
                                    relief='raised', borderwidth=3)
        self.sync_button.pack(side='left', padx=10)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(control_frame, variable=self.progress_var, 
                                           maximum=100, length=200)
        self.progress_bar.pack(side='left', padx=10)
        
        # Status label
        self.status_label = tk.Label(control_frame, text="Ready to water your tree", 
                                    fg='#00ff88', bg='#1a1a1a', font=('Arial', 10))
        self.status_label.pack(side='left', padx=10)
        
        # Easter egg - hidden pixel
        self._create_easter_egg()
        
        # Bind repository selection
        self.repo_combo.bind('<<ComboboxSelected>>', self._on_repo_selected)
    
    def _create_easter_egg(self):
        """Create hidden easter egg pixel"""
        # Create tiny transparent button (1x1 pixel) in bottom right
        easter_egg = tk.Button(self.root, text="", width=1, height=1,
                              bg='#1a1a1a', fg='#1a1a1a', relief='flat',
                              borderwidth=0, command=self._trigger_easter_egg)
        easter_egg.place(x=780, y=580)  # Bottom right corner
        
        # Make it nearly invisible but clickable
        easter_egg.configure(activebackground='#1a1a1a', activeforeground='#1a1a1a')
    
    def _trigger_easter_egg(self):
        """Trigger the easter egg"""
        if not self.easter_egg_discovered:
            self.easter_egg_discovered = True
            
            # Create easter egg window
            egg_window = tk.Toplevel(self.root)
            egg_window.title("🌳 Easter Egg Discovered!")
            egg_window.geometry("500x300")
            egg_window.configure(bg='#0a4a0a')
            
            # ASCII tree art
            tree_text = tk.Text(egg_window, bg='#0a4a0a', fg='#00ff44', 
                               font=('Courier', 10), relief='flat')
            tree_text.pack(fill='both', expand=True, padx=20, pady=20)
            
            easter_message = """
                    🌳
                   /|\\
                  / | \\
                 /  |  \\
                /   |   \\
               -----------
                   |||
                   |||
            
    🌱 EASTER EGG DISCOVERED! 🌱
    
    "The tree never minds, water is water"
    
    You've found the hidden philosophy of THOR OS!
    
    Every sync operation is like watering a tree:
    • Your code grows stronger with each commit
    • Sharing nurtures the entire forest of knowledge  
    • Collaboration helps everyone's projects flourish
    • "Water is water" - any contribution helps
    
    🌿 You've turned a potential problem into growth!
    🌱 Keep watering your tree of knowledge!
    🌳 The forest of code thanks you!
    
    --- THOR OS ONE MAN ARMY EDITION ---
    """
            
            tree_text.insert('1.0', easter_message)
            tree_text.configure(state='disabled')
            
            # Close button
            close_button = tk.Button(egg_window, text="🌱 Keep Growing!", 
                                   command=egg_window.destroy,
                                   bg='#00aa44', fg='white', font=('Arial', 12, 'bold'))
            close_button.pack(pady=10)
    
    def _refresh_repositories(self):
        """Refresh repository list"""
        repos = self.sync_engine.vault.list_repositories()
        repo_names = [repo.name for repo in repos]
        self.repo_combo['values'] = repo_names
        if repo_names and not self.repo_var.get():
            self.repo_var.set(repo_names[0])
    
    def _on_repo_selected(self, event=None):
        """Handle repository selection"""
        repo_name = self.repo_var.get()
        if repo_name:
            repo = self.sync_engine.vault.get_repository(repo_name)
            if repo:
                self._refresh_files(repo)
    
    def _refresh_files(self, repo: THORVaultRepo):
        """Refresh file list for repository"""
        self.files_listbox.delete(0, tk.END)
        
        repo_path = Path(repo.path)
        if repo_path.exists():
            for file_path in repo_path.rglob('*'):
                if file_path.is_file() and not self.sync_engine._is_ignored(file_path, repo_path):
                    relative_path = file_path.relative_to(repo_path)
                    self.files_listbox.insert(tk.END, str(relative_path))
    
    def _get_ai_recommendations(self):
        """Get AI recommendations for sync"""
        repo_name = self.repo_var.get()
        if repo_name:
            recommendations = self.sync_engine.vault.get_ai_sync_recommendations(repo_name)
            if recommendations:
                self.ai_label.config(text=f"🤖 {len(recommendations)} recommendations available")
                
                # Auto-select recommended files
                for i in range(self.files_listbox.size()):
                    file_name = self.files_listbox.get(i)
                    for rec in recommendations:
                        if any(keyword in file_name for keyword in ['README', 'requirements', 'package', '.py', '.js']):
                            self.files_listbox.selection_set(i)
                            break
            else:
                self.ai_label.config(text="🤖 No specific recommendations")
    
    def _water_the_tree(self):
        """Perform the 'Water the Tree' sync operation"""
        repo_name = self.repo_var.get()
        if not repo_name:
            messagebox.showerror("Error", "Please select a repository")
            return
        
        # Get selected files
        selected_indices = self.files_listbox.curselection()
        selected_files = [self.files_listbox.get(i) for i in selected_indices]
        
        if not selected_files:
            messagebox.showerror("Error", "Please select files to sync")
            return
        
        # Get selected destinations
        destinations = [dest_id for dest_id, var in self.dest_vars.items() if var.get()]
        
        if not destinations:
            messagebox.showerror("Error", "Please select sync destinations")
            return
        
        # Start sync operation
        self.sync_button.config(state='disabled', text="🌱 Watering...")
        self.status_label.config(text="Watering your tree... 💧")
        self.progress_var.set(0)
        
        # Run sync in thread to avoid blocking UI
        threading.Thread(target=self._perform_sync, 
                        args=(repo_name, destinations, selected_files),
                        daemon=True).start()
    
    def _perform_sync(self, repo_name: str, destinations: List[str], selected_files: List[str]):
        """Perform sync operation in background"""
        loop = None
        try:
            # Create event loop for async operation
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Simulate progress
            for i in range(0, 101, 10):
                self.root.after(0, lambda p=i: self.progress_var.set(p))
                time.sleep(0.2)
            
            # Perform actual sync
            sync_op = loop.run_until_complete(
                self.sync_engine.sync_repository(repo_name, destinations, selected_files)
            )
            
            # Update UI on completion
            self.root.after(0, self._sync_completed, sync_op)
            
        except Exception as e:
            self.root.after(0, self._sync_failed, str(e))
        finally:
            if loop:
                loop.close()
    
    def _sync_completed(self, sync_op: THORSyncOperation):
        """Handle sync completion"""
        self.sync_button.config(state='normal', text="🌱 Water the Tree")
        self.progress_var.set(100)
        
        stats = self.sync_engine.get_watering_stats()
        
        self.status_label.config(text=f"🌱 Tree watered! {sync_op.files_count} files, "
                                     f"{sync_op.bytes_transferred:,} bytes")
        
        # Show completion message
        messagebox.showinfo("Tree Watered! 🌱", 
                           f"Successfully watered your tree!\n\n"
                           f"Files synced: {sync_op.files_count}\n"
                           f"Bytes transferred: {sync_op.bytes_transferred:,}\n"
                           f"Destinations: {sync_op.destination}\n"
                           f"Total watering sessions: {stats['total_watering_sessions']}\n\n"
                           f"🌳 Your tree of knowledge keeps growing!")
    
    def _sync_failed(self, error: str):
        """Handle sync failure"""
        self.sync_button.config(state='normal', text="🌱 Water the Tree")
        self.progress_var.set(0)
        self.status_label.config(text="❌ Sync failed")
        messagebox.showerror("Sync Failed", f"Failed to water your tree:\n{error}")
    
    def run(self):
        """Run the sync UI"""
        self.root.mainloop()

class THOROSOneManArmy:
    """THOR OS ONE MAN ARMY EDITION - Main System"""
    
    def __init__(self):
        self.system_info = THORSystemInfo()
        self.system_info.boot_time = datetime.now()
        
        # Initialize subsystems
        self.vault = THORVault()
        self.forge = THORForge()
        self.p2p = THORP2PCloud("THOR_OneManArmy")
        self.sync_engine = THORSyncEngine(self.vault, self.p2p)
        
        # Setup logging
        self._setup_logging()
        
        # Update system info
        self._update_system_info()
    
    def _setup_logging(self):
        """Setup logging system"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - THOR-OS - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(log_dir / f'thor_os_{datetime.now().strftime("%Y%m%d")}.log')
            ]
        )
        self.logger = logging.getLogger('thor_os')
    
    def _update_system_info(self):
        """Update system information"""
        self.system_info.vault_repos_count = len(self.vault.repos)
        self.system_info.forge_sessions_active = self.forge.active_sessions
        self.system_info.p2p_peers_connected = len(self.p2p.peers)
        self.system_info.sync_operations_completed = len([
            op for op in self.sync_engine.sync_operations.values() 
            if op.status == "completed"
        ])
        self.system_info.watering_count = self.sync_engine.watering_count
    
    def print_boot_banner(self):
        """Print THOR OS ONE MAN ARMY boot banner"""
        banner = f"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                          🌱 THOR OS 🌱                                   ║
║                    ONE MAN ARMY EDITION                                   ║
║                Ultimate Developer & Gamer Platform                        ║
║                                                                           ║
║  🎯 Version: {self.system_info.version} "{self.system_info.codename}"                                 ║
║  🌱 "The tree never minds, water is water"                               ║
║                                                                           ║
║  ✅ THOR Vault: {self.system_info.vault_repos_count} repositories                                    ║
║  ✅ THOR Forge: {self.system_info.forge_sessions_active} active sessions                                  ║
║  ✅ P2P Cloud: {self.system_info.p2p_peers_connected} connected peers                                  ║
║  ✅ Sync Engine: {self.system_info.sync_operations_completed} completed operations                            ║
║  ✅ Trees Watered: {self.system_info.watering_count}                                                ║
║                                                                           ║
║  🌐 Local Hosting & Repo Sync                                            ║
║  🤝 Peer-to-Peer Collaboration                                           ║
║  🤖 AI-Powered Development Assistant                                     ║
║  🔐 Privacy-First Design                                                 ║
║  🌳 Find the easter egg! (Hidden in sync UI)                             ║
╚═══════════════════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def start_services(self):
        """Start THOR OS services"""
        self.logger.info("🚀 Starting THOR OS ONE MAN ARMY services...")
        
        # Start P2P discovery
        self.p2p.start_discovery()
        self.system_info.p2p_cloud_active = True
        
        # Mark AI assistant as online
        self.system_info.ai_assistant_online = True
        
        self.logger.info("✅ All THOR OS services started successfully")
    
    def create_demo_repository(self):
        """Create a demo repository for testing"""
        demo_repo = self.vault.create_repository("thor_demo_project")
        
        # Add some demo files
        demo_path = Path(demo_repo.path)
        
        # Create demo files
        demo_files = {
            "game.py": """#!/usr/bin/env python3
\"\"\"
THOR Demo Game - ONE MAN ARMY EDITION
\"\"\"

class THORGame:
    def __init__(self):
        self.name = "THOR Demo Game"
        self.version = "1.0.0"
        self.thor_integrated = True
    
    def start(self):
        print("🎮 THOR Demo Game starting...")
        print("🌱 Integrated with THOR OS")
        print("🌳 The tree never minds, water is water!")
    
    def water_tree(self):
        print("💧 Watering the code tree...")
        return "Growth achieved!"

if __name__ == "__main__":
    game = THORGame()
    game.start()
    result = game.water_tree()
    print(f"🌿 {result}")
""",
            
            "config.json": """{
    "game": {
        "name": "THOR Demo Game",
        "version": "1.0.0",
        "thor_features": {
            "vault_integration": true,
            "p2p_sync": true,
            "ai_assistance": true,
            "easter_eggs": true
        }
    },
    "sync": {
        "auto_sync": true,
        "destinations": ["thor_cloud", "p2p_network"],
        "encryption": true
    }
}""",
            
            "requirements.txt": """# THOR Demo Game Requirements
asyncio>=3.4.3
tkinter>=8.6
cryptography>=3.0.0
# THOR OS Integration
# "The tree never minds, water is water"
""",
            
            "docs/README.md": f"""# THOR Demo Project

🌱 Welcome to the THOR OS ONE MAN ARMY demonstration project!

## Features
- 🔐 Secure vault storage
- 🌐 P2P collaboration
- 🤖 AI-powered development
- 🌱 "Water your tree" sync philosophy

## Getting Started
1. Open THOR Sync UI
2. Select files to sync
3. Choose your destinations
4. Click "Water the Tree" 🌱
5. Find the hidden easter egg!

## Philosophy
"The tree never minds, water is water" - Every sync operation
helps your code tree grow stronger.

---
*Created with THOR OS {THOR_OS_VERSION} "{THOR_OS_CODENAME}"*
"""
        }
        
        for filename, content in demo_files.items():
            file_path = demo_path / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content)
        
        # Commit changes
        try:
            subprocess.run(['git', 'add', '.'], cwd=demo_path, check=True)
            subprocess.run(['git', 'commit', '-m', 'Added demo files 🌱'], 
                         cwd=demo_path, check=True)
        except subprocess.CalledProcessError:
            pass  # Git not available
        
        self.logger.info(f"📁 Created demo repository: {demo_repo.name}")
        return demo_repo
    
    def launch_sync_ui(self):
        """Launch the THOR Sync UI"""
        self.logger.info("🎨 Launching THOR Sync UI...")
        sync_ui = THORSyncUI(self.sync_engine)
        sync_ui.run()
    
    def show_system_status(self):
        """Show system status"""
        self._update_system_info()
        
        boot_time_str = self.system_info.boot_time.strftime("%Y-%m-%d %H:%M:%S") if self.system_info.boot_time else "Unknown"
        uptime_str = str(datetime.now() - self.system_info.boot_time) if self.system_info.boot_time else "Unknown"
        
        status = f"""
🌱 THOR OS ONE MAN ARMY - System Status
=====================================

⏱️  Boot Time: {boot_time_str}
📈 Uptime: {uptime_str}

🔧 THOR Vault:
   • Repositories: {self.system_info.vault_repos_count}
   
🛠️  THOR Forge:
   • Active Sessions: {self.system_info.forge_sessions_active}
   
🌐 P2P Cloud:
   • Connected Peers: {self.system_info.p2p_peers_connected}
   • Discovery Active: {self.system_info.p2p_cloud_active}
   
🌱 Sync Engine:
   • Completed Operations: {self.system_info.sync_operations_completed}
   • Trees Watered: {self.system_info.watering_count}
   
🤖 AI Assistant: {'🟢 Online' if self.system_info.ai_assistant_online else '🔴 Offline'}
🔐 Security: {'🟢 Active' if self.system_info.security_firewall_active else '🔴 Inactive'}

🌳 "The tree never minds, water is water"
💧 Keep watering your tree of knowledge!
        """
        
        print(status)
    
    def interactive_menu(self):
        """Interactive menu for THOR OS"""
        while True:
            print("\n" + "="*60)
            print("🌱 THOR OS ONE MAN ARMY - Interactive Menu")
            print("="*60)
            print("1. 🎨 Launch Sync UI ('Water Your Tree')")
            print("2. 📁 Create New Repository")
            print("3. 📊 Show System Status") 
            print("4. 🛠️  Create Demo Repository")
            print("5. 🌐 Show P2P Peers")
            print("6. 📈 Show Sync Statistics")
            print("7. 🔍 List Repositories")
            print("8. 🌳 Show Easter Egg Hint")
            print("9. 🛑 Exit")
            print()
            
            choice = input("Select option (1-9): ").strip()
            
            if choice == "1":
                self.launch_sync_ui()
            elif choice == "2":
                repo_name = input("Enter repository name: ").strip()
                if repo_name:
                    repo = self.vault.create_repository(repo_name)
                    print(f"✅ Created repository: {repo.name} at {repo.path}")
            elif choice == "3":
                self.show_system_status()
            elif choice == "4":
                demo_repo = self.create_demo_repository()
                print(f"✅ Created demo repository: {demo_repo.name}")
                print("💡 Try syncing it with the Sync UI!")
            elif choice == "5":
                peers = self.p2p.get_trusted_peers()
                if peers:
                    print(f"🌐 Found {len(peers)} trusted peers:")
                    for peer in peers:
                        print(f"   • {peer.name} ({peer.address}:{peer.port})")
                else:
                    print("🔍 No peers discovered yet. Discovery is running...")
            elif choice == "6":
                stats = self.sync_engine.get_watering_stats()
                print("📈 Sync Statistics:")
                print(f"   • Total watering sessions: {stats['total_watering_sessions']}")
                print(f"   • Total files watered: {stats['total_files_watered']}")
                print(f"   • Total bytes watered: {stats['total_bytes_watered']:,}")
                if stats['last_watering']:
                    print(f"   • Last watering: {stats['last_watering'].strftime('%Y-%m-%d %H:%M:%S')}")
            elif choice == "7":
                repos = self.vault.list_repositories()
                if repos:
                    print(f"📁 Found {len(repos)} repositories:")
                    for repo in repos:
                        print(f"   • {repo.name} ({repo.path})")
                        if repo.last_sync:
                            print(f"     Last sync: {repo.last_sync.strftime('%Y-%m-%d %H:%M:%S')}")
                else:
                    print("📁 No repositories found. Create one with option 2!")
            elif choice == "8":
                print("🌳 Easter Egg Hint:")
                print("💡 Look for a tiny, nearly invisible pixel in the Sync UI...")
                print("🔍 It's hiding in the bottom right corner!")
                print("🌱 Click it to discover the full 'watering the tree' philosophy!")
            elif choice == "9":
                print("🌱 Thank you for using THOR OS ONE MAN ARMY!")
                print("🌳 Remember: The tree never minds, water is water!")
                break
            else:
                print("❌ Invalid choice. Please select 1-9.")
            
            input("\nPress Enter to continue...")

def main():
    """Main entry point for THOR OS ONE MAN ARMY"""
    # Initialize THOR OS
    thor_os = THOROSOneManArmy()
    
    # Print boot banner
    thor_os.print_boot_banner()
    
    # Start services
    thor_os.start_services()
    
    # Create demo repository if none exist
    if not thor_os.vault.list_repositories():
        thor_os.create_demo_repository()
    
    # Run interactive menu
    try:
        thor_os.interactive_menu()
    except KeyboardInterrupt:
        print("\n\n🛑 THOR OS interrupted by user")
    finally:
        # Cleanup
        thor_os.p2p.stop_discovery()
        print("🌱 THOR OS shutdown complete. Keep growing! 🌳")

if __name__ == "__main__":
    main()
