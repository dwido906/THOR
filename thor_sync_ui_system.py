#!/usr/bin/env python3
"""
THOR Gamer OS Sync UI System - "Watering the Tree" Interface
Part of THOR Gamer OS Unified Platform

Features:
- Interactive sync/upload interface
- File selection with AI recommendations
- Progress tracking and status updates
- Easter egg "watering the tree" implementation
- Destination selection (cloud, P2P, storage)

Created as part of THOR-OS "ONE MAN ARMY" Ultimate Implementation
"""

import asyncio
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from pathlib import Path
import logging
from dataclasses import dataclass
import time
import random

@dataclass
class UITheme:
    """THOR Gamer OS UI Theme"""
    primary_color: str = "#1e1e2e"
    secondary_color: str = "#313244"
    accent_color: str = "#89b4fa"
    success_color: str = "#a6e3a1"
    warning_color: str = "#f9e2af"
    error_color: str = "#f38ba8"
    text_color: str = "#cdd6f4"
    button_color: str = "#45475a"
    hover_color: str = "#585b70"

class TreeWateringAnimation:
    """Animated tree watering system for UI"""
    
    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.animation_running = False
        self.water_drops = []
        self.tree_growth_stage = 0
        
        # Tree growth stages
        self.tree_stages = [
            "🌱",  # Seed
            "🌿",  # Sprout
            "🪴",  # Small plant
            "🌳",  # Tree
            "🌲",  # Tall tree
            "🎋"   # Forest
        ]
        
        # Easter egg messages
        self.easter_messages = [
            "🌱 The tree never minds, water is water.",
            "💧 You've turned a pissed-on situation into growth. Water your tree!",
            "🌳 Every drop of knowledge feeds the forest of innovation.",
            "🚀 From humble seeds grow mighty trees of code.",
            "🎮 Your commits are the water, your repo is the tree."
        ]
        
        self.easter_egg_triggered = False
    
    def start_watering_animation(self):
        """Start the tree watering animation"""
        self.animation_running = True
        self._animate_water_drops()
        self._grow_tree()
    
    def _animate_water_drops(self):
        """Animate water drops falling"""
        if not self.animation_running:
            return
        
        # Create new water drop
        drop = {
            'x': random.randint(50, 150),
            'y': 10,
            'id': self.canvas.create_oval(0, 0, 6, 10, fill='#89b4fa', outline='')
        }
        self.water_drops.append(drop)
        
        # Animate existing drops
        for drop in self.water_drops[:]:
            drop['y'] += 3
            self.canvas.coords(drop['id'], drop['x'], drop['y'], drop['x']+6, drop['y']+10)
            
            # Remove drops that hit the ground
            if drop['y'] > 180:
                self.canvas.delete(drop['id'])
                self.water_drops.remove(drop)
                self._splash_effect(drop['x'])
        
        # Schedule next frame
        if self.animation_running:
            self.canvas.after(50, self._animate_water_drops)
    
    def _splash_effect(self, x: int):
        """Create splash effect when water hits ground"""
        splash = self.canvas.create_text(x, 180, text="💦", font=("Arial", 8))
        self.canvas.after(500, lambda: self.canvas.delete(splash))
    
    def _grow_tree(self):
        """Grow the tree gradually"""
        if self.tree_growth_stage < len(self.tree_stages) - 1:
            self.tree_growth_stage += 1
            
        # Update tree display
        tree_emoji = self.tree_stages[self.tree_growth_stage]
        self.canvas.delete("tree")
        self.canvas.create_text(100, 160, text=tree_emoji, font=("Arial", 24), tags="tree")
        
        # Add growth message
        if self.tree_growth_stage == len(self.tree_stages) - 1:
            self.canvas.create_text(100, 200, text="Forest of Knowledge!", font=("Arial", 10), fill=self.easter_messages[0])
    
    def trigger_easter_egg(self) -> str:
        """Trigger the hidden easter egg"""
        self.easter_egg_triggered = True
        return random.choice(self.easter_messages)
    
    def stop_animation(self):
        """Stop the watering animation"""
        self.animation_running = False

