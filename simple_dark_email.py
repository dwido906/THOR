#!/usr/bin/env python3
"""
📧 SIMPLE DARK EMAIL CLIENT - NO TEMPLATE ERRORS!
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def email_client():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>THOR Email - Dark Mode</title>
    <style>
        body { 
            background: #0a0a0a; 
            color: #00ff88; 
            font-family: monospace; 
            padding: 20px; 
        }
        .header { 
            font-size: 2rem; 
            text-align: center; 
            margin-bottom: 30px; 
        }
        .email-card { 
            background: #1a1a1a; 
            border: 1px solid #333; 
            border-radius: 8px; 
            padding: 15px; 
            margin: 10px 0; 
        }
        .sender { color: #fff; font-weight: bold; }
        .subject { color: #00ff88; margin: 5px 0; }
        .preview { color: #888; }
    </style>
</head>
<body>
    <div class="header">📧 THOR EMAIL - DARK MODE</div>
    
    <div class="email-card">
        <div class="sender">THOR-AI System</div>
        <div class="subject">🚀 Northbaystudios.io Deployment Complete</div>
        <div class="preview">Your server is live! Trinity AI learning system activated...</div>
    </div>
    
    <div class="email-card">
        <div class="sender">LOKI Deal Hunter</div>
        <div class="subject">💰 Oracle Cloud $300 Credits Found</div>
        <div class="preview">Urgent: Free ARM servers available. Sign up now...</div>
    </div>
    
    <div class="email-card">
        <div class="sender">Vultr</div>
        <div class="subject">Server northbaystudios-production is active</div>
        <div class="preview">Your new server in New Jersey datacenter is ready...</div>
    </div>
    
    <div style="text-align: center; margin-top: 30px; color: #666;">
        🎮 THOR Email System - No More Blinding White!
    </div>
</body>
</html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
