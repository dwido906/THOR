#!/usr/bin/env python3
"""
THOR P2P Cloud System - Peer-to-Peer Collaboration Network
Part of THOR Gamer OS Unified Platform

Features:
- Peer discovery and networking
- Secure file sharing and sync
- Decentralized collaboration
- Node hosting and management
- Trust-based reputation system

Created as part of THOR-OS "ONE MAN ARMY" Ultimate Implementation
"""

import asyncio
import json
import socket
import hashlib
import logging
import platform
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set, Tuple
from pathlib import Path
import websockets
import ssl
from dataclasses import dataclass, asdict
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import uuid
import zlib
import time

@dataclass
class THORPeerNode:
    """Represents a THOR peer node in the network"""
    node_id: str
    address: str
    port: int
    public_key_pem: str
    capabilities: List[str]
    node_type: str  # 'full', 'light', 'bridge'
    last_seen: datetime
    trust_score: float
    shared_repos: List[str]
    bandwidth_limit: int  # KB/s
    storage_available: int  # MB
    
@dataclass 
class P2PMessage:
    """Represents a P2P network message"""
    message_id: str
    sender_id: str
    receiver_id: str
    message_type: str
    payload: Dict[str, Any]
    timestamp: datetime
    signature: Optional[str] = None

@dataclass
class FileShare:
    """Represents a shared file in the P2P network"""
    file_id: str
    file_name: str
    file_hash: str
    file_size: int
    owner_node: str
    access_level: str  # 'public', 'private', 'team'
    encryption_key: Optional[str] = None
    created_at: datetime = None

