#!/usr/bin/env python3
"""
THOR Gamer OS - Unified Developer & Gamer Platform
Core System Implementation with Repo Sync and P2P Collaboration

Features:
- Local hosting & repo sync ("Watering the Tree")
- Ethical & free storage options
- Peer-to-peer THOR Cloud
- AI-assisted development and gaming
- Privacy-first design with GDPR compliance

Created as part of THOR-OS "ONE MAN ARMY" Ultimate Implementation
"""

import os
import json
import sqlite3
import asyncio
import hashlib
import logging
import platform
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Set
from pathlib import Path
import aiohttp
import websockets
import git
from dataclasses import dataclass, asdict
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import uuid
import threading
import queue
from collections import defaultdict

@dataclass
class THORRepo:
    """Represents a THOR repository"""
    repo_id: str
    name: str
    path: str
    remote_url: Optional[str]
    branch: str
    last_sync: Optional[datetime]
    sync_enabled: bool
    encryption_enabled: bool
    storage_type: str  # 'thor_cloud', 's3', 'ipfs', 'peer'
    access_level: str  # 'private', 'public', 'team'
    created_at: datetime
    
@dataclass
class SyncOperation:
    """Represents a sync operation"""
    operation_id: str
    repo_id: str
    operation_type: str  # 'push', 'pull', 'merge'
    files: List[str]
    destination: str
    status: str  # 'pending', 'running', 'completed', 'failed'
    progress: float
    created_at: datetime
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None

@dataclass
class PeerNode:
    """Represents a THOR peer node"""
    node_id: str
    address: str
    port: int
    public_key: str
    capabilities: List[str]
    last_seen: datetime
    trust_score: float
    shared_repos: List[str]

