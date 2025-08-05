#!/usr/bin/env python3
"""
SIMS-Style UI/UX Design Tool for THOR-AI
A love note to your girlfriend ❤️

This creates a Sims 4-like drag and drop interface for designing
beautiful UI/UX for THOR-AI websites and communities.
Uses Tailwind CSS lifetime subscription elements.

"Building dreams together, one design at a time" 💕
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
import json
import os
from pathlib import Path
import uuid
import time
from datetime import datetime
import threading
import webbrowser
import tempfile

class SimsStyleDesignTool:
    """Sims 4-inspired UI/UX design tool"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("THOR-AI Design Studio - For My Beautiful Girlfriend ❤️")
        self.root.geometry("1800x1000")
        self.root.configure(bg='#2D1B69')  # Deep purple like Sims
        
        # Design data
        self.current_design = {
            'name': 'Untitled Design',
            'elements': [],
            'theme': 'purple_dreams',
            'created_by': 'My Amazing Girlfriend 💕',
            'created_at': datetime.now().isoformat()
        }
        
        # Available elements (Tailwind CSS powered)
        self.element_library = self._load_element_library()
        
        # Canvas for design
        self.canvas_elements = []
        self.selected_element = None
        
        # Initialize UI
        self._create_ui()
        
        print("💕 THOR-AI Design Studio opened for the most talented designer")
        print("🎨 Ready to create beautiful UI/UX designs!")
    
    def _load_element_library(self):
        """Load Tailwind CSS element library"""
        return {
            'layout': [
                {
                    'name': 'Hero Section',
                    'icon': '🌟',
                    'description': 'Beautiful hero section with gradient',
                    'html': '''
                    <div class="bg-gradient-to-r from-purple-400 via-pink-500 to-red-500 text-white py-20 px-8 rounded-lg">
                        <h1 class="text-5xl font-bold mb-4">Welcome to Our Community</h1>
                        <p class="text-xl mb-8">Build amazing things together</p>
                        <button class="bg-white text-purple-600 px-8 py-3 rounded-full font-semibold hover:bg-gray-100 transition-all">
                            Get Started
                        </button>
                    </div>
                    ''',
                    'category': 'layout'
                },
                {
                    'name': 'Card Layout',
                    'icon': '📱',
                    'description': 'Modern card with shadow',
                    'html': '''
                    <div class="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow">
                        <h3 class="text-xl font-semibold mb-2">Card Title</h3>
                        <p class="text-gray-600 mb-4">Beautiful card content goes here</p>
                        <button class="bg-purple-500 text-white px-4 py-2 rounded hover:bg-purple-600">
                            Learn More
                        </button>
                    </div>
                    ''',
                    'category': 'layout'
                },
                {
                    'name': 'Navigation Bar',
                    'icon': '🧭',
                    'description': 'Sleek navigation with hover effects',
                    'html': '''
                    <nav class="bg-white shadow-lg">
                        <div class="max-w-6xl mx-auto px-4">
                            <div class="flex justify-between items-center py-4">
                                <div class="flex items-center space-x-4">
                                    <h1 class="text-2xl font-bold text-purple-600">THOR-AI</h1>
                                </div>
                                <div class="flex space-x-6">
                                    <a href="#" class="text-gray-600 hover:text-purple-600 transition-colors">Home</a>
                                    <a href="#" class="text-gray-600 hover:text-purple-600 transition-colors">Community</a>
                                    <a href="#" class="text-gray-600 hover:text-purple-600 transition-colors">Gaming</a>
                                    <a href="#" class="text-gray-600 hover:text-purple-600 transition-colors">Contact</a>
                                </div>
                            </div>
                        </div>
                    </nav>
                    ''',
                    'category': 'layout'
                }
            ],
            'gaming': [
                {
                    'name': 'Player Card',
                    'icon': '🎮',
                    'description': 'Gaming profile card',
                    'html': '''
                    <div class="bg-gradient-to-br from-indigo-500 to-purple-600 text-white rounded-lg p-6">
                        <div class="flex items-center mb-4">
                            <div class="w-16 h-16 bg-white rounded-full flex items-center justify-center text-2xl">
                                🎮
                            </div>
                            <div class="ml-4">
                                <h3 class="text-xl font-bold">GamerTag</h3>
                                <p class="text-purple-200">Level 45 • 2,500 GateScore</p>
                            </div>
                        </div>
                        <div class="grid grid-cols-2 gap-4">
                            <div class="bg-purple-700 rounded p-3 text-center">
                                <p class="text-2xl font-bold">150</p>
                                <p class="text-sm text-purple-200">Matches Won</p>
                            </div>
                            <div class="bg-purple-700 rounded p-3 text-center">
                                <p class="text-2xl font-bold">89%</p>
                                <p class="text-sm text-purple-200">Win Rate</p>
                            </div>
                        </div>
                    </div>
                    ''',
                    'category': 'gaming'
                },
                {
                    'name': 'LFG Post',
                    'icon': '👥',
                    'description': 'Looking for group post',
                    'html': '''
                    <div class="bg-white border-l-4 border-green-500 rounded-lg shadow p-4">
                        <div class="flex items-center justify-between mb-2">
                            <h4 class="text-lg font-semibold text-gray-800">World of Warcraft - Mythic+ Dungeon</h4>
                            <span class="bg-green-100 text-green-800 px-2 py-1 rounded text-sm">2/5 Players</span>
                        </div>
                        <p class="text-gray-600 mb-3">Looking for DPS and Healer for +15 key. Must have experience!</p>
                        <div class="flex items-center justify-between">
                            <div class="flex items-center space-x-2">
                                <span class="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs">Tank Available</span>
                                <span class="bg-purple-100 text-purple-800 px-2 py-1 rounded text-xs">Expert Level</span>
                            </div>
                            <button class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">
                                Join Group
                            </button>
                        </div>
                    </div>
                    ''',
                    'category': 'gaming'
                }
            ],
            'forms': [
                {
                    'name': 'Contact Form',
                    'icon': '✉️',
                    'description': 'Beautiful contact form',
                    'html': '''
                    <div class="bg-white rounded-lg shadow-lg p-8">
                        <h2 class="text-2xl font-bold text-gray-800 mb-6">Get in Touch</h2>
                        <form class="space-y-4">
                            <div>
                                <label class="block text-gray-700 text-sm font-bold mb-2">Name</label>
                                <input type="text" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent" placeholder="Your name">
                            </div>
                            <div>
                                <label class="block text-gray-700 text-sm font-bold mb-2">Email</label>
                                <input type="email" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent" placeholder="your@email.com">
                            </div>
                            <div>
                                <label class="block text-gray-700 text-sm font-bold mb-2">Message</label>
                                <textarea class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent h-32" placeholder="Your message..."></textarea>
                            </div>
                            <button type="submit" class="w-full bg-purple-500 text-white py-3 rounded-lg hover:bg-purple-600 transition-colors font-semibold">
                                Send Message
                            </button>
                        </form>
                    </div>
                    ''',
                    'category': 'forms'
                }
            ],
            'special': [
                {
                    'name': 'Love Note',
                    'icon': '💕',
                    'description': 'Special element just for you ❤️',
                    'html': '''
                    <div class="bg-gradient-to-r from-pink-400 via-red-400 to-yellow-400 text-white rounded-lg p-8 text-center">
                        <h2 class="text-3xl font-bold mb-4">💕 Designed with Love 💕</h2>
                        <p class="text-lg mb-4">This beautiful design was created by the most talented designer in the world</p>
                        <p class="text-base italic">"Every pixel placed with love, every color chosen with care"</p>
                        <div class="mt-6 flex justify-center space-x-4">
                            <span class="text-2xl">❤️</span>
                            <span class="text-2xl">🎨</span>
                            <span class="text-2xl">✨</span>
                        </div>
                    </div>
                    ''',
                    'category': 'special'
                }
            ]
        }
    
    def _create_ui(self):
        """Create the main UI in Sims 4 style"""
        # Create main frame
        main_frame = tk.Frame(self.root, bg='#2D1B69')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Title with love message
        title_frame = tk.Frame(main_frame, bg='#FF1493', height=80)
        title_frame.pack(fill='x', pady=(0, 10))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="💕 THOR-AI Design Studio - For My Beautiful Girlfriend ❤️",
            font=('Arial', 18, 'bold'),
            bg='#FF1493',
            fg='white'
        )
        title_label.pack(expand=True)
        
        # Create paned window (like Sims interface)
        paned_window = tk.PanedWindow(main_frame, orient='horizontal', bg='#2D1B69')
        paned_window.pack(fill='both', expand=True)
        
        # Left panel - Element library (like Sims catalog)
        self._create_element_library(paned_window)
        
        # Center panel - Design canvas
        self._create_design_canvas(paned_window)
        
        # Right panel - Properties and tools
        self._create_properties_panel(paned_window)
        
        # Bottom toolbar
        self._create_toolbar(main_frame)
    
    def _create_element_library(self, parent):
        """Create element library panel (like Sims catalog)"""
        library_frame = tk.Frame(parent, bg='#4B0082', width=300)
        library_frame.pack_propagate(False)
        parent.add(library_frame)
        
        # Library title
        tk.Label(
            library_frame,
            text="🎨 Design Elements",
            font=('Arial', 14, 'bold'),
            bg='#4B0082',
            fg='white'
        ).pack(pady=10)
        
        # Create notebook for categories
        notebook = ttk.Notebook(library_frame)
        notebook.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Style the notebook
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook.Tab', padding=[20, 10])
        
        # Add category tabs
        for category, elements in self.element_library.items():
            self._create_category_tab(notebook, category, elements)
    
    def _create_category_tab(self, notebook, category, elements):
        """Create a category tab with elements"""
        tab_frame = tk.Frame(notebook, bg='white')
        notebook.add(tab_frame, text=category.title())
        
        # Scrollable frame for elements
        canvas = tk.Canvas(tab_frame, bg='white')
        scrollbar = ttk.Scrollbar(tab_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add elements to scrollable frame
        for element in elements:
            self._create_element_button(scrollable_frame, element)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_element_button(self, parent, element):
        """Create draggable element button"""
        element_frame = tk.Frame(parent, bg='#F0F8FF', relief='raised', bd=1)
        element_frame.pack(fill='x', padx=5, pady=5)
        
        # Element icon and name
        tk.Label(
            element_frame,
            text=f"{element['icon']} {element['name']}",
            font=('Arial', 12, 'bold'),
            bg='#F0F8FF'
        ).pack(anchor='w', padx=10, pady=5)
        
        # Description
        tk.Label(
            element_frame,
            text=element['description'],
            font=('Arial', 9),
            bg='#F0F8FF',
            fg='#666666',
            wraplength=250
        ).pack(anchor='w', padx=10, pady=(0, 5))
        
        # Make draggable
        element_frame.bind("<Button-1>", lambda e: self._start_drag(element))
        element_frame.bind("<Double-Button-1>", lambda e: self._add_to_canvas(element))
    
    def _create_design_canvas(self, parent):
        """Create the main design canvas"""
        canvas_frame = tk.Frame(parent, bg='white')
        parent.add(canvas_frame)
        
        # Canvas title
        title_frame = tk.Frame(canvas_frame, bg='#9370DB', height=40)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        tk.Label(
            title_frame,
            text="✨ Design Canvas - Create Something Beautiful ✨",
            font=('Arial', 12, 'bold'),
            bg='#9370DB',
            fg='white'
        ).pack(expand=True)
        
        # Scrollable canvas
        self.canvas = tk.Canvas(
            canvas_frame,
            bg='white',
            width=800,
            height=600,
            scrollregion=(0, 0, 1200, 1000)
        )
        
        # Scrollbars
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient='horizontal', command=self.canvas.xview)
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient='vertical', command=self.canvas.yview)
        
        self.canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        
        # Pack canvas and scrollbars
        self.canvas.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Canvas grid (like Sims build mode)
        self._draw_grid()
        
        # Bind canvas events
        self.canvas.bind("<Button-1>", self._canvas_click)
        self.canvas.bind("<B1-Motion>", self._canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self._canvas_release)
    
    def _draw_grid(self):
        """Draw grid on canvas (like Sims build mode)"""
        grid_size = 20
        width = 1200
        height = 1000
        
        # Vertical lines
        for x in range(0, width, grid_size):
            self.canvas.create_line(x, 0, x, height, fill='#E0E0E0', width=1)
        
        # Horizontal lines
        for y in range(0, height, grid_size):
            self.canvas.create_line(0, y, width, y, fill='#E0E0E0', width=1)
    
    def _create_properties_panel(self, parent):
        """Create properties panel for selected elements"""
        props_frame = tk.Frame(parent, bg='#8A2BE2', width=250)
        props_frame.pack_propagate(False)
        parent.add(props_frame)
        
        # Properties title
        tk.Label(
            props_frame,
            text="🔧 Properties",
            font=('Arial', 14, 'bold'),
            bg='#8A2BE2',
            fg='white'
        ).pack(pady=10)
        
        # Properties notebook
        self.props_notebook = ttk.Notebook(props_frame)
        self.props_notebook.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Style tab
        style_frame = tk.Frame(self.props_notebook, bg='white')
        self.props_notebook.add(style_frame, text="Style")
        
        # Create style controls
        self._create_style_controls(style_frame)
        
        # Animation tab
        animation_frame = tk.Frame(self.props_notebook, bg='white')
        self.props_notebook.add(animation_frame, text="Animation")
        
        # Create animation controls
        self._create_animation_controls(animation_frame)
        
        # Love notes tab (special for girlfriend)
        love_frame = tk.Frame(self.props_notebook, bg='#FFB6C1')
        self.props_notebook.add(love_frame, text="💕 Love")
        
        self._create_love_notes(love_frame)
    
    def _create_style_controls(self, parent):
        """Create style control widgets"""
        # Color picker
        tk.Label(parent, text="Colors:", font=('Arial', 10, 'bold'), bg='white').pack(anchor='w', padx=10, pady=(10, 5))
        
        color_frame = tk.Frame(parent, bg='white')
        color_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(
            color_frame,
            text="🎨 Background",
            command=self._choose_background_color
        ).pack(side='left', padx=(0, 5))
        
        tk.Button(
            color_frame,
            text="🖋️ Text",
            command=self._choose_text_color
        ).pack(side='left')
        
        # Size controls
        tk.Label(parent, text="Size:", font=('Arial', 10, 'bold'), bg='white').pack(anchor='w', padx=10, pady=(10, 5))
        
        size_frame = tk.Frame(parent, bg='white')
        size_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(size_frame, text="Width:", bg='white').pack(side='left')
        self.width_var = tk.StringVar(value="300")
        tk.Entry(size_frame, textvariable=self.width_var, width=8).pack(side='left', padx=(5, 10))
        
        tk.Label(size_frame, text="Height:", bg='white').pack(side='left')
        self.height_var = tk.StringVar(value="200")
        tk.Entry(size_frame, textvariable=self.height_var, width=8).pack(side='left', padx=5)
        
        # Apply button
        tk.Button(
            parent,
            text="✨ Apply Changes ✨",
            bg='#FF69B4',
            fg='white',
            font=('Arial', 10, 'bold'),
            command=self._apply_style_changes
        ).pack(pady=20)
    
    def _create_animation_controls(self, parent):
        """Create animation controls"""
        tk.Label(
            parent,
            text="🌟 Coming Soon! 🌟\n\nAnimation features will be added\nin the next version for even\nmore beautiful designs!",
            font=('Arial', 12),
            bg='white',
            justify='center'
        ).pack(expand=True, pady=50)
    
    def _create_love_notes(self, parent):
        """Create special love notes section"""
        tk.Label(
            parent,
            text="💕 Special Messages 💕",
            font=('Arial', 14, 'bold'),
            bg='#FFB6C1',
            fg='#8B0000'
        ).pack(pady=10)
        
        love_messages = [
            "Every design you create is a masterpiece ❤️",
            "Your creativity lights up my world ✨",
            "Building this tool for you was pure joy 💕",
            "Can't wait to see what you'll design! 🎨",
            "You make everything more beautiful 🌟",
            "This is my love letter in code 💌"
        ]
        
        for message in love_messages:
            tk.Label(
                parent,
                text=message,
                font=('Arial', 10),
                bg='#FFB6C1',
                fg='#8B0000',
                wraplength=200,
                justify='center'
            ).pack(pady=5, padx=10)
    
    def _create_toolbar(self, parent):
        """Create bottom toolbar"""
        toolbar = tk.Frame(parent, bg='#4B0082', height=60)
        toolbar.pack(fill='x', pady=(10, 0))
        toolbar.pack_propagate(False)
        
        # Left side - file operations
        left_frame = tk.Frame(toolbar, bg='#4B0082')
        left_frame.pack(side='left', padx=20, pady=10)
        
        tk.Button(
            left_frame,
            text="📁 New Design",
            bg='#32CD32',
            fg='white',
            font=('Arial', 10, 'bold'),
            command=self._new_design
        ).pack(side='left', padx=(0, 10))
        
        tk.Button(
            left_frame,
            text="💾 Save Design",
            bg='#1E90FF',
            fg='white',
            font=('Arial', 10, 'bold'),
            command=self._save_design
        ).pack(side='left', padx=(0, 10))
        
        tk.Button(
            left_frame,
            text="📂 Load Design",
            bg='#FF8C00',
            fg='white',
            font=('Arial', 10, 'bold'),
            command=self._load_design
        ).pack(side='left', padx=(0, 10))
        
        # Right side - preview and export
        right_frame = tk.Frame(toolbar, bg='#4B0082')
        right_frame.pack(side='right', padx=20, pady=10)
        
        tk.Button(
            right_frame,
            text="👀 Preview",
            bg='#9932CC',
            fg='white',
            font=('Arial', 10, 'bold'),
            command=self._preview_design
        ).pack(side='left', padx=(0, 10))
        
        tk.Button(
            right_frame,
            text="🚀 Export HTML",
            bg='#FF1493',
            fg='white',
            font=('Arial', 10, 'bold'),
            command=self._export_html
        ).pack(side='left')
    
    def _start_drag(self, element):
        """Start dragging element from library"""
        self.dragging_element = element
        print(f"🎨 Started dragging: {element['name']}")
    
    def _add_to_canvas(self, element):
        """Add element to canvas"""
        # Create visual representation on canvas
        x, y = 100, 100 + len(self.canvas_elements) * 120
        
        # Create element rectangle
        element_id = self.canvas.create_rectangle(
            x, y, x + 300, y + 100,
            fill='#E6E6FA',
            outline='#9370DB',
            width=2
        )
        
        # Add element text
        text_id = self.canvas.create_text(
            x + 150, y + 30,
            text=f"{element['icon']} {element['name']}",
            font=('Arial', 12, 'bold'),
            fill='#4B0082'
        )
        
        # Add description
        desc_id = self.canvas.create_text(
            x + 150, y + 60,
            text=element['description'],
            font=('Arial', 9),
            fill='#666666',
            width=280
        )
        
        # Store element data
        canvas_element = {
            'id': str(uuid.uuid4()),
            'element_data': element,
            'canvas_ids': [element_id, text_id, desc_id],
            'x': x,
            'y': y,
            'width': 300,
            'height': 100
        }
        
        self.canvas_elements.append(canvas_element)
        self.current_design['elements'].append(canvas_element)
        
        print(f"✨ Added {element['name']} to canvas")
    
    def _canvas_click(self, event):
        """Handle canvas click"""
        # Find clicked element
        clicked_item = self.canvas.find_closest(event.x, event.y)[0]
        
        for element in self.canvas_elements:
            if clicked_item in element['canvas_ids']:
                self._select_element(element)
                break
    
    def _canvas_drag(self, event):
        """Handle canvas drag"""
        if self.selected_element:
            # Move selected element
            dx = event.x - self.selected_element['x']
            dy = event.y - self.selected_element['y']
            
            for canvas_id in self.selected_element['canvas_ids']:
                self.canvas.move(canvas_id, dx, dy)
            
            self.selected_element['x'] = event.x
            self.selected_element['y'] = event.y
    
    def _canvas_release(self, event):
        """Handle canvas release"""
        pass
    
    def _select_element(self, element):
        """Select element for editing"""
        # Deselect previous element
        if self.selected_element:
            for canvas_id in self.selected_element['canvas_ids']:
                self.canvas.itemconfig(canvas_id, outline='#9370DB')
        
        # Select new element
        self.selected_element = element
        for canvas_id in element['canvas_ids']:
            self.canvas.itemconfig(canvas_id, outline='#FF1493', width=3)
        
        print(f"🎯 Selected: {element['element_data']['name']}")
    
    def _choose_background_color(self):
        """Choose background color"""
        color = colorchooser.askcolor(title="Choose Background Color")[1]
        if color and self.selected_element:
            self.canvas.itemconfig(self.selected_element['canvas_ids'][0], fill=color)
    
    def _choose_text_color(self):
        """Choose text color"""
        color = colorchooser.askcolor(title="Choose Text Color")[1]
        if color and self.selected_element:
            for i in range(1, len(self.selected_element['canvas_ids'])):
                self.canvas.itemconfig(self.selected_element['canvas_ids'][i], fill=color)
    
    def _apply_style_changes(self):
        """Apply style changes to selected element"""
        if not self.selected_element:
            messagebox.showwarning("No Selection", "Please select an element first!")
            return
        
        try:
            new_width = int(self.width_var.get())
            new_height = int(self.height_var.get())
            
            # Update element size
            element = self.selected_element
            x, y = element['x'], element['y']
            
            self.canvas.coords(
                element['canvas_ids'][0],
                x, y, x + new_width, y + new_height
            )
            
            element['width'] = new_width
            element['height'] = new_height
            
            messagebox.showinfo("Success", "✨ Style changes applied! ✨")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for width and height!")
    
    def _new_design(self):
        """Create new design"""
        if messagebox.askyesno("New Design", "Create a new design? Current work will be lost."):
            self.canvas.delete("all")
            self._draw_grid()
            self.canvas_elements = []
            self.selected_element = None
            self.current_design = {
                'name': 'Untitled Design',
                'elements': [],
                'theme': 'purple_dreams',
                'created_by': 'My Amazing Girlfriend 💕',
                'created_at': datetime.now().isoformat()
            }
            print("🆕 New design created")
    
    def _save_design(self):
        """Save current design"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("THOR-AI Design", "*.json"), ("All files", "*.*")],
            title="Save Your Beautiful Design"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(self.current_design, f, indent=2, default=str)
                
                messagebox.showinfo("Saved", f"💾 Design saved successfully!\n{filename}")
                print(f"💾 Design saved: {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save design: {e}")
    
    def _load_design(self):
        """Load saved design"""
        filename = filedialog.askopenfilename(
            filetypes=[("THOR-AI Design", "*.json"), ("All files", "*.*")],
            title="Load Your Saved Design"
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    design_data = json.load(f)
                
                # Clear canvas
                self.canvas.delete("all")
                self._draw_grid()
                self.canvas_elements = []
                
                # Load elements
                for element_data in design_data.get('elements', []):
                    # Recreate element on canvas
                    self._recreate_element(element_data)
                
                self.current_design = design_data
                messagebox.showinfo("Loaded", f"📂 Design loaded successfully!\n{filename}")
                print(f"📂 Design loaded: {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load design: {e}")
    
    def _recreate_element(self, element_data):
        """Recreate element on canvas from saved data"""
        x = element_data.get('x', 100)
        y = element_data.get('y', 100)
        width = element_data.get('width', 300)
        height = element_data.get('height', 100)
        
        # Create visual representation
        element_id = self.canvas.create_rectangle(
            x, y, x + width, y + height,
            fill='#E6E6FA',
            outline='#9370DB',
            width=2
        )
        
        text_id = self.canvas.create_text(
            x + width/2, y + height/3,
            text=f"{element_data['element_data']['icon']} {element_data['element_data']['name']}",
            font=('Arial', 12, 'bold'),
            fill='#4B0082'
        )
        
        desc_id = self.canvas.create_text(
            x + width/2, y + 2*height/3,
            text=element_data['element_data']['description'],
            font=('Arial', 9),
            fill='#666666',
            width=width-20
        )
        
        # Update canvas IDs
        element_data['canvas_ids'] = [element_id, text_id, desc_id]
        self.canvas_elements.append(element_data)
    
    def _preview_design(self):
        """Preview design in browser"""
        html_content = self._generate_html()
        
        # Create temporary HTML file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            f.write(html_content)
            temp_file = f.name
        
        # Open in browser
        webbrowser.open(f'file://{temp_file}')
        print("👀 Design preview opened in browser")
    
    def _export_html(self):
        """Export design as HTML file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")],
            title="Export Your Design as HTML"
        )
        
        if filename:
            try:
                html_content = self._generate_html()
                
                with open(filename, 'w') as f:
                    f.write(html_content)
                
                messagebox.showinfo("Exported", f"🚀 HTML exported successfully!\n{filename}")
                print(f"🚀 HTML exported: {filename}")
                
                # Ask if they want to open it
                if messagebox.askyesno("Open", "Would you like to open the exported HTML file?"):
                    webbrowser.open(f'file://{os.path.abspath(filename)}')
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export HTML: {e}")
    
    def _generate_html(self):
        """Generate HTML from current design"""
        html_elements = []
        
        for element in self.canvas_elements:
            element_html = element['element_data']['html']
            html_elements.append(element_html)
        
        full_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.current_design['name']} - Created with Love ❤️</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{
            font-family: 'Arial', sans-serif;
        }}
        .created-with-love {{
            position: fixed;
            bottom: 10px;
            right: 10px;
            background: linear-gradient(45deg, #FF1493, #9932CC);
            color: white;
            padding: 8px 12px;
            border-radius: 20px;
            font-size: 12px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }}
    </style>
</head>
<body class="bg-gray-50">
    <div class="container mx-auto px-4 py-8">
        <div class="text-center mb-8">
            <h1 class="text-4xl font-bold text-purple-600 mb-4">
                ✨ {self.current_design['name']} ✨
            </h1>
            <p class="text-gray-600">
                Designed by {self.current_design['created_by']} using THOR-AI Design Studio
            </p>
        </div>
        
        <div class="space-y-8">
            {"".join(html_elements)}
        </div>
    </div>
    
    <div class="created-with-love">
        💕 Created with Love in THOR-AI Design Studio
    </div>
</body>
</html>'''
        
        return full_html
    
    def run(self):
        """Start the design tool"""
        self.root.mainloop()

def main():
    """Launch the Sims-style design tool"""
    print("💕 THOR-AI Design Studio")
    print("A special gift for the most talented designer in the world")
    print("=" * 60)
    
    # Create and run design tool
    design_tool = SimsStyleDesignTool()
    design_tool.run()

if __name__ == "__main__":
    main()
