#!/usr/bin/env python3
"""
🌐 NORTHBAYSTUDIOS.IO - LIVE WEBSITE
Simple Flask server for Stripe verification and business presence
"""

from flask import Flask, render_template_string, jsonify
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Northbay Studios - Gaming & AI Development</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
            color: #e5e5e5;
            font-family: 'SF Mono', 'Monaco', 'Consolas', monospace;
            min-height: 100vh;
            overflow-x: hidden;
        }
        
        .hero {
            text-align: center;
            padding: 80px 20px;
            position: relative;
        }
        
        .logo {
            font-size: 3.5rem;
            font-weight: bold;
            background: linear-gradient(45deg, #00ff88, #0099ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 20px;
        }
        
        .tagline {
            font-size: 1.2rem;
            color: #888;
            margin-bottom: 40px;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }
        
        .services {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        .service-card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(0, 255, 136, 0.2);
            border-radius: 15px;
            padding: 30px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .service-card:hover {
            border-color: #00ff88;
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0, 255, 136, 0.1);
        }
        
        .service-icon {
            font-size: 3rem;
            margin-bottom: 20px;
        }
        
        .service-title {
            font-size: 1.4rem;
            color: #00ff88;
            margin-bottom: 15px;
        }
        
        .service-desc {
            color: #ccc;
            line-height: 1.6;
        }
        
        .contact {
            text-align: center;
            padding: 60px 20px;
            background: rgba(0, 255, 136, 0.05);
            margin-top: 80px;
        }
        
        .contact-info {
            max-width: 600px;
            margin: 0 auto;
        }
        
        .contact h2 {
            color: #00ff88;
            margin-bottom: 20px;
            font-size: 2rem;
        }
        
        .contact p {
            color: #ccc;
            margin-bottom: 10px;
        }
        
        .status-indicator {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(0, 255, 136, 0.9);
            color: #000;
            padding: 10px 20px;
            border-radius: 25px;
            font-weight: bold;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.7; }
            100% { opacity: 1; }
        }
        
        .gaming-elements {
            position: absolute;
            width: 100%;
            height: 100%;
            pointer-events: none;
            overflow: hidden;
        }
        
        .pixel {
            position: absolute;
            width: 2px;
            height: 2px;
            background: #00ff88;
            animation: float 3s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }
        
        @media (max-width: 768px) {
            .logo {
                font-size: 2.5rem;
            }
            
            .services {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="gaming-elements">
        <div class="pixel" style="left: 10%; animation-delay: 0s;"></div>
        <div class="pixel" style="left: 20%; animation-delay: 0.5s;"></div>
        <div class="pixel" style="left: 30%; animation-delay: 1s;"></div>
        <div class="pixel" style="left: 40%; animation-delay: 1.5s;"></div>
        <div class="pixel" style="left: 50%; animation-delay: 2s;"></div>
        <div class="pixel" style="left: 60%; animation-delay: 2.5s;"></div>
        <div class="pixel" style="left: 70%; animation-delay: 3s;"></div>
        <div class="pixel" style="left: 80%; animation-delay: 3.5s;"></div>
        <div class="pixel" style="left: 90%; animation-delay: 4s;"></div>
    </div>
    
    <div class="status-indicator">
        🟢 LIVE
    </div>
    
    <div class="hero">
        <h1 class="logo">NORTHBAY STUDIOS</h1>
        <p class="tagline">
            Cutting-edge Gaming OS Development & AI Automation Solutions
            <br>Building the Future of Interactive Computing
        </p>
    </div>
    
    <div class="services">
        <div class="service-card">
            <div class="service-icon">🎮</div>
            <h3 class="service-title">YOOPER Gaming OS</h3>
            <p class="service-desc">
                Custom gaming kernel with educational syntax. Learn programming through gaming metaphors like IDDQD for super admin access.
            </p>
        </div>
        
        <div class="service-card">
            <div class="service-icon">🤖</div>
            <h3 class="service-title">TRINITY AI System</h3>
            <p class="service-desc">
                Advanced AI ecosystem with THOR (revenue), LOKI (deals), and HELA (learning) agents for automated business operations.
            </p>
        </div>
        
        <div class="service-card">
            <div class="service-icon">📱</div>
            <h3 class="service-title">Custom VOIP SMS</h3>
            <p class="service-desc">
                Free SMS system using VOIP technology. No more expensive Twilio fees - full control and gaming integration.
            </p>
        </div>
        
        <div class="service-card">
            <div class="service-icon">🌐</div>
            <h3 class="service-title">Web Development</h3>
            <p class="service-desc">
                Modern web applications with dark themes and mobile-first design. Built for developers and gamers.
            </p>
        </div>
        
        <div class="service-card">
            <div class="service-icon">⚡</div>
            <h3 class="service-title">Cloud Automation</h3>
            <p class="service-desc">
                Vultr, AWS, and multi-cloud deployment automation. Server management and scaling solutions.
            </p>
        </div>
        
        <div class="service-card">
            <div class="service-icon">💰</div>
            <h3 class="service-title">Revenue Systems</h3>
            <p class="service-desc">
                Automated revenue generation through Fiverr integration, deal hunting, and opportunity detection.
            </p>
        </div>
    </div>
    
    <div class="contact">
        <div class="contact-info">
            <h2>Ready to Level Up?</h2>
            <p><strong>Business Email:</strong> contact@northbaystudios.io</p>
            <p><strong>Technical Support:</strong> support@northbaystudios.io</p>
            <p><strong>Location:</strong> Michigan, USA</p>
            <p><strong>Specialties:</strong> Gaming OS, AI Automation, VOIP Systems</p>
            
            <p style="margin-top: 30px; color: #888;">
                © 2025 Northbay Studios. Built with custom gaming kernel technology.
            </p>
        </div>
    </div>
    
    <script>
        // Gaming console effect
        console.log('🎮 NORTHBAY STUDIOS - Gaming OS Development');
        console.log('⚡ YOOPER Kernel ready for players');
        console.log('🤖 TRINITY AI System online');
        console.log('📱 Custom VOIP SMS active');
        
        // Add some interactive elements
        document.addEventListener('DOMContentLoaded', function() {
            const cards = document.querySelectorAll('.service-card');
            
            cards.forEach(card => {
                card.addEventListener('click', function() {
                    const title = this.querySelector('.service-title').textContent;
                    console.log(`🎯 Interested in: ${title}`);
                });
            });
        });
    </script>
</body>
</html>
    ''')

@app.route('/api/status')
def status():
    """API endpoint for system status"""
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'services': {
            'yooper_kernel': 'active',
            'trinity_ai': 'learning',
            'voip_sms': 'ready',
            'revenue_system': 'hunting'
        }
    })

@app.route('/health')
def health():
    """Health check for monitoring"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    print("🌐 Northbay Studios - Starting production server...")
    print("🎮 Gaming OS development showcase")
    print("🤖 AI automation demonstrations")
    app.run(host='0.0.0.0', port=80, debug=False)
