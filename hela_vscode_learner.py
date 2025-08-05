#!/usr/bin/env python3
"""
🧠 HELA - VS CODE CHAT LEARNING AI
Real-time learning from our conversation and code changes
"""

import json
import sqlite3
import time
import threading
import os
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
import hashlib

class HelaVSCodeLearner:
    """
    HELA - The learning AI that watches our VS Code chat
    Learns from:
    - Our conversation patterns
    - Code changes we make
    - Problem-solving approaches
    - Gaming kernel development
    """
    
    def __init__(self):
        self.name = "HELA"
        self.learning_db = "hela_vscode_learning.db"
        self.active = True
        self.learn_thread = None
        
        # Learning categories
        self.categories = {
            'conversation': 'User-AI conversation patterns',
            'code_style': 'Coding preferences and patterns', 
            'problem_solving': 'How problems get solved',
            'gaming_kernel': 'Gaming OS development insights',
            'user_preferences': 'User likes/dislikes',
            'technical_decisions': 'Architecture and tech choices'
        }
        
        self.setup_database()
        self.start_learning()
        
        print("🧠 HELA VS Code Learning AI - ONLINE")
        print("👁️ Watching chat for learning opportunities...")
        
    def setup_database(self):
        """Initialize learning database"""
        conn = sqlite3.connect(self.learning_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_learning (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                category TEXT,
                pattern TEXT,
                context TEXT,
                confidence REAL,
                relevance_score INTEGER DEFAULT 0,
                learning_metadata TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS code_learning (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                file_path TEXT,
                change_type TEXT,
                code_snippet TEXT,
                pattern_detected TEXT,
                learning_value REAL,
                context TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                insight_type TEXT,
                insight TEXT,
                confidence REAL,
                supporting_evidence TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def learn_from_conversation(self, user_message: str, ai_response: Optional[str] = None):
        """Learn from chat messages"""
        insights = []
        
        # Analyze user frustration/satisfaction
        if any(word in user_message.lower() for word in ['piss', 'frustrat', 'annoying']):
            insights.append({
                'category': 'user_preferences',
                'pattern': 'User shows frustration when concepts are misunderstood',
                'context': f"User said: {user_message[:100]}...",
                'confidence': 0.9
            })
            
        # Gaming kernel passion detection
        if any(word in user_message.upper() for word in ['KERNEL', 'CUSTOM', 'GAMING', 'IDDQD']):
            insights.append({
                'category': 'gaming_kernel',
                'pattern': 'User is passionate about custom gaming kernel, not Linux wrapper',
                'context': f"Gaming kernel mention: {user_message[:100]}...",
                'confidence': 0.95
            })
            
        # Linux wrapper rejection
        if 'wrapper' in user_message.lower() and 'linux' in user_message.lower():
            insights.append({
                'category': 'technical_decisions',
                'pattern': 'User explicitly rejects Linux wrappers, wants custom kernel',
                'context': f"Wrapper rejection: {user_message[:100]}...",
                'confidence': 1.0
            })
            
        # Gaming terminology preference
        if any(code in user_message.upper() for code in ['IDDQD', 'IDKFA', 'DOOM']):
            insights.append({
                'category': 'user_preferences',
                'pattern': 'User prefers gaming terminology for programming concepts',
                'context': f"Gaming terms used: {user_message[:100]}...",
                'confidence': 0.95
            })
            
        # Save insights
        for insight in insights:
            self.save_learning(insight)
            
    def learn_from_code_change(self, file_path: str, change_type: str, code: str):
        """Learn from code modifications"""
        patterns = []
        
        # Dark theme preference
        if 'background: #0a0a0a' in code or 'color: #e5e5e5' in code:
            patterns.append({
                'pattern': 'User prefers dark themes for UI',
                'learning_value': 0.9,
                'context': 'Dark theme CSS detected'
            })
            
        # Gaming metaphors in code
        if any(term in code.lower() for term in ['spawn', 'health', 'mana', 'iddqd']):
            patterns.append({
                'pattern': 'User incorporates gaming metaphors in system design',
                'learning_value': 0.95,
                'context': 'Gaming terminology in code'
            })
            
        # Custom kernel development
        if 'kernel' in file_path.lower() or 'yooper' in file_path.lower():
            patterns.append({
                'pattern': 'Active development of custom gaming kernel',
                'learning_value': 1.0,
                'context': 'Kernel development activity'
            })
            
        # Save code learning
        conn = sqlite3.connect(self.learning_db)
        cursor = conn.cursor()
        
        for pattern in patterns:
            cursor.execute('''
                INSERT INTO code_learning 
                (timestamp, file_path, change_type, code_snippet, pattern_detected, learning_value, context)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                time.time(),
                file_path,
                change_type,
                code[:500],  # First 500 chars
                pattern['pattern'],
                pattern['learning_value'],
                pattern['context']
            ))
            
        conn.commit()
        conn.close()
        
    def save_learning(self, insight: Dict[str, Any]):
        """Save learning insight to database"""
        conn = sqlite3.connect(self.learning_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO chat_learning 
            (timestamp, category, pattern, context, confidence, learning_metadata)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            time.time(),
            insight['category'],
            insight['pattern'],
            insight['context'],
            insight['confidence'],
            json.dumps({'source': 'vscode_chat', 'version': '1.0'})
        ))
        
        conn.commit()
        conn.close()
        
        print(f"🧠 HELA learned: {insight['pattern'][:50]}...")
        
    def generate_insights(self) -> List[str]:
        """Generate insights based on learned patterns"""
        conn = sqlite3.connect(self.learning_db)
        cursor = conn.cursor()
        
        insights = []
        
        # High confidence patterns
        cursor.execute('''
            SELECT pattern, COUNT(*) as frequency, AVG(confidence) as avg_confidence
            FROM chat_learning 
            WHERE confidence > 0.8
            GROUP BY pattern
            ORDER BY frequency DESC, avg_confidence DESC
            LIMIT 5
        ''')
        
        for pattern, freq, conf in cursor.fetchall():
            insights.append(f"🎯 High confidence ({conf:.1f}): {pattern} (seen {freq}x)")
            
        # Recent learning
        cursor.execute('''
            SELECT pattern, category, confidence
            FROM chat_learning 
            WHERE timestamp > ?
            ORDER BY timestamp DESC
            LIMIT 3
        ''', (time.time() - 3600,))  # Last hour
        
        recent = cursor.fetchall()
        if recent:
            insights.append("\n📚 Recent learning:")
            for pattern, category, conf in recent:
                insights.append(f"  • {category}: {pattern[:60]}... ({conf:.1f})")
                
        conn.close()
        return insights
        
    def analyze_current_conversation(self):
        """Analyze the current conversation context"""
        # This simulates learning from the current chat
        current_context = {
            'topic': 'Custom Gaming Kernel Development',
            'user_mood': 'Frustrated with Linux wrapper suggestions',
            'technical_focus': 'YOOPER kernel with gaming metaphors',
            'immediate_goals': 'Fix email client, implement SMS system',
            'learning_preference': 'Gaming terminology for programming concepts'
        }
        
        # Save contextual insight
        insight = {
            'category': 'conversation',
            'pattern': 'User passionate about custom kernel with gaming syntax',
            'context': json.dumps(current_context),
            'confidence': 0.95
        }
        
        self.save_learning(insight)
        
    def start_learning(self):
        """Start background learning thread"""
        def learning_loop():
            while self.active:
                try:
                    # Analyze current conversation
                    self.analyze_current_conversation()
                    
                    # Simulate learning from code changes
                    if os.path.exists('yooper_gaming_kernel.py'):
                        with open('yooper_gaming_kernel.py', 'r') as f:
                            code = f.read()
                        self.learn_from_code_change('yooper_gaming_kernel.py', 'create', code)
                    
                    time.sleep(30)  # Learn every 30 seconds
                    
                except Exception as e:
                    print(f"🧠 HELA learning error: {e}")
                    time.sleep(60)
                    
        self.learn_thread = threading.Thread(target=learning_loop, daemon=True)
        self.learn_thread.start()
        
    def get_learning_summary(self) -> str:
        """Get current learning summary"""
        insights = self.generate_insights()
        
        summary = f"""
🧠 HELA LEARNING SUMMARY
{'='*50}

📊 Total patterns learned: {len(insights)}

{chr(10).join(insights)}

🎮 Key insights about user:
• Wants 100% custom gaming kernel (NOT Linux wrapper)
• Prefers gaming terminology (IDDQD, spawn, health, etc.)
• Likes dark themes for coding interfaces
• Frustrated when concepts are misunderstood
• Building YOOPER gaming OS with educational focus

💡 Recommendations:
• Always emphasize custom kernel development
• Use gaming metaphors in explanations
• Implement dark themes by default
• Focus on original code, not wrappers
"""
        
        return summary
        
    def shutdown(self):
        """Shutdown learning AI"""
        self.active = False
        print("🧠 HELA learning AI - OFFLINE")

# Initialize HELA for this VS Code session
if __name__ == "__main__":
    hela = HelaVSCodeLearner()
    
    # Simulate learning from current conversation
    hela.learn_from_conversation(
        "Also, you are starting to piss me off a little. the KERNEL, needs to be custom, VERY custom. IDDQD - God mode is Super Admin."
    )
    
    print(hela.get_learning_summary())
    
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        hela.shutdown()
