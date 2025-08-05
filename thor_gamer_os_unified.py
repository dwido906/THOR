#!/usr/bin/env python3
"""
THOR Gamer OS - Complete Unified Platform Integration
Main orchestrator for all THOR systems

Features:
- Unified system launcher and coordinator
- Integration of all THOR-OS components
- Auto-initialization and health monitoring
- Cross-system communication and data flow
- Complete "Water the Tree" workflow

Created as part of THOR-OS "ONE MAN ARMY" Ultimate Implementation
"""

import asyncio
import json
import logging
import signal
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import threading
import time

# Import all THOR systems
try:
    from thor_gamer_os_core import THORRepoManager, TreeWateringEasterEgg
    from thor_p2p_cloud_system import THORPeerToPeer, THORGamerOSP2PIntegration
    from thor_sync_ui_system import THORSyncUI, launch_sync_ui
    from thor_ai_content_creator import AIContentCreator, THORAIContentIntegration
    from thor_driver_template_system import THORDriverManager, THORDriverIntegration
    from thor_os_universal_game_tracker import UniversalGameTracker
    from thor_kb_gaming_knowledgebase import THORGamingKnowledgebase
    from thor_os_complete import THOROSCore
    from thor_os_tabby_ml import THORTabbyML
    from thor_os_monitor import THORSystemMonitor
except ImportError as e:
    print(f"Warning: Some THOR modules not available: {e}")