class THORCrypto:
    """Cryptographic utilities for THOR P2P network"""
    
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self._generate_keypair()
    
    def _generate_keypair(self):
        """Generate RSA keypair for node"""
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()
    
    def get_public_key_pem(self) -> str:
        """Get public key in PEM format"""
        pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem.decode('utf-8')
    
    def sign_message(self, message: str) -> str:
        """Sign a message with private key"""
        signature = self.private_key.sign(
            message.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return base64.b64encode(signature).decode('utf-8')
    
    def verify_signature(self, message: str, signature: str, public_key_pem: str) -> bool:
        """Verify message signature"""
        try:
            public_key = serialization.load_pem_public_key(
                public_key_pem.encode('utf-8'),
                backend=default_backend()
            )
            
            signature_bytes = base64.b64decode(signature)
            
            public_key.verify(
                signature_bytes,
                message.encode('utf-8'),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False
    
    def encrypt_data(self, data: bytes, public_key_pem: str) -> bytes:
        """Encrypt data with public key"""
        public_key = serialization.load_pem_public_key(
            public_key_pem.encode('utf-8'),
            backend=default_backend()
        )
        
        # Generate AES key for actual encryption
        aes_key = os.urandom(32)
        iv = os.urandom(16)
        
        # Encrypt data with AES
        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        
        # Pad data to AES block size
        padding_length = 16 - (len(data) % 16)
        padded_data = data + bytes([padding_length] * padding_length)
        
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        
        # Encrypt AES key with RSA
        encrypted_key = public_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Combine encrypted key, IV, and data
        return encrypted_key + iv + encrypted_data
    
    def decrypt_data(self, encrypted_data: bytes) -> bytes:
        """Decrypt data with private key"""
        # Extract components
        encrypted_key = encrypted_data[:256]  # RSA key size
        iv = encrypted_data[256:272]  # IV size
        ciphertext = encrypted_data[272:]
        
        # Decrypt AES key
        aes_key = self.private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Decrypt data
        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Remove padding
        padding_length = padded_data[-1]
        return padded_data[:-padding_length]

class THORPeerDiscovery:
    """Peer discovery service for THOR P2P network"""
    
    def __init__(self, node_id: str, port: int = 8888):
        self.node_id = node_id
        self.port = port
        self.discovered_peers: Dict[str, THORPeerNode] = {}
        self.discovery_active = False
        self.logger = logging.getLogger('thor_peer_discovery')
        
    async def start_discovery(self):
        """Start peer discovery service"""
        self.discovery_active = True
        
        # Start UDP broadcast listener
        asyncio.create_task(self._udp_discovery_listener())
        
        # Start periodic broadcast
        asyncio.create_task(self._periodic_broadcast())
        
        # Start web discovery (for internet peers)
        asyncio.create_task(self._web_discovery())
        
        self.logger.info(f"Peer discovery started on port {self.port}")
    
    async def _udp_discovery_listener(self):
        """Listen for UDP discovery broadcasts"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', self.port))
        
        while self.discovery_active:
            try:
                data, addr = sock.recvfrom(1024)
                await self._handle_discovery_message(data, addr)
            except Exception as e:
                self.logger.error(f"UDP discovery error: {str(e)}")
                await asyncio.sleep(1)
    
    async def _handle_discovery_message(self, data: bytes, addr: Tuple[str, int]):
        """Handle incoming discovery message"""
        try:
            message = json.loads(data.decode('utf-8'))
            
            if message.get('type') == 'thor_peer_announce':
                peer_info = message.get('peer_info')
                if peer_info and peer_info['node_id'] != self.node_id:
                    # Create peer node object
                    peer = THORPeerNode(
                        node_id=peer_info['node_id'],
                        address=addr[0],
                        port=peer_info.get('port', 8889),
                        public_key_pem=peer_info.get('public_key', ''),
                        capabilities=peer_info.get('capabilities', []),
                        node_type=peer_info.get('node_type', 'light'),
                        last_seen=datetime.now(),
                        trust_score=0.5,  # Initial trust score
                        shared_repos=peer_info.get('shared_repos', []),
                        bandwidth_limit=peer_info.get('bandwidth_limit', 1000),
                        storage_available=peer_info.get('storage_available', 1000)
                    )
                    
                    self.discovered_peers[peer.node_id] = peer
                    self.logger.info(f"Discovered THOR peer: {peer.node_id} at {addr[0]}")
        
        except Exception as e:
            self.logger.error(f"Failed to handle discovery message: {str(e)}")
    
    async def _periodic_broadcast(self):
        """Periodically broadcast node presence"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        while self.discovery_active:
            try:
                # Create announcement message
                announcement = {
                    'type': 'thor_peer_announce',
                    'peer_info': {
                        'node_id': self.node_id,
                        'port': self.port + 1,  # Data port
                        'capabilities': ['sync', 'storage', 'relay'],
                        'node_type': 'full',
                        'shared_repos': [],
                        'bandwidth_limit': 10000,
                        'storage_available': 50000
                    }
                }
                
                message = json.dumps(announcement).encode('utf-8')
                sock.sendto(message, ('<broadcast>', self.port))
                
                await asyncio.sleep(30)  # Broadcast every 30 seconds
                
            except Exception as e:
                self.logger.error(f"Broadcast error: {str(e)}")
                await asyncio.sleep(5)
    
    async def _web_discovery(self):
        """Discover peers through web services"""
        # This would connect to THOR discovery servers on the internet
        discovery_urls = [
            "wss://thor-discovery.example.com/peers",
            "wss://thor-network.example.com/discover"
        ]
        
        while self.discovery_active:
            try:
                # In a real implementation, connect to discovery servers
                await asyncio.sleep(60)  # Check every minute
            except Exception as e:
                self.logger.error(f"Web discovery error: {str(e)}")
                await asyncio.sleep(30)
    
    def get_discovered_peers(self) -> List[THORPeerNode]:
        """Get list of discovered peers"""
        # Remove stale peers (not seen in 5 minutes)
        current_time = datetime.now()
        stale_peers = [
            node_id for node_id, peer in self.discovered_peers.items()
            if current_time - peer.last_seen > timedelta(minutes=5)
        ]
        
        for node_id in stale_peers:
            del self.discovered_peers[node_id]
        
        return list(self.discovered_peers.values())

class THORPeerConnection:
    """Manages connection to a THOR peer"""
    
    def __init__(self, peer: THORPeerNode, crypto: THORCrypto):
        self.peer = peer
        self.crypto = crypto
        self.websocket = None
        self.connected = False
        self.message_queue = asyncio.Queue()
        self.logger = logging.getLogger('thor_peer_connection')
    
    async def connect(self) -> bool:
        """Connect to the peer"""
        try:
            uri = f"ws://{self.peer.address}:{self.peer.port}/thor"
            self.websocket = await websockets.connect(uri)
            self.connected = True
            
            # Start message handler
            asyncio.create_task(self._message_handler())
            
            # Send handshake
            await self._send_handshake()
            
            self.logger.info(f"Connected to THOR peer: {self.peer.node_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to connect to peer {self.peer.node_id}: {str(e)}")
            return False
    
    async def _send_handshake(self):
        """Send handshake message to peer"""
        handshake = P2PMessage(
            message_id=str(uuid.uuid4()),
            sender_id=self.crypto.node_id,
            receiver_id=self.peer.node_id,
            message_type='handshake',
            payload={
                'public_key': self.crypto.get_public_key_pem(),
                'capabilities': ['sync', 'storage', 'relay'],
                'protocol_version': '1.0'
            },
            timestamp=datetime.now()
        )
        
        await self.send_message(handshake)
    
    async def send_message(self, message: P2PMessage):
        """Send message to peer"""
        if not self.connected or not self.websocket:
            raise Exception("Not connected to peer")
        
        # Sign the message
        message_data = json.dumps(asdict(message), default=str)
        message.signature = self.crypto.sign_message(message_data)
        
        # Send message
        signed_data = json.dumps(asdict(message), default=str)
        await self.websocket.send(signed_data)
    
    async def _message_handler(self):
        """Handle incoming messages from peer"""
        try:
            async for message_data in self.websocket:
                try:
                    message_dict = json.loads(message_data)
                    message = P2PMessage(**message_dict)
                    
                    # Verify signature
                    message_without_sig = message_dict.copy()
                    del message_without_sig['signature']
                    message_content = json.dumps(message_without_sig, default=str)
                    
                    if self.crypto.verify_signature(
                        message_content, 
                        message.signature, 
                        self.peer.public_key_pem
                    ):
                        await self.message_queue.put(message)
                    else:
                        self.logger.warning(f"Invalid signature from peer {self.peer.node_id}")
                
                except Exception as e:
                    self.logger.error(f"Failed to handle message: {str(e)}")
        
        except websockets.exceptions.ConnectionClosed:
            self.connected = False
            self.logger.info(f"Connection to peer {self.peer.node_id} closed")
    
    async def get_message(self) -> Optional[P2PMessage]:
        """Get next message from peer"""
        try:
            return await asyncio.wait_for(self.message_queue.get(), timeout=1.0)
        except asyncio.TimeoutError:
            return None
    
    async def disconnect(self):
        """Disconnect from peer"""
        if self.websocket:
            await self.websocket.close()
        self.connected = False

class THORFileSharing:
    """File sharing system for THOR P2P network"""
    
    def __init__(self, crypto: THORCrypto, storage_dir: str = "thor_p2p_storage"):
        self.crypto = crypto
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.shared_files: Dict[str, FileShare] = {}
        self.logger = logging.getLogger('thor_file_sharing')
    
    async def share_file(self, file_path: str, access_level: str = 'private') -> FileShare:
        """Share a file on the P2P network"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Calculate file hash
        file_content = file_path.read_bytes()
        file_hash = hashlib.sha256(file_content).hexdigest()
        
        # Create file share object
        file_share = FileShare(
            file_id=str(uuid.uuid4()),
            file_name=file_path.name,
            file_hash=file_hash,
            file_size=len(file_content),
            owner_node=self.crypto.node_id,
            access_level=access_level,
            created_at=datetime.now()
        )
        
        # Encrypt file if private
        if access_level == 'private':
            # Generate encryption key
            encryption_key = os.urandom(32)
            file_share.encryption_key = base64.b64encode(encryption_key).decode('utf-8')
            
            # Encrypt file content
            iv = os.urandom(16)
            cipher = Cipher(algorithms.AES(encryption_key), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            
            # Pad content
            padding_length = 16 - (len(file_content) % 16)
            padded_content = file_content + bytes([padding_length] * padding_length)
            
            encrypted_content = iv + encryptor.update(padded_content) + encryptor.finalize()
            
            # Store encrypted file
            storage_path = self.storage_dir / f"{file_share.file_id}.enc"
            storage_path.write_bytes(encrypted_content)
        else:
            # Store file as-is for public access
            storage_path = self.storage_dir / f"{file_share.file_id}.dat"
            storage_path.write_bytes(file_content)
        
        self.shared_files[file_share.file_id] = file_share
        
        self.logger.info(f"File shared: {file_share.file_name} ({access_level})")
        return file_share
    
    async def download_file(self, file_share: FileShare, 
                          download_path: str = None) -> Optional[Path]:
        """Download a file from the P2P network"""
        try:
            # Check if we have the file locally
            if file_share.access_level == 'private':
                storage_path = self.storage_dir / f"{file_share.file_id}.enc"
            else:
                storage_path = self.storage_dir / f"{file_share.file_id}.dat"
            
            if storage_path.exists():
                # Decrypt if needed
                file_content = storage_path.read_bytes()
                
                if file_share.access_level == 'private' and file_share.encryption_key:
                    # Decrypt file
                    encryption_key = base64.b64decode(file_share.encryption_key)
                    
                    iv = file_content[:16]
                    encrypted_content = file_content[16:]
                    
                    cipher = Cipher(algorithms.AES(encryption_key), modes.CBC(iv), backend=default_backend())
                    decryptor = cipher.decryptor()
                    padded_content = decryptor.update(encrypted_content) + decryptor.finalize()
                    
                    # Remove padding
                    padding_length = padded_content[-1]
                    file_content = padded_content[:-padding_length]
                
                # Save to download path
                if download_path:
                    output_path = Path(download_path)
                else:
                    output_path = Path(f"downloads/{file_share.file_name}")
                
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(file_content)
                
                self.logger.info(f"File downloaded: {file_share.file_name}")
                return output_path
            
            # TODO: Request file from other peers
            self.logger.warning(f"File not available locally: {file_share.file_name}")
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to download file: {str(e)}")
            return None
    
    def get_shared_files(self) -> List[FileShare]:
        """Get list of shared files"""
        return list(self.shared_files.values())

class THORPeerToPeer:
    """Main THOR P2P system coordinator"""
    
    def __init__(self, node_id: str = None, data_dir: str = "thor_p2p_data"):
        self.node_id = node_id or str(uuid.uuid4())
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize components
        self.crypto = THORCrypto()
        self.discovery = THORPeerDiscovery(self.node_id)
        self.file_sharing = THORFileSharing(self.crypto, str(self.data_dir / "storage"))
        
        # Peer connections
        self.connections: Dict[str, THORPeerConnection] = {}
        
        # System state
        self.running = False
        self.logger = self._setup_logging()
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for P2P system"""
        logger = logging.getLogger('thor_p2p')
        logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler(self.data_dir / 'p2p.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    async def start(self):
        """Start the THOR P2P system"""
        self.running = True
        
        # Start peer discovery
        await self.discovery.start_discovery()
        
        # Start connection manager
        asyncio.create_task(self._connection_manager())
        
        # Start message processor
        asyncio.create_task(self._message_processor())
        
        self.logger.info(f"THOR P2P system started - Node ID: {self.node_id}")
    
    async def _connection_manager(self):
        """Manage peer connections"""
        while self.running:
            try:
                # Get discovered peers
                peers = self.discovery.get_discovered_peers()
                
                # Connect to new peers
                for peer in peers:
                    if peer.node_id not in self.connections and len(self.connections) < 10:
                        connection = THORPeerConnection(peer, self.crypto)
                        if await connection.connect():
                            self.connections[peer.node_id] = connection
                
                # Remove dead connections
                dead_connections = [
                    node_id for node_id, conn in self.connections.items()
                    if not conn.connected
                ]
                
                for node_id in dead_connections:
                    del self.connections[node_id]
                
                await asyncio.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                self.logger.error(f"Connection manager error: {str(e)}")
                await asyncio.sleep(5)
    
    async def _message_processor(self):
        """Process messages from all connected peers"""
        while self.running:
            try:
                for connection in list(self.connections.values()):
                    message = await connection.get_message()
                    if message:
                        await self._handle_peer_message(message, connection)
                
                await asyncio.sleep(0.1)  # Small delay to prevent busy waiting
                
            except Exception as e:
                self.logger.error(f"Message processor error: {str(e)}")
                await asyncio.sleep(1)
    
    async def _handle_peer_message(self, message: P2PMessage, connection: THORPeerConnection):
        """Handle message from peer"""
        try:
            if message.message_type == 'handshake':
                # Handle handshake
                self.logger.info(f"Handshake from peer: {message.sender_id}")
                
                # Update peer public key
                connection.peer.public_key_pem = message.payload.get('public_key', '')
                
            elif message.message_type == 'file_share_announce':
                # Handle file share announcement
                file_info = message.payload.get('file_info')
                if file_info:
                    self.logger.info(f"Peer {message.sender_id} shared file: {file_info.get('file_name')}")
            
            elif message.message_type == 'sync_request':
                # Handle sync request
                await self._handle_sync_request(message, connection)
            
        except Exception as e:
            self.logger.error(f"Failed to handle peer message: {str(e)}")
    
    async def _handle_sync_request(self, message: P2PMessage, connection: THORPeerConnection):
        """Handle sync request from peer"""
        # Implementation for handling sync requests
        self.logger.info(f"Sync request from {message.sender_id}")
    
    async def share_repository(self, repo_path: str, access_level: str = 'private') -> List[FileShare]:
        """Share repository files on P2P network"""
        repo_path = Path(repo_path)
        shared_files = []
        
        # Share all files in repository (excluding .git)
        for file_path in repo_path.rglob('*'):
            if file_path.is_file() and '.git' not in str(file_path):
                try:
                    file_share = await self.file_sharing.share_file(str(file_path), access_level)
                    shared_files.append(file_share)
                except Exception as e:
                    self.logger.error(f"Failed to share file {file_path}: {str(e)}")
        
        # Announce shared files to connected peers
        for connection in self.connections.values():
            for file_share in shared_files:
                announce_message = P2PMessage(
                    message_id=str(uuid.uuid4()),
                    sender_id=self.node_id,
                    receiver_id=connection.peer.node_id,
                    message_type='file_share_announce',
                    payload={'file_info': asdict(file_share)},
                    timestamp=datetime.now()
                )
                
                try:
                    await connection.send_message(announce_message)
                except Exception as e:
                    self.logger.error(f"Failed to announce file share: {str(e)}")
        
        return shared_files
    
    def get_network_status(self) -> Dict[str, Any]:
        """Get P2P network status"""
        discovered_peers = self.discovery.get_discovered_peers()
        
        return {
            'node_id': self.node_id,
            'running': self.running,
            'discovered_peers': len(discovered_peers),
            'active_connections': len(self.connections),
            'shared_files': len(self.file_sharing.get_shared_files()),
            'peers': [
                {
                    'node_id': peer.node_id,
                    'address': peer.address,
                    'node_type': peer.node_type,
                    'trust_score': peer.trust_score,
                    'last_seen': peer.last_seen.isoformat()
                }
                for peer in discovered_peers
            ]
        }
    
    async def stop(self):
        """Stop the THOR P2P system"""
        self.running = False
        
        # Close all connections
        for connection in self.connections.values():
            await connection.disconnect()
        
        self.logger.info("THOR P2P system stopped")

# Integration with THOR Gamer OS
class THORGamerOSP2PIntegration:
    """Integration layer for P2P system with THOR Gamer OS"""
    
    def __init__(self, gamer_os_data_dir: str = "thor_gamer_data"):
        self.gamer_os_data_dir = Path(gamer_os_data_dir)
        self.p2p_system = THORPeerToPeer(data_dir=str(self.gamer_os_data_dir / "p2p"))
        
    async def initialize_p2p_gaming(self) -> Dict[str, Any]:
        """Initialize P2P system for gaming collaboration"""
        # Start P2P system
        await self.p2p_system.start()
        
        # Wait for peer discovery
        await asyncio.sleep(5)
        
        status = self.p2p_system.get_network_status()
        
        return {
            'p2p_initialized': True,
            'network_status': status,
            'collaboration_ready': status['discovered_peers'] > 0
        }
    
    async def sync_repository_p2p(self, repo_path: str) -> Dict[str, Any]:
        """Sync repository using P2P network"""
        shared_files = await self.p2p_system.share_repository(repo_path, 'team')
        
        return {
            'repo_path': repo_path,
            'shared_files_count': len(shared_files),
            'p2p_sync_complete': True,
            'network_peers': len(self.p2p_system.connections)
        }

async def main():
    """Example usage of THOR P2P system"""
    # Create P2P system
    p2p = THORPeerToPeer()
    
    # Start the system
    await p2p.start()
    
    print(f"THOR P2P system started - Node ID: {p2p.node_id}")
    
    # Wait a bit for peer discovery
    await asyncio.sleep(10)
    
    # Get network status
    status = p2p.get_network_status()
    print(f"Network status: {status}")
    
    # Share a file
    test_file = Path("test_share.txt")
    test_file.write_text("Hello THOR P2P Network!")
    
    file_share = await p2p.file_sharing.share_file(str(test_file), 'public')
    print(f"Shared file: {file_share.file_name}")
    
    # Keep running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await p2p.stop()

if __name__ == "__main__":
    asyncio.run(main())
