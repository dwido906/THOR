#!/usr/bin/env python3
"""
📧 THOR-AI EMAIL CLIENT
Beautiful dark mobile-first email interface with card system
"""

from flask import Flask, render_template_string, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def email_client():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>THOR-AI Email</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        /* DARK THEME FOR CODERS/GAMERS */
        body {
            background: #0a0a0a;
            color: #e5e5e5;
            font-family: 'SF Mono', 'Monaco', 'Consolas', monospace;
        }
        .email-container {
            max-width: 420px;
            margin: 0 auto;
            padding: 15px;
            min-height: 100vh;
        }
        .email-card {
            background: #1a1a1a;
            border: 1px solid #333;
            border-radius: 12px;
            margin-bottom: 12px;
            padding: 16px;
            transition: all 0.2s ease;
            cursor: pointer;
        }
        .email-card:hover {
            background: #252525;
            border-color: #444;
            transform: translateY(-1px);
        }
        .email-card.unread {
            border-left: 3px solid #00ff88;
        }
        .email-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }
        .sender-name {
            font-weight: 600;
            color: #ffffff;
            font-size: 14px;
        }
        .email-time {
            font-size: 12px;
            color: #888;
        }
        .email-subject {
            font-size: 13px;
            color: #cccccc;
            margin-bottom: 6px;
            font-weight: 500;
        }
        .email-preview {
            font-size: 12px;
            color: #999;
            line-height: 1.4;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
        }
        .compose-btn {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 60px;
            height: 60px;
            background: #00ff88;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0, 255, 136, 0.3);
            transition: all 0.2s ease;
        }
        .compose-btn:hover {
            transform: scale(1.1);
            box-shadow: 0 6px 20px rgba(0, 255, 136, 0.4);
        }
        .search-bar {
            background: #1a1a1a;
            border: 1px solid #333;
            border-radius: 8px;
            padding: 12px 16px;
            width: 100%;
            color: #ffffff;
            margin-bottom: 20px;
            font-size: 14px;
        }
        .search-bar:focus {
            outline: none;
            border-color: #00ff88;
        }
        .folder-nav {
            display: flex;
            gap: 8px;
            margin-bottom: 20px;
            overflow-x: auto;
            padding-bottom: 8px;
        }
        .folder-tab {
            background: #1a1a1a;
            border: 1px solid #333;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 12px;
            white-space: nowrap;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .folder-tab.active {
            background: #00ff88;
            color: #000000;
            border-color: #00ff88;
        }
        .email-actions {
            display: flex;
            gap: 8px;
            margin-top: 8px;
        }
        .action-btn {
            background: #2a2a2a;
            border: none;
            padding: 6px 12px;
            border-radius: 6px;
            color: #ccc;
            font-size: 11px;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .action-btn:hover {
            background: #3a3a3a;
            color: #fff;
        }
        .priority-high {
            border-left-color: #ff4444 !important;
        }
        .priority-medium {
            border-left-color: #ffaa00 !important;
        }
        @media (max-width: 480px) {
            .email-container {
                padding: 10px;
            }
            .compose-btn {
                bottom: 15px;
                right: 15px;
                width: 55px;
                height: 55px;
            }
        }
    </style>
</head>
<body>
    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect } = React;

        function EmailClient() {
            const [emails, setEmails] = useState([]);
            const [activeFolder, setActiveFolder] = useState('inbox');
            const [searchTerm, setSearchTerm] = useState('');

            useEffect(() => {
                // Demo emails
                const demoEmails = [
                    {
                        id: 1,
                        sender: 'THOR-AI System',
                        subject: '🚀 Northbaystudios.io Deployment Complete',
                        preview: 'Your server is live at 207.246.95.179. Trinity AI learning system activated...',
                        time: '2 min ago',
                        unread: true,
                        priority: 'high'
                    },
                    {
                        id: 2,
                        sender: 'LOKI Deal Hunter',
                        subject: '💰 Oracle Cloud $300 Credits Found',
                        preview: 'Urgent: Free ARM servers available. Sign up now for maximum value...',
                        time: '15 min ago',
                        unread: true,
                        priority: 'high'
                    },
                    {
                        id: 3,
                        sender: 'Stripe Notifications',
                        subject: 'Business verification pending',
                        preview: 'Complete your business profile to activate payments...',
                        time: '1 hour ago',
                        unread: false,
                        priority: 'medium'
                    },
                    {
                        id: 4,
                        sender: 'Vultr',
                        subject: 'Server northbaystudios-production is active',
                        preview: 'Your new server in New Jersey datacenter is ready for use...',
                        time: '2 hours ago',
                        unread: false,
                        priority: 'medium'
                    },
                    {
                        id: 5,
                        sender: 'Trinity AI Learning',
                        subject: '🧠 Chat Learning Integration Complete',
                        preview: 'THOR, LOKI, and HELA are now learning from conversations. 5 patterns extracted...',
                        time: '3 hours ago',
                        unread: false,
                        priority: 'low'
                    }
                ];
                setEmails(demoEmails);
            }, []);

            const folders = [
                { id: 'inbox', name: 'Inbox', count: emails.filter(e => e.unread).length },
                { id: 'alerts', name: 'Alerts', count: 3 },
                { id: 'deals', name: 'Deals', count: 1 },
                { id: 'sent', name: 'Sent', count: 0 }
            ];

            const filteredEmails = emails.filter(email => 
                email.sender.toLowerCase().includes(searchTerm.toLowerCase()) ||
                email.subject.toLowerCase().includes(searchTerm.toLowerCase())
            );

            return (
                <div className="email-container">
                    {/* Search Bar */}
                    <input
                        type="text"
                        placeholder="🔍 Search emails..."
                        className="search-bar"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />

                    {/* Folder Navigation */}
                    <div className="folder-nav">
                        {folders.map(folder => (
                            <div
                                key={folder.id}
                                className={`folder-tab ${activeFolder === folder.id ? 'active' : ''}`}
                                onClick={() => setActiveFolder(folder.id)}
                            >
                                {folder.name} {folder.count > 0 && `(${folder.count})`}
                            </div>
                        ))}
                    </div>

                    {/* Email Cards */}
                    <div className="emails-list">
                        {filteredEmails.map(email => (
                            <div
                                key={email.id}
                                className={`email-card ${email.unread ? 'unread' : ''} ${email.priority ? 'priority-' + email.priority : ''}`}
                            >
                                <div className="email-header">
                                    <span className="sender-name">{email.sender}</span>
                                    <span className="email-time">{email.time}</span>
                                </div>
                                <div className="email-subject">{email.subject}</div>
                                <div className="email-preview">{email.preview}</div>
                                
                                <div className="email-actions">
                                    <button className="action-btn">📄 Read</button>
                                    <button className="action-btn">↩️ Reply</button>
                                    <button className="action-btn">🗑️ Delete</button>
                                </div>
                            </div>
                        ))}
                    </div>

                    {/* Compose Button */}
                    <div className="compose-btn" onClick={() => alert('📝 Compose email coming soon!')}>
                        <i className="fas fa-plus" style={{color: '#000', fontSize: '20px'}}></i>
                    </div>
                </div>
            );
        }

        ReactDOM.render(<EmailClient />, document.getElementById('root'));
    </script>
</body>
</html>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
