#!/usr/bin/env python3
"""
📱 SMS NOTIFICATION SYSTEM
Twilio integration for user alerts and notifications
"""

import os
from twilio.rest import Client
import sqlite3
from datetime import datetime

class SMSNotificationSystem:
    """SMS alerts for THOR-AI users and team"""
    
    def __init__(self):
        # Twilio credentials (you'll need to set these up)
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID', 'demo_sid')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN', 'demo_token')
        self.from_number = os.getenv('TWILIO_PHONE_NUMBER', '+15551234567')
        
        # Initialize Twilio client
        try:
            self.client = Client(self.account_sid, self.auth_token)
        except:
            self.client = None
            print("⚠️  Twilio not configured - using demo mode")
            
        self.db_path = "/Users/dwido/TRINITY/production.db"
        self.init_sms_db()
        
    def init_sms_db(self):
        """Initialize SMS notification database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # SMS subscribers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sms_subscribers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                phone_number TEXT UNIQUE,
                name TEXT,
                notification_types TEXT,
                status TEXT DEFAULT 'active',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # SMS history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sms_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number TEXT,
                message TEXT,
                message_type TEXT,
                status TEXT,
                sent_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def add_team_members(self):
        """Add you and Courtney to SMS notifications"""
        
        team_members = [
            {
                'name': 'dwido (Founder)',
                'phone': '+19065533642',  # Your real phone number
                'notifications': ['server_alerts', 'revenue_updates', 'system_status', 'deal_alerts']
            },
            {
                'name': 'Courtney',
                'phone': '+1COURTNEY_PHONE_NUMBER',  # You'll need to provide this
                'notifications': ['system_updates', 'revenue_milestones', 'user_feedback']
            }
        ]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for member in team_members:
            cursor.execute('''
                INSERT OR REPLACE INTO sms_subscribers 
                (user_id, phone_number, name, notification_types, status)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                1,  # Founder user_id
                member['phone'],
                member['name'],
                ','.join(member['notifications']),
                'active'
            ))
            
        conn.commit()
        conn.close()
        
        print(f"📱 Added {len(team_members)} team members to SMS notifications")
        
    def send_sms(self, phone_number, message, message_type='general'):
        """Send SMS notification"""
        
        if self.client:
            try:
                message_obj = self.client.messages.create(
                    body=message,
                    from_=self.from_number,
                    to=phone_number
                )
                
                status = 'sent'
                print(f"✅ SMS sent to {phone_number}: {message[:50]}...")
                
            except Exception as e:
                status = 'failed'
                print(f"❌ SMS failed to {phone_number}: {str(e)}")
                
        else:
            # Demo mode
            status = 'demo'
            print(f"📱 [DEMO SMS to {phone_number}]: {message}")
            
        # Log to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO sms_history (phone_number, message, message_type, status)
            VALUES (?, ?, ?, ?)
        ''', (phone_number, message, message_type, status))
        conn.commit()
        conn.close()
        
        return status == 'sent'
        
    def notify_server_deployment(self, server_name, server_ip):
        """Notify about server deployment"""
        
        message = f"🚀 THOR-AI Alert: {server_name} deployed successfully! IP: {server_ip}. DNS setup required."
        
        self.send_notification_to_team(message, 'server_alerts')
        
    def notify_revenue_milestone(self, amount, milestone_type):
        """Notify about revenue milestones"""
        
        message = f"💰 Revenue Alert: ${amount:.2f} {milestone_type} achieved! THOR-AI is growing! 🎯"
        
        self.send_notification_to_team(message, 'revenue_updates')
        
    def notify_system_status(self, status, details):
        """Notify about system status changes"""
        
        emoji = "✅" if status == "healthy" else "⚠️" if status == "warning" else "❌"
        message = f"{emoji} System Status: {status.upper()} - {details}"
        
        self.send_notification_to_team(message, 'system_status')
        
    def notify_deal_alert(self, deal_type, savings, details):
        """Notify about deals found by LOKI"""
        
        message = f"🔥 LOKI Deal Alert: {deal_type} - Save ${savings:.2f}! {details[:100]}..."
        
        self.send_notification_to_team(message, 'deal_alerts')
        
    def send_notification_to_team(self, message, notification_type):
        """Send notification to all team members subscribed to this type"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT phone_number, name FROM sms_subscribers 
            WHERE status = 'active' AND notification_types LIKE ?
        ''', (f'%{notification_type}%',))
        
        subscribers = cursor.fetchall()
        conn.close()
        
        for phone, name in subscribers:
            self.send_sms(phone, f"{message} - THOR-AI", notification_type)
            
    def get_sms_dashboard(self):
        """Get SMS notification dashboard"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total SMS sent
        cursor.execute('SELECT COUNT(*) FROM sms_history')
        total_sent = cursor.fetchone()[0]
        
        # SMS by type
        cursor.execute('''
            SELECT message_type, COUNT(*) as count
            FROM sms_history
            GROUP BY message_type
            ORDER BY count DESC
        ''')
        by_type = cursor.fetchall()
        
        # Active subscribers
        cursor.execute('SELECT COUNT(*) FROM sms_subscribers WHERE status = "active"')
        active_subscribers = cursor.fetchone()[0]
        
        # Recent messages
        cursor.execute('''
            SELECT phone_number, message, sent_at, status
            FROM sms_history
            ORDER BY sent_at DESC
            LIMIT 5
        ''')
        recent_messages = cursor.fetchall()
        
        conn.close()
        
        return {
            'total_sent': total_sent,
            'by_type': dict(by_type),
            'active_subscribers': active_subscribers,
            'recent_messages': recent_messages
        }

def main():
    """Demo SMS notification system"""
    print("📱 SMS NOTIFICATION SYSTEM")
    print("=" * 30)
    
    # Initialize system
    sms = SMSNotificationSystem()
    
    # Add team members
    print("\n👥 Adding team members...")
    sms.add_team_members()
    
    # Demo notifications
    print("\n📱 Sending demo notifications...")
    
    # Server deployment notification
    sms.notify_server_deployment("Northbaystudios.io", "203.120.45.178")
    
    # Revenue milestone
    sms.notify_revenue_milestone(500.00, "daily revenue")
    
    # System status
    sms.notify_system_status("healthy", "All systems operational, 99.9% uptime")
    
    # Deal alert (from LOKI)
    sms.notify_deal_alert("VPS Hosting", 25.00, "DigitalOcean 50% off annual plans")
    
    # Show dashboard
    print("\n📊 SMS Dashboard:")
    dashboard = sms.get_sms_dashboard()
    
    print(f"  📤 Total SMS Sent: {dashboard['total_sent']}")
    print(f"  👥 Active Subscribers: {dashboard['active_subscribers']}")
    
    if dashboard['by_type']:
        print("  📈 Messages by Type:")
        for msg_type, count in dashboard['by_type'].items():
            print(f"    • {msg_type}: {count}")
            
    print("\n🎯 SMS SYSTEM READY!")
    print("📱 Team notifications active")
    print("🔔 Real-time alerts configured")

if __name__ == "__main__":
    main()