class THORRepoManager:
    """Core repository management system"""
    
    def __init__(self, data_dir: str = "thor_gamer_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.db_path = self.data_dir / "thor_repos.db"
        self.repos_dir = self.data_dir / "repositories"
        self.sync_dir = self.data_dir / "sync_staging"
        self.repos_dir.mkdir(exist_ok=True)
        self.sync_dir.mkdir(exist_ok=True)
        
        self.logger = self._setup_logging()
        self._init_database()
        
        # Encryption setup
        self.encryption_key = self._get_or_create_encryption_key()
        self.cipher_suite = Fernet(self.encryption_key)
        
        # Active repositories
        self.active_repos: Dict[str, git.Repo] = {}
        self.sync_queue = queue.Queue()
        self.sync_thread = None
        
        # AI suggestions cache
        self.ai_suggestions: Dict[str, List[str]] = defaultdict(list)
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for repo manager"""
        logger = logging.getLogger('thor_repo_manager')
        logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler(self.data_dir / 'repo_manager.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def _init_database(self):
        """Initialize the repository database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Repositories table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS repositories (
            repo_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            path TEXT NOT NULL,
            remote_url TEXT,
            branch TEXT DEFAULT 'main',
            last_sync TIMESTAMP,
            sync_enabled BOOLEAN DEFAULT 1,
            encryption_enabled BOOLEAN DEFAULT 1,
            storage_type TEXT DEFAULT 'thor_cloud',
            access_level TEXT DEFAULT 'private',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Sync operations table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS sync_operations (
            operation_id TEXT PRIMARY KEY,
            repo_id TEXT,
            operation_type TEXT,
            files TEXT,
            destination TEXT,
            status TEXT DEFAULT 'pending',
            progress REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            error_message TEXT,
            FOREIGN KEY (repo_id) REFERENCES repositories (repo_id)
        )''')
        
        # File tracking table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS file_tracking (
            file_id TEXT PRIMARY KEY,
            repo_id TEXT,
            file_path TEXT,
            file_hash TEXT,
            last_modified TIMESTAMP,
            sync_status TEXT DEFAULT 'pending',
            ai_recommended BOOLEAN DEFAULT 0,
            FOREIGN KEY (repo_id) REFERENCES repositories (repo_id)
        )''')
        
        # AI suggestions table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ai_suggestions (
            suggestion_id TEXT PRIMARY KEY,
            repo_id TEXT,
            suggestion_type TEXT,
            suggestion_text TEXT,
            priority INTEGER DEFAULT 5,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (repo_id) REFERENCES repositories (repo_id)
        )''')
        
        conn.commit()
        conn.close()
    
    def _get_or_create_encryption_key(self) -> bytes:
        """Get or create encryption key for secure storage"""
        key_file = self.data_dir / ".thor_encryption_key"
        
        if key_file.exists():
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            # Generate new key
            password = b"THOR_GAMER_OS_ENCRYPTION_KEY_2025"
            salt = os.urandom(16)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password))
            
            with open(key_file, 'wb') as f:
                f.write(key)
            
            # Hide the key file
            if platform.system() == "Windows":
                os.system(f'attrib +h "{key_file}"')
            
            return key
    
    async def create_repository(self, name: str, path: str, 
                              init_git: bool = True) -> THORRepo:
        """Create a new THOR repository"""
        repo_id = str(uuid.uuid4())
        repo_path = Path(path)
        
        try:
            # Create directory if it doesn't exist
            repo_path.mkdir(parents=True, exist_ok=True)
            
            # Initialize Git repository if requested
            if init_git:
                git_repo = git.Repo.init(repo_path)
                
                # Create initial commit
                readme_path = repo_path / "README.md"
                with open(readme_path, 'w') as f:
                    f.write(f"# {name}\n\nTHOR Gamer OS Repository\n")
                
                git_repo.index.add([str(readme_path)])
                git_repo.index.commit("Initial THOR commit - The tree begins to grow")
                
                self.active_repos[repo_id] = git_repo
            
            # Create THOR repo object
            thor_repo = THORRepo(
                repo_id=repo_id,
                name=name,
                path=str(repo_path),
                remote_url=None,
                branch='main',
                last_sync=None,
                sync_enabled=True,
                encryption_enabled=True,
                storage_type='thor_cloud',
                access_level='private',
                created_at=datetime.now()
            )
            
            # Store in database
            await self._store_repository(thor_repo)
            
            self.logger.info(f"Created THOR repository: {name} at {path}")
            return thor_repo
            
        except Exception as e:
            self.logger.error(f"Failed to create repository {name}: {str(e)}")
            raise
    
    async def _store_repository(self, repo: THORRepo):
        """Store repository in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT OR REPLACE INTO repositories
        (repo_id, name, path, remote_url, branch, last_sync,
         sync_enabled, encryption_enabled, storage_type, access_level, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            repo.repo_id, repo.name, repo.path, repo.remote_url,
            repo.branch, repo.last_sync, repo.sync_enabled,
            repo.encryption_enabled, repo.storage_type,
            repo.access_level, repo.created_at
        ))
        
        conn.commit()
        conn.close()
    
    async def get_repositories(self) -> List[THORRepo]:
        """Get all repositories"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM repositories ORDER BY created_at DESC')
        rows = cursor.fetchall()
        conn.close()
        
        repos = []
        for row in rows:
            repo = THORRepo(
                repo_id=row[0],
                name=row[1], 
                path=row[2],
                remote_url=row[3],
                branch=row[4],
                last_sync=datetime.fromisoformat(row[5]) if row[5] else None,
                sync_enabled=bool(row[6]),
                encryption_enabled=bool(row[7]),
                storage_type=row[8],
                access_level=row[9],
                created_at=datetime.fromisoformat(row[10])
            )
            repos.append(repo)
        
        return repos
    
    async def scan_repo_changes(self, repo_id: str) -> Dict[str, Any]:
        """Scan repository for changes and AI recommendations"""
        try:
            repo = await self._get_repository(repo_id)
            if not repo:
                return {"error": "Repository not found"}
            
            git_repo = self._get_git_repo(repo)
            if not git_repo:
                return {"error": "Git repository not initialized"}
            
            # Get file changes
            changed_files = []
            untracked_files = []
            
            # Check for modified files
            for item in git_repo.index.diff(None):
                changed_files.append({
                    'path': item.a_path,
                    'change_type': 'modified',
                    'ai_recommended': await self._ai_should_sync_file(item.a_path)
                })
            
            # Check for untracked files
            for file_path in git_repo.untracked_files:
                untracked_files.append({
                    'path': file_path,
                    'change_type': 'untracked',
                    'ai_recommended': await self._ai_should_sync_file(file_path)
                })
            
            # Generate AI suggestions
            suggestions = await self._generate_ai_suggestions(repo_id, changed_files + untracked_files)
            
            return {
                'repo_id': repo_id,
                'changed_files': changed_files,
                'untracked_files': untracked_files,
                'ai_suggestions': suggestions,
                'total_changes': len(changed_files) + len(untracked_files)
            }
            
        except Exception as e:
            self.logger.error(f"Failed to scan repo changes: {str(e)}")
            return {"error": str(e)}
    
    async def _ai_should_sync_file(self, file_path: str) -> bool:
        """AI determines if file should be synced"""
        # AI logic for determining sync recommendations
        file_ext = Path(file_path).suffix.lower()
        
        # Recommended file types for syncing
        sync_extensions = {
            '.py', '.js', '.ts', '.html', '.css', '.cpp', '.c', '.h',
            '.java', '.cs', '.php', '.rb', '.go', '.rs', '.swift',
            '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg',
            '.md', '.txt', '.rst', '.adoc',
            '.unity', '.unreal', '.blend', '.fbx', '.obj',
            '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico',
            '.mp3', '.wav', '.ogg', '.mp4', '.avi', '.mov'
        }
        
        # Skip temporary/cache files
        skip_patterns = {
            '__pycache__', '.git', 'node_modules', '.vscode',
            'temp', 'tmp', '.cache', 'build', 'dist'
        }
        
        # Check if file should be skipped
        for pattern in skip_patterns:
            if pattern in file_path:
                return False
        
        # Check if file extension is recommended
        return file_ext in sync_extensions
    
    async def _generate_ai_suggestions(self, repo_id: str, files: List[Dict]) -> List[str]:
        """Generate AI suggestions for repository actions"""
        suggestions = []
        
        recommended_files = [f for f in files if f.get('ai_recommended', False)]
        
        if recommended_files:
            suggestions.append(f"🌱 THOR recommends syncing {len(recommended_files)} files to water your tree")
        
        # Check for common patterns
        has_config_changes = any('config' in f['path'].lower() for f in files)
        has_source_changes = any(f['path'].endswith(('.py', '.js', '.cpp', '.c')) for f in files)
        has_asset_changes = any(f['path'].endswith(('.png', '.jpg', '.mp3', '.fbx')) for f in files)
        
        if has_config_changes:
            suggestions.append("⚙️ Configuration changes detected - Consider creating a backup")
        
        if has_source_changes:
            suggestions.append("💻 Source code changes found - Ready for collaborative review")
        
        if has_asset_changes:
            suggestions.append("🎨 Asset updates available - Perfect for sharing with the community")
        
        # Check file count for bulk operations
        if len(files) > 10:
            suggestions.append("📦 Multiple files changed - Consider using bulk sync operation")
        
        # Store suggestions in database
        await self._store_ai_suggestions(repo_id, suggestions)
        
        return suggestions
    
    async def _store_ai_suggestions(self, repo_id: str, suggestions: List[str]):
        """Store AI suggestions in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for i, suggestion in enumerate(suggestions):
            suggestion_id = f"{repo_id}_suggestion_{int(datetime.now().timestamp())}_{i}"
            cursor.execute('''
            INSERT INTO ai_suggestions
            (suggestion_id, repo_id, suggestion_type, suggestion_text, priority)
            VALUES (?, ?, ?, ?, ?)
            ''', (suggestion_id, repo_id, 'sync_recommendation', suggestion, 5 + i))
        
        conn.commit()
        conn.close()
    
    async def prepare_sync_operation(self, repo_id: str, files: List[str], 
                                   destination: str) -> SyncOperation:
        """Prepare a sync operation"""
        operation_id = str(uuid.uuid4())
        
        sync_op = SyncOperation(
            operation_id=operation_id,
            repo_id=repo_id,
            operation_type='push',
            files=files,
            destination=destination,
            status='pending',
            progress=0.0,
            created_at=datetime.now()
        )
        
        # Store in database
        await self._store_sync_operation(sync_op)
        
        # Add to sync queue
        self.sync_queue.put(sync_op)
        
        # Start sync thread if not running
        if not self.sync_thread or not self.sync_thread.is_alive():
            self.sync_thread = threading.Thread(target=self._sync_worker)
            self.sync_thread.daemon = True
            self.sync_thread.start()
        
        return sync_op
    
    async def _store_sync_operation(self, sync_op: SyncOperation):
        """Store sync operation in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT OR REPLACE INTO sync_operations
        (operation_id, repo_id, operation_type, files, destination,
         status, progress, created_at, completed_at, error_message)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            sync_op.operation_id, sync_op.repo_id, sync_op.operation_type,
            json.dumps(sync_op.files), sync_op.destination, sync_op.status,
            sync_op.progress, sync_op.created_at, sync_op.completed_at,
            sync_op.error_message
        ))
        
        conn.commit()
        conn.close()
    
    def _sync_worker(self):
        """Background worker for sync operations"""
        while True:
            try:
                sync_op = self.sync_queue.get(timeout=1)
                if sync_op:
                    asyncio.run(self._execute_sync_operation(sync_op))
                    self.sync_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                self.logger.error(f"Sync worker error: {str(e)}")
    
    async def _execute_sync_operation(self, sync_op: SyncOperation):
        """Execute a sync operation"""
        try:
            self.logger.info(f"Starting sync operation: {sync_op.operation_id}")
            
            # Update status to running
            sync_op.status = 'running'
            await self._store_sync_operation(sync_op)
            
            repo = await self._get_repository(sync_op.repo_id)
            if not repo:
                raise Exception("Repository not found")
            
            # Execute sync based on destination type
            if sync_op.destination == 'thor_cloud':
                await self._sync_to_thor_cloud(sync_op, repo)
            elif sync_op.destination.startswith('s3://'):
                await self._sync_to_s3(sync_op, repo)
            elif sync_op.destination.startswith('ipfs://'):
                await self._sync_to_ipfs(sync_op, repo)
            elif sync_op.destination.startswith('peer://'):
                await self._sync_to_peer(sync_op, repo)
            else:
                raise Exception(f"Unknown destination type: {sync_op.destination}")
            
            # Mark as completed
            sync_op.status = 'completed'
            sync_op.progress = 100.0
            sync_op.completed_at = datetime.now()
            
            # Update repository last sync time
            repo.last_sync = datetime.now()
            await self._store_repository(repo)
            
            self.logger.info(f"Sync operation completed: {sync_op.operation_id}")
            
        except Exception as e:
            sync_op.status = 'failed'
            sync_op.error_message = str(e)
            self.logger.error(f"Sync operation failed: {str(e)}")
        
        finally:
            await self._store_sync_operation(sync_op)
    
    async def _sync_to_thor_cloud(self, sync_op: SyncOperation, repo: THORRepo):
        """Sync to THOR Cloud"""
        # Simulate cloud sync with progress updates
        total_files = len(sync_op.files)
        
        for i, file_path in enumerate(sync_op.files):
            # Simulate file upload
            await asyncio.sleep(0.1)  # Simulate network delay
            
            # Update progress
            sync_op.progress = ((i + 1) / total_files) * 100
            await self._store_sync_operation(sync_op)
            
            self.logger.info(f"Synced file to THOR Cloud: {file_path}")
        
        self.logger.info("THOR Cloud sync completed - Your tree has been watered! 🌱")
    
    async def _sync_to_s3(self, sync_op: SyncOperation, repo: THORRepo):
        """Sync to S3-compatible storage"""
        # Implementation for S3 sync
        for file_path in sync_op.files:
            self.logger.info(f"Syncing to S3: {file_path}")
            # Add actual S3 upload logic here
    
    async def _sync_to_ipfs(self, sync_op: SyncOperation, repo: THORRepo):
        """Sync to IPFS"""
        # Implementation for IPFS sync
        for file_path in sync_op.files:
            self.logger.info(f"Syncing to IPFS: {file_path}")
            # Add actual IPFS upload logic here
    
    async def _sync_to_peer(self, sync_op: SyncOperation, repo: THORRepo):
        """Sync to peer node"""
        # Implementation for peer-to-peer sync
        for file_path in sync_op.files:
            self.logger.info(f"Syncing to peer: {file_path}")
            # Add actual P2P sync logic here
    
    async def _get_repository(self, repo_id: str) -> Optional[THORRepo]:
        """Get repository by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM repositories WHERE repo_id = ?', (repo_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return THORRepo(
            repo_id=row[0],
            name=row[1],
            path=row[2],
            remote_url=row[3],
            branch=row[4],
            last_sync=datetime.fromisoformat(row[5]) if row[5] else None,
            sync_enabled=bool(row[6]),
            encryption_enabled=bool(row[7]),
            storage_type=row[8],
            access_level=row[9],
            created_at=datetime.fromisoformat(row[10])
        )
    
    def _get_git_repo(self, repo: THORRepo) -> Optional[git.Repo]:
        """Get Git repository object"""
        if repo.repo_id in self.active_repos:
            return self.active_repos[repo.repo_id]
        
        try:
            git_repo = git.Repo(repo.path)
            self.active_repos[repo.repo_id] = git_repo
            return git_repo
        except:
            return None
    
    async def get_sync_status(self, repo_id: str) -> Dict[str, Any]:
        """Get sync status for repository"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get recent sync operations
        cursor.execute('''
        SELECT * FROM sync_operations 
        WHERE repo_id = ? 
        ORDER BY created_at DESC 
        LIMIT 10
        ''', (repo_id,))
        
        operations = []
        for row in cursor.fetchall():
            operations.append({
                'operation_id': row[0],
                'operation_type': row[2],
                'status': row[5],
                'progress': row[6],
                'created_at': row[7],
                'error_message': row[9]
            })
        
        conn.close()
        
        return {
            'repo_id': repo_id,
            'recent_operations': operations,
            'last_sync_status': operations[0]['status'] if operations else 'never'
        }

# The Tree Watering Easter Egg System
class TreeWateringEasterEgg:
    """Hidden easter egg system for the 'watering the tree' metaphor"""
    
    def __init__(self):
        self.easter_egg_triggered = False
        self.water_count = 0
        self.growth_stages = [
            "🌱 A small seed has been planted...",
            "🌿 Your tree begins to sprout!",
            "🌳 Strong branches are growing!",
            "🌲 Your tree stands tall and proud!",
            "🎋 A magnificent forest of knowledge!"
        ]
    
    def trigger_easter_egg(self) -> str:
        """Trigger the hidden easter egg message"""
        self.easter_egg_triggered = True
        
        messages = [
            "🌱 The tree never minds, water is water.",
            "💧 You've turned a pissed-on situation into growth. Water your tree!",
            "🌳 Every drop of knowledge feeds the forest of innovation.",
            "🚀 From humble seeds grow mighty trees of code.",
            "🎮 Your commits are the water, your repo is the tree."
        ]
        
        import random
        return random.choice(messages)
    
    def water_tree(self) -> str:
        """Water the tree and show growth"""
        self.water_count += 1
        stage = min(self.water_count // 5, len(self.growth_stages) - 1)
        return self.growth_stages[stage]
    
    def get_tree_status(self) -> Dict[str, Any]:
        """Get current tree status"""
        stage = min(self.water_count // 5, len(self.growth_stages) - 1)
        
        return {
            'water_count': self.water_count,
            'growth_stage': stage,
            'status_message': self.growth_stages[stage],
            'easter_egg_found': self.easter_egg_triggered
        }

async def main():
    """Example usage of THOR Gamer OS Repo Manager"""
    # Create repo manager
    repo_manager = THORRepoManager()
    
    # Create a sample repository
    repo = await repo_manager.create_repository(
        name="My Game Project",
        path="./test_game_project"
    )
    
    print(f"Created repository: {repo.name}")
    
    # Scan for changes
    changes = await repo_manager.scan_repo_changes(repo.repo_id)
    print(f"Repository changes: {changes}")
    
    # Prepare sync operation
    if changes.get('untracked_files'):
        files_to_sync = [f['path'] for f in changes['untracked_files'] if f['ai_recommended']]
        if files_to_sync:
            sync_op = await repo_manager.prepare_sync_operation(
                repo.repo_id, 
                files_to_sync, 
                'thor_cloud'
            )
            print(f"Sync operation created: {sync_op.operation_id}")
    
    # Easter egg demonstration
    easter_egg = TreeWateringEasterEgg()
    print(f"Easter egg: {easter_egg.trigger_easter_egg()}")
    print(f"Tree watered: {easter_egg.water_tree()}")

if __name__ == "__main__":
    asyncio.run(main())