class THORGamerOSUnified:
    """Main THOR Gamer OS unified platform"""
    
    def __init__(self, data_dir: str = "thor_unified_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # System state
        self.running = False
        self.systems_initialized = False
        self.logger = self._setup_logging()
        
        # Core systems
        self.repo_manager = None
        self.p2p_system = None
        self.ai_content_creator = None
        self.driver_manager = None
        self.game_tracker = None
        self.knowledge_base = None
        self.system_monitor = None
        self.tabby_ml = None
        self.core_os = None
        
        # UI system
        self.sync_ui = None
        self.ui_thread = None
        
        # Easter egg system
        self.tree_watering = TreeWateringEasterEgg()
        
        # System metrics
        self.metrics = {
            'start_time': None,
            'repos_managed': 0,
            'files_synced': 0,
            'peers_connected': 0,
            'content_generated': 0,
            'games_tracked': 0,
            'knowledge_queries': 0,
            'tree_water_count': 0
        }
        
        # Shutdown handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _setup_logging(self) -> logging.Logger:
        """Setup unified logging system"""
        logger = logging.getLogger('thor_gamer_os_unified')
        logger.setLevel(logging.INFO)
        
        # File handler
        file_handler = logging.FileHandler(self.data_dir / 'thor_gamer_os.log')
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    async def initialize_all_systems(self) -> Dict[str, Any]:
        """Initialize all THOR systems"""
        init_results = {}
        
        try:
            self.logger.info("🚀 Initializing THOR Gamer OS Unified Platform...")
            
            # Initialize core repository manager
            self.logger.info("📁 Initializing Repository Manager...")
            self.repo_manager = THORRepoManager(str(self.data_dir / "repos"))
            init_results['repo_manager'] = True
            
            # Initialize P2P system
            self.logger.info("🌐 Initializing P2P Cloud System...")
            p2p_integration = THORGamerOSP2PIntegration(str(self.data_dir))
            p2p_result = await p2p_integration.initialize_p2p_gaming()
            self.p2p_system = p2p_integration.p2p_system
            init_results['p2p_system'] = p2p_result
            
            # Initialize AI Content Creator
            self.logger.info("🤖 Initializing AI Content Creator...")
            content_integration = THORAIContentIntegration(str(self.data_dir))
            self.ai_content_creator = content_integration.content_creator
            init_results['ai_content_creator'] = True
            
            # Initialize Driver Manager
            self.logger.info("🔧 Initializing Driver Management System...")
            driver_integration = THORDriverIntegration(str(self.data_dir))
            driver_result = await driver_integration.initialize_driver_system()
            self.driver_manager = driver_integration.driver_manager
            init_results['driver_manager'] = driver_result
            
            # Initialize Game Tracker
            self.logger.info("🎮 Initializing Universal Game Tracker...")
            self.game_tracker = UniversalGameTracker(str(self.data_dir / "game_tracking"))
            await self.game_tracker.initialize()
            init_results['game_tracker'] = True
            
            # Initialize Gaming Knowledge Base
            self.logger.info("📚 Initializing Gaming Knowledge Base...")
            self.knowledge_base = THORGamingKnowledgebase(str(self.data_dir / "knowledge"))
            await self.knowledge_base.initialize()
            init_results['knowledge_base'] = True
            
            # Initialize System Monitor
            self.logger.info("📊 Initializing System Monitor...")
            self.system_monitor = THORSystemMonitor(str(self.data_dir / "monitoring"))
            await self.system_monitor.start_monitoring()
            init_results['system_monitor'] = True
            
            # Initialize Tabby ML
            self.logger.info("🧠 Initializing Tabby ML System...")
            self.tabby_ml = THORTabbyML(str(self.data_dir / "ml"))
            await self.tabby_ml.initialize()
            init_results['tabby_ml'] = True
            
            # Initialize Core OS
            self.logger.info("⚡ Initializing THOR Core OS...")
            self.core_os = THOROSCore(str(self.data_dir / "core"))
            await self.core_os.initialize()
            init_results['core_os'] = True
            
            self.systems_initialized = True
            self.metrics['start_time'] = datetime.now()
            
            self.logger.info("✅ All THOR systems initialized successfully!")
            
            # Start cross-system communication
            asyncio.create_task(self._system_coordinator())
            
            return init_results
            
        except Exception as e:
            self.logger.error(f"❌ System initialization failed: {str(e)}")
            init_results['error'] = str(e)
            return init_results
    
    async def launch_ui(self):
        """Launch the THOR Sync UI"""
        try:
            self.logger.info("🎨 Launching THOR Sync UI...")
            
            # Create and launch UI
            self.sync_ui = THORSyncUI(self.repo_manager, self.p2p_system)
            
            # Load repositories into UI
            repos = await self.repo_manager.get_repositories()
            repo_data = [{'name': repo.name, 'repo_id': repo.repo_id} for repo in repos]
            self.sync_ui.load_repositories(repo_data)
            
            # Launch UI in separate thread
            self.ui_thread = await launch_sync_ui(self.repo_manager, self.p2p_system)
            
            self.logger.info("✅ THOR Sync UI launched successfully!")
            
        except Exception as e:
            self.logger.error(f"❌ UI launch failed: {str(e)}")
    
    async def _system_coordinator(self):
        """Coordinate communication between all systems"""
        while self.running:
            try:
                # Update metrics
                await self._update_system_metrics()
                
                # Cross-system data synchronization
                await self._sync_cross_system_data()
                
                # Health monitoring
                await self._monitor_system_health()
                
                # AI-driven optimizations
                await self._ai_system_optimization()
                
                await asyncio.sleep(30)  # Run every 30 seconds
                
            except Exception as e:
                self.logger.error(f"System coordinator error: {str(e)}")
                await asyncio.sleep(10)
    
    async def _update_system_metrics(self):
        """Update system-wide metrics"""
        try:
            if self.repo_manager:
                repos = await self.repo_manager.get_repositories()
                self.metrics['repos_managed'] = len(repos)
            
            if self.p2p_system:
                status = self.p2p_system.get_network_status()
                self.metrics['peers_connected'] = status.get('active_connections', 0)
            
            if self.game_tracker:
                sessions = await self.game_tracker.get_recent_sessions()
                self.metrics['games_tracked'] = len(sessions)
            
            if self.ai_content_creator:
                library = self.ai_content_creator.get_content_library()
                self.metrics['content_generated'] = len(library)
            
            # Update tree watering count
            self.metrics['tree_water_count'] = self.tree_watering.water_count
            
        except Exception as e:
            self.logger.error(f"Metrics update error: {str(e)}")
    
    async def _sync_cross_system_data(self):
        """Synchronize data between systems"""
        try:
            # Sync game data between tracker and knowledge base
            if self.game_tracker and self.knowledge_base:
                recent_games = await self.game_tracker.get_recent_games()
                for game in recent_games:
                    await self.knowledge_base.update_game_activity(game)
            
            # Sync AI content with repository manager
            if self.ai_content_creator and self.repo_manager:
                # Auto-suggest content creation for new repos
                repos = await self.repo_manager.get_repositories()
                for repo in repos:
                    # Check if repo needs content generation
                    changes = await self.repo_manager.scan_repo_changes(repo.repo_id)
                    if changes.get('total_changes', 0) > 5:
                        # Suggest content creation
                        pass  # Implementation would go here
            
        except Exception as e:
            self.logger.error(f"Cross-system sync error: {str(e)}")
    
    async def _monitor_system_health(self):
        """Monitor health of all systems"""
        try:
            health_status = {}
            
            # Check each system
            systems = {
                'repo_manager': self.repo_manager,
                'p2p_system': self.p2p_system,
                'ai_content_creator': self.ai_content_creator,
                'driver_manager': self.driver_manager,
                'game_tracker': self.game_tracker,
                'knowledge_base': self.knowledge_base,
                'system_monitor': self.system_monitor,
                'tabby_ml': self.tabby_ml,
                'core_os': self.core_os
            }
            
            for name, system in systems.items():
                if system:
                    health_status[name] = 'healthy'
                else:
                    health_status[name] = 'offline'
                    self.logger.warning(f"System {name} is offline")
            
            # Log overall health
            healthy_count = sum(1 for status in health_status.values() if status == 'healthy')
            total_count = len(health_status)
            
            if healthy_count == total_count:
                self.logger.info(f"🟢 All systems healthy ({healthy_count}/{total_count})")
            else:
                self.logger.warning(f"🟡 System health: {healthy_count}/{total_count} healthy")
            
        except Exception as e:
            self.logger.error(f"Health monitoring error: {str(e)}")
    
    async def _ai_system_optimization(self):
        """AI-driven system optimizations"""
        try:
            # Optimize based on usage patterns
            if self.system_monitor and self.ai_content_creator:
                # Check system performance
                performance = await self.system_monitor.get_performance_metrics()
                
                # AI suggestions for optimization
                if performance.get('cpu_usage', 0) > 80:
                    self.logger.info("🧠 AI suggests reducing background tasks")
                
                if performance.get('memory_usage', 0) > 85:
                    self.logger.info("🧠 AI suggests clearing cache and temporary files")
            
        except Exception as e:
            self.logger.error(f"AI optimization error: {str(e)}")
    
    async def create_sample_content(self):
        """Create sample content to demonstrate the system"""
        try:
            self.logger.info("🎨 Creating sample content...")
            
            # Create sample repository
            sample_repo = await self.repo_manager.create_repository(
                name="THOR Gaming Demo Project",
                path=str(self.data_dir / "sample_repo")
            )
            
            # Create sample files
            sample_files = [
                ("game_config.json", '{"name": "THOR Demo Game", "version": "1.0"}'),
                ("player_stats.py", "# Player statistics tracking\nclass PlayerStats:\n    pass"),
                ("README.md", "# THOR Gaming Demo\n\nA sample gaming project for THOR OS.")
            ]
            
            for filename, content in sample_files:
                file_path = Path(sample_repo.path) / filename
                file_path.write_text(content)
            
            # Generate AI content for the project
            if self.ai_content_creator:
                content_integration = THORAIContentIntegration(str(self.data_dir))
                content_pack = await content_integration.create_gaming_content_pack(
                    "THOR Demo Game", 
                    ['overview', 'beginner_guide', 'character_showcase']
                )
                self.logger.info(f"Generated content pack: {len(content_pack['contents'])} items")
            
            # Water the tree!
            tree_message = self.tree_watering.water_tree()
            self.logger.info(f"🌱 {tree_message}")
            
            self.logger.info("✅ Sample content created successfully!")
            
        except Exception as e:
            self.logger.error(f"Sample content creation failed: {str(e)}")
    
    async def run_full_demo(self):
        """Run a complete demonstration of all systems"""
        try:
            self.logger.info("🎯 Starting THOR Gamer OS Full Demo...")
            
            # Initialize all systems
            init_results = await self.initialize_all_systems()
            self.logger.info(f"Initialization results: {init_results}")
            
            # Create sample content
            await self.create_sample_content()
            
            # Launch UI
            await self.launch_ui()
            
            # Demo P2P functionality
            if self.p2p_system:
                self.logger.info("🌐 Starting P2P network discovery...")
                await asyncio.sleep(5)  # Wait for peer discovery
                
                network_status = self.p2p_system.get_network_status()
                self.logger.info(f"P2P Network Status: {network_status}")
            
            # Demo game tracking
            if self.game_tracker:
                self.logger.info("🎮 Demonstrating game tracking...")
                # In a real scenario, this would track actual games
                await self.game_tracker.start_session_tracking()
            
            # Demo knowledge base
            if self.knowledge_base:
                self.logger.info("📚 Testing knowledge base...")
                # Test search functionality
                search_results = await self.knowledge_base.search_content("THOR gaming tips")
                self.logger.info(f"Knowledge search results: {len(search_results)} items found")
            
            self.logger.info("🎉 THOR Gamer OS Full Demo completed!")
            
        except Exception as e:
            self.logger.error(f"Demo failed: {str(e)}")
    
    async def start(self):
        """Start the complete THOR Gamer OS platform"""
        self.running = True
        
        try:
            # Print banner
            self._print_thor_banner()
            
            # Run full demo
            await self.run_full_demo()
            
            # Keep running
            self.logger.info("🚀 THOR Gamer OS is now running...")
            self.logger.info("🌱 Water your tree by syncing your repositories!")
            self.logger.info("Press Ctrl+C to stop")
            
            while self.running:
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            self.logger.info("🛑 Shutdown requested by user")
        except Exception as e:
            self.logger.error(f"💥 Critical error: {str(e)}")
        finally:
            await self.shutdown()
    
    def _print_thor_banner(self):
        """Print THOR Gamer OS banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                    🌱 THOR GAMER OS 🌱                       ║
║              Unified Developer & Gamer Platform              ║
║                                                              ║
║  🎮 Game Tracking    📁 Repository Sync    🤖 AI Content    ║
║  🌐 P2P Sharing      📚 Knowledge Base     🔧 Driver Mgmt   ║
║  ⚡ Performance      🧠 Machine Learning   🎨 UI Interface   ║
║                                                              ║
║              "Water your tree, grow your code"              ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    async def shutdown(self):
        """Shutdown all THOR systems gracefully"""
        self.running = False
        
        self.logger.info("🛑 Shutting down THOR Gamer OS...")
        
        # Stop all systems
        shutdown_tasks = []
        
        if self.p2p_system:
            shutdown_tasks.append(self.p2p_system.stop())
        
        if self.game_tracker:
            shutdown_tasks.append(self.game_tracker.stop_tracking())
        
        if self.system_monitor:
            shutdown_tasks.append(self.system_monitor.stop_monitoring())
        
        # Wait for all shutdowns
        if shutdown_tasks:
            await asyncio.gather(*shutdown_tasks, return_exceptions=True)
        
        # Final metrics
        uptime = datetime.now() - self.metrics['start_time'] if self.metrics['start_time'] else None
        
        self.logger.info("📊 Final Statistics:")
        self.logger.info(f"   Uptime: {uptime}")
        self.logger.info(f"   Repositories: {self.metrics['repos_managed']}")
        self.logger.info(f"   Files Synced: {self.metrics['files_synced']}")
        self.logger.info(f"   P2P Connections: {self.metrics['peers_connected']}")
        self.logger.info(f"   Content Generated: {self.metrics['content_generated']}")
        self.logger.info(f"   Games Tracked: {self.metrics['games_tracked']}")
        self.logger.info(f"   Tree Watered: {self.metrics['tree_water_count']} times")
        
        self.logger.info("🌱 THOR Gamer OS shutdown complete. Your tree will keep growing!")
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.logger.info(f"Received signal {signum}")
        self.running = False
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get complete system status"""
        return {
            'running': self.running,
            'systems_initialized': self.systems_initialized,
            'metrics': self.metrics,
            'tree_status': self.tree_watering.get_tree_status(),
            'components': {
                'repo_manager': self.repo_manager is not None,
                'p2p_system': self.p2p_system is not None,
                'ai_content_creator': self.ai_content_creator is not None,
                'driver_manager': self.driver_manager is not None,
                'game_tracker': self.game_tracker is not None,
                'knowledge_base': self.knowledge_base is not None,
                'system_monitor': self.system_monitor is not None,
                'tabby_ml': self.tabby_ml is not None,
                'core_os': self.core_os is not None,
                'sync_ui': self.sync_ui is not None
            }
        }

# Quick launcher functions
async def quick_start_thor_gamer_os():
    """Quick start function for THOR Gamer OS"""
    thor_os = THORGamerOSUnified()
    await thor_os.start()

def launch_thor_gamer_os():
    """Launch THOR Gamer OS in new event loop"""
    try:
        asyncio.run(quick_start_thor_gamer_os())
    except KeyboardInterrupt:
        print("\n🌱 THOR Gamer OS stopped. Keep growing!")

async def main():
    """Main entry point"""
    thor_os = THORGamerOSUnified()
    await thor_os.start()

if __name__ == "__main__":
    launch_thor_gamer_os()