class FileSelectionFrame(ttk.Frame):
    """File selection interface with AI recommendations"""
    
    def __init__(self, parent, on_selection_change: Callable = None):
        super().__init__(parent)
        self.on_selection_change = on_selection_change
        self.file_vars: Dict[str, tk.BooleanVar] = {}
        self.ai_recommendations: Dict[str, bool] = {}
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create file selection widgets"""
        # Header
        header_frame = ttk.Frame(self)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header_frame, text="Select files to sync:", 
                 font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        
        ttk.Button(header_frame, text="Select All", 
                  command=self._select_all).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(header_frame, text="AI Recommended", 
                  command=self._select_ai_recommended).pack(side=tk.RIGHT)
        
        # File list with scrollbar
        list_frame = ttk.Frame(self)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.file_listbox = tk.Listbox(list_frame, selectmode=tk.MULTIPLE,
                                      font=("Consolas", 10))
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, 
                                 command=self.file_listbox.yview)
        self.file_listbox.config(yscrollcommand=scrollbar.set)
        
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # File details frame
        self.details_frame = ttk.Frame(self)
        self.details_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.details_label = ttk.Label(self.details_frame, text="Select files to see details")
        self.details_label.pack()
    
    def update_file_list(self, files: List[Dict[str, Any]]):
        """Update the file list with new files"""
        self.file_listbox.delete(0, tk.END)
        self.file_vars.clear()
        self.ai_recommendations.clear()
        
        for file_info in files:
            file_path = file_info['path']
            ai_recommended = file_info.get('ai_recommended', False)
            change_type = file_info.get('change_type', 'unknown')
            
            # Create display text
            if ai_recommended:
                display_text = f"✨ {file_path} [{change_type}] - THOR recommends"
            else:
                display_text = f"   {file_path} [{change_type}]"
            
            self.file_listbox.insert(tk.END, display_text)
            
            # Store recommendation
            self.ai_recommendations[file_path] = ai_recommended
            
            # Create variable for checkbox-like behavior
            var = tk.BooleanVar(value=ai_recommended)
            var.trace('w', self._on_selection_change)
            self.file_vars[file_path] = var
        
        # Bind selection events
        self.file_listbox.bind('<<ListboxSelect>>', self._on_listbox_select)
    
    def _on_listbox_select(self, event):
        """Handle listbox selection"""
        selection = self.file_listbox.curselection()
        if selection:
            # Toggle selection for clicked items
            for index in selection:
                file_path = list(self.file_vars.keys())[index]
                current_value = self.file_vars[file_path].get()
                self.file_vars[file_path].set(not current_value)
    
    def _on_selection_change(self, *args):
        """Handle selection change"""
        selected_count = sum(1 for var in self.file_vars.values() if var.get())
        self.details_label.config(text=f"Selected: {selected_count} files")
        
        if self.on_selection_change:
            self.on_selection_change(self.get_selected_files())
    
    def _select_all(self):
        """Select all files"""
        for var in self.file_vars.values():
            var.set(True)
    
    def _select_ai_recommended(self):
        """Select only AI recommended files"""
        for file_path, var in self.file_vars.items():
            var.set(self.ai_recommendations.get(file_path, False))
    
    def get_selected_files(self) -> List[str]:
        """Get list of selected files"""
        return [path for path, var in self.file_vars.items() if var.get()]

class DestinationFrame(ttk.Frame):
    """Destination selection interface"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.destination_var = tk.StringVar(value="thor_cloud")
        self._create_widgets()
    
    def _create_widgets(self):
        """Create destination selection widgets"""
        ttk.Label(self, text="Destination:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        
        # Destination options
        destinations = [
            ("THOR Cloud Node", "thor_cloud", "🌐 Secure THOR cloud storage"),
            ("Peer Network", "peer", "👥 Share with THOR peers"),
            ("S3 Compatible", "s3", "☁️ Amazon S3 or compatible"),
            ("IPFS Network", "ipfs", "🌍 Decentralized IPFS storage"),
            ("Local Backup", "local", "💾 Local backup copy")
        ]
        
        for name, value, description in destinations:
            frame = ttk.Frame(self)
            frame.pack(fill=tk.X, pady=2)
            
            ttk.Radiobutton(frame, text=name, variable=self.destination_var, 
                           value=value).pack(side=tk.LEFT)
            ttk.Label(frame, text=description, font=("Arial", 9)).pack(side=tk.LEFT, padx=(10, 0))
    
    def get_destination(self) -> str:
        """Get selected destination"""
        return self.destination_var.get()

class ProgressFrame(ttk.Frame):
    """Progress tracking interface"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Ready to sync")
        self._create_widgets()
    
    def _create_widgets(self):
        """Create progress widgets"""
        # Progress bar
        self.progress_bar = ttk.Progressbar(self, variable=self.progress_var, 
                                           maximum=100, mode='determinate')
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))
        
        # Status label
        self.status_label = ttk.Label(self, textvariable=self.status_var)
        self.status_label.pack(anchor=tk.W)
        
        # Activity log
        log_frame = ttk.Frame(self)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        ttk.Label(log_frame, text="Activity Log:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        self.log_text = tk.Text(log_frame, height=6, font=("Consolas", 9))
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.config(yscrollcommand=log_scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def update_progress(self, progress: float, status: str):
        """Update progress and status"""
        self.progress_var.set(progress)
        self.status_var.set(status)
    
    def add_log_entry(self, message: str):
        """Add entry to activity log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)

class THORSyncUI:
    """Main THOR Sync/Upload UI System"""
    
    def __init__(self, repo_manager=None, p2p_system=None):
        self.repo_manager = repo_manager
        self.p2p_system = p2p_system
        
        # UI state
        self.selected_repo_id = None
        self.current_files = []
        self.sync_in_progress = False
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("THOR Gamer OS - Water Your Tree 🌱")
        self.root.geometry("800x700")
        self.root.configure(bg=UITheme.primary_color)
        
        # Apply theme
        self._setup_theme()
        
        # Create widgets
        self._create_widgets()
        
        # Easter egg setup
        self.easter_egg = TreeWateringAnimation(self.tree_canvas)
        self.easter_egg_pixel = None
        
        # Setup easter egg pixel
        self._setup_easter_egg()
    
    def _setup_theme(self):
        """Setup THOR Gamer OS theme"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('THOR.TFrame', background=UITheme.primary_color)
        style.configure('THOR.TLabel', background=UITheme.primary_color, 
                       foreground=UITheme.text_color)
        style.configure('THOR.TButton', background=UITheme.button_color,
                       foreground=UITheme.text_color)
        style.map('THOR.TButton', background=[('active', UITheme.hover_color)])
    
    def _create_widgets(self):
        """Create main UI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, style='THOR.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title and tree animation
        self._create_header(main_frame)
        
        # Repository selection
        self._create_repo_selection(main_frame)
        
        # File selection
        self._create_file_selection(main_frame)
        
        # Destination selection
        self._create_destination_selection(main_frame)
        
        # Action buttons
        self._create_action_buttons(main_frame)
        
        # Progress tracking
        self._create_progress_section(main_frame)
    
    def _create_header(self, parent):
        """Create header with title and tree animation"""
        header_frame = ttk.Frame(parent, style='THOR.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title
        title_frame = ttk.Frame(header_frame, style='THOR.TFrame')
        title_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(title_frame, text="🌱 Water Your Tree", 
                               font=("Arial", 18, "bold"), style='THOR.TLabel')
        title_label.pack(anchor=tk.W)
        
        subtitle_label = ttk.Label(title_frame, text="THOR Gamer OS Repository Sync", 
                                  font=("Arial", 12), style='THOR.TLabel')
        subtitle_label.pack(anchor=tk.W)
        
        # Tree animation canvas
        self.tree_canvas = tk.Canvas(header_frame, width=200, height=220, 
                                    bg=UITheme.primary_color, highlightthickness=0)
        self.tree_canvas.pack(side=tk.RIGHT)
        
        # Initial tree
        self.tree_canvas.create_text(100, 160, text="🌱", font=("Arial", 24), tags="tree")
        self.tree_canvas.create_text(100, 190, text="Ready to grow!", font=("Arial", 10))
    
    def _create_repo_selection(self, parent):
        """Create repository selection section"""
        repo_frame = ttk.LabelFrame(parent, text="Repository", style='THOR.TFrame')
        repo_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Repository dropdown
        repo_select_frame = ttk.Frame(repo_frame, style='THOR.TFrame')
        repo_select_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(repo_select_frame, text="Select Repository:", 
                 style='THOR.TLabel').pack(side=tk.LEFT)
        
        self.repo_var = tk.StringVar()
        self.repo_combo = ttk.Combobox(repo_select_frame, textvariable=self.repo_var,
                                      state="readonly", width=40)
        self.repo_combo.pack(side=tk.LEFT, padx=(10, 0))
        self.repo_combo.bind('<<ComboboxSelected>>', self._on_repo_selected)
        
        ttk.Button(repo_select_frame, text="Scan Changes", 
                  command=self._scan_repo_changes).pack(side=tk.RIGHT)
    
    def _create_file_selection(self, parent):
        """Create file selection section"""
        file_frame = ttk.LabelFrame(parent, text="Files to Sync", style='THOR.TFrame')
        file_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.file_selection = FileSelectionFrame(file_frame, self._on_file_selection_change)
        self.file_selection.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    def _create_destination_selection(self, parent):
        """Create destination selection section"""
        dest_frame = ttk.LabelFrame(parent, text="Sync Destination", style='THOR.TFrame')
        dest_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.destination_selection = DestinationFrame(dest_frame)
        self.destination_selection.pack(fill=tk.X, padx=10, pady=5)
    
    def _create_action_buttons(self, parent):
        """Create action buttons"""
        button_frame = ttk.Frame(parent, style='THOR.TFrame')
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Sync button
        self.sync_button = ttk.Button(button_frame, text="💧 Sync Now / Water the Tree", 
                                     command=self._start_sync, style='THOR.TButton')
        self.sync_button.pack(side=tk.LEFT)
        
        # Schedule button
        ttk.Button(button_frame, text="⏰ Schedule", 
                  command=self._schedule_sync, style='THOR.TButton').pack(side=tk.LEFT, padx=(10, 0))
        
        # Stop button
        self.stop_button = ttk.Button(button_frame, text="⏹️ Stop", 
                                     command=self._stop_sync, state=tk.DISABLED, 
                                     style='THOR.TButton')
        self.stop_button.pack(side=tk.RIGHT)
    
    def _create_progress_section(self, parent):
        """Create progress tracking section"""
        progress_frame = ttk.LabelFrame(parent, text="Sync Progress", style='THOR.TFrame')
        progress_frame.pack(fill=tk.X)
        
        self.progress_tracking = ProgressFrame(progress_frame)
        self.progress_tracking.pack(fill=tk.X, padx=10, pady=5)
    
    def _setup_easter_egg(self):
        """Setup the hidden easter egg pixel"""
        # Create tiny invisible button in bottom-right corner
        self.easter_egg_pixel = tk.Button(self.root, text="", width=1, height=1,
                                         bd=0, bg=UITheme.primary_color, 
                                         activebackground=UITheme.primary_color,
                                         command=self._trigger_easter_egg)
        self.easter_egg_pixel.place(x=780, y=670)
    
    def _trigger_easter_egg(self):
        """Trigger the hidden easter egg"""
        message = self.easter_egg.trigger_easter_egg()
        
        # Show easter egg message
        easter_window = tk.Toplevel(self.root)
        easter_window.title("🌱 Tree Wisdom")
        easter_window.geometry("400x200")
        easter_window.configure(bg=UITheme.success_color)
        
        easter_label = tk.Label(easter_window, text=message, 
                               font=("Arial", 14, "bold"),
                               bg=UITheme.success_color, fg=UITheme.primary_color,
                               wraplength=350)
        easter_label.pack(expand=True)
        
        # Auto-close after 5 seconds
        easter_window.after(5000, easter_window.destroy)
        
        # Start tree animation
        self.easter_egg.start_watering_animation()
    
    def _on_repo_selected(self, event):
        """Handle repository selection"""
        repo_name = self.repo_var.get()
        # In real implementation, get repo_id from repo_name
        self.selected_repo_id = repo_name  # Simplified
        self._scan_repo_changes()
    
    def _scan_repo_changes(self):
        """Scan repository for changes"""
        if not self.selected_repo_id:
            messagebox.showwarning("Warning", "Please select a repository first")
            return
        
        self.progress_tracking.add_log_entry("Scanning repository for changes...")
        
        # Simulate scanning (in real implementation, use repo_manager)
        self.root.after(1000, self._update_file_list_demo)
    
    def _update_file_list_demo(self):
        """Update file list with demo data"""
        # Demo file data
        demo_files = [
            {'path': 'src/main.py', 'change_type': 'modified', 'ai_recommended': True},
            {'path': 'config/settings.json', 'change_type': 'modified', 'ai_recommended': True},
            {'path': 'assets/player.png', 'change_type': 'new', 'ai_recommended': True},
            {'path': 'temp/cache.tmp', 'change_type': 'new', 'ai_recommended': False},
            {'path': 'README.md', 'change_type': 'modified', 'ai_recommended': True},
            {'path': 'logs/debug.log', 'change_type': 'modified', 'ai_recommended': False},
        ]
        
        self.current_files = demo_files
        self.file_selection.update_file_list(demo_files)
        
        self.progress_tracking.add_log_entry(f"Found {len(demo_files)} changed files")
        self.progress_tracking.add_log_entry("THOR AI suggests syncing 4 recommended files")
    
    def _on_file_selection_change(self, selected_files: List[str]):
        """Handle file selection change"""
        if selected_files:
            self.progress_tracking.add_log_entry(f"Selected {len(selected_files)} files for sync")
    
    def _start_sync(self):
        """Start the sync operation"""
        if self.sync_in_progress:
            return
        
        selected_files = self.file_selection.get_selected_files()
        if not selected_files:
            messagebox.showwarning("Warning", "Please select files to sync")
            return
        
        destination = self.destination_selection.get_destination()
        
        self.sync_in_progress = True
        self.sync_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # Start sync animation
        self.easter_egg.start_watering_animation()
        
        # Start sync process in background
        sync_thread = threading.Thread(target=self._sync_worker, 
                                      args=(selected_files, destination))
        sync_thread.daemon = True
        sync_thread.start()
    
    def _sync_worker(self, files: List[str], destination: str):
        """Background sync worker"""
        try:
            total_files = len(files)
            
            for i, file_path in enumerate(files):
                if not self.sync_in_progress:
                    break
                
                # Simulate file sync
                progress = ((i + 1) / total_files) * 100
                status = f"Syncing {file_path} to {destination}..."
                
                # Update UI in main thread
                self.root.after(0, lambda p=progress, s=status: self.progress_tracking.update_progress(p, s))
                self.root.after(0, lambda f=file_path: self.progress_tracking.add_log_entry(f"✅ Synced: {f}"))
                
                # Simulate network delay
                time.sleep(0.5)
            
            if self.sync_in_progress:
                # Sync completed
                self.root.after(0, lambda: self.progress_tracking.update_progress(100, "Sync completed successfully!"))
                self.root.after(0, lambda: self.progress_tracking.add_log_entry("🌱 Tree watered successfully! Your code is growing!"))
                
                # Show completion message
                self.root.after(0, self._show_sync_complete)
        
        except Exception as e:
            self.root.after(0, lambda: self.progress_tracking.add_log_entry(f"❌ Sync failed: {str(e)}"))
        
        finally:
            self.root.after(0, self._sync_finished)
    
    def _show_sync_complete(self):
        """Show sync completion message"""
        messagebox.showinfo("Sync Complete", 
                           "🌱 Your tree has been watered!\n\nFiles synced successfully to the THOR network.")
    
    def _sync_finished(self):
        """Handle sync completion"""
        self.sync_in_progress = False
        self.sync_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.easter_egg.stop_animation()
    
    def _stop_sync(self):
        """Stop the sync operation"""
        self.sync_in_progress = False
        self.progress_tracking.add_log_entry("Sync operation stopped by user")
    
    def _schedule_sync(self):
        """Schedule a sync operation"""
        messagebox.showinfo("Schedule Sync", "Sync scheduling will be available in the next update!")
    
    def load_repositories(self, repositories: List[Dict[str, Any]]):
        """Load repositories into the dropdown"""
        repo_names = [repo['name'] for repo in repositories]
        self.repo_combo['values'] = repo_names
        
        if repo_names:
            self.repo_combo.set(repo_names[0])
    
    def run(self):
        """Run the UI"""
        # Load demo repositories
        demo_repos = [
            {'name': 'My Game Project', 'repo_id': 'repo_1'},
            {'name': 'THOR Mods Collection', 'repo_id': 'repo_2'},
            {'name': 'Gaming Assets Library', 'repo_id': 'repo_3'}
        ]
        self.load_repositories(demo_repos)
        
        # Start the UI
        self.root.mainloop()

# Integration function for THOR Gamer OS
async def launch_sync_ui(repo_manager=None, p2p_system=None):
    """Launch the THOR Sync UI"""
    def run_ui():
        ui = THORSyncUI(repo_manager, p2p_system)
        ui.run()
    
    # Run UI in separate thread to avoid blocking async operations
    ui_thread = threading.Thread(target=run_ui)
    ui_thread.daemon = True
    ui_thread.start()
    
    return ui_thread

async def main():
    """Example usage of THOR Sync UI"""
    ui = THORSyncUI()
    ui.run()

if __name__ == "__main__":
    asyncio.run(main())
