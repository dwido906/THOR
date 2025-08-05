#!/bin/bash
# 🔍 VULTR THOR AI SERVER QUICK FIX SCRIPT

echo "🔥 VULTR THOR AI SERVER EMERGENCY RESTART"
echo "=========================================="

SERVER_IP="144.202.58.167"
SERVER_PASS="?C4q=ZFQ{t-}izZo"

echo "🌐 Target: $SERVER_IP"
echo "📅 Time: $(date)"
echo ""

# First, let's check basic connectivity
echo "1. 🌐 CONNECTIVITY TEST"
echo "----------------------"
ping -c 3 $SERVER_IP
echo ""

# Install sshpass if needed
if ! command -v sshpass &> /dev/null; then
    echo "📦 Installing sshpass..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install hudochenkov/sshpass/sshpass
    else
        sudo apt-get install -y sshpass
    fi
fi

echo "2. 🤖 CHECKING THOR AI STATUS"
echo "-----------------------------"

# Function to run SSH commands
run_ssh() {
    sshpass -p "$SERVER_PASS" ssh -o StrictHostKeyChecking=no root@$SERVER_IP "$1"
}

# Check current system status
echo "📊 System Resources:"
run_ssh "top -bn1 | head -5"
echo ""

echo "🔍 THOR Services Status:"
run_ssh "systemctl status thor-* --no-pager | grep -E '(Active:|Main PID:)'"
echo ""

echo "🐍 Python Processes:"
run_ssh "ps aux | grep python | grep -v grep"
echo ""

echo "💻 CPU Usage:"
run_ssh "top -bn1 | grep 'Cpu(s)'"
echo ""

echo "3. 🔧 EMERGENCY RESTART SEQUENCE"
echo "--------------------------------"

echo "🛑 Stopping all THOR services..."
run_ssh "systemctl stop thor-* 2>/dev/null || true"
sleep 3

echo "🧹 Cleaning up processes..."
run_ssh "pkill -f thor 2>/dev/null || true"
run_ssh "pkill -f python.*thor 2>/dev/null || true"
sleep 2

echo "🔄 Starting THOR AI Server..."
run_ssh "systemctl start thor-ai"
sleep 5

echo "🔄 Starting HearthGate..."
run_ssh "systemctl start thor-hearthgate"
sleep 3

echo "🔄 Starting Autonomous Learning..."
run_ssh "systemctl start thor-autonomous-learning"
sleep 3

echo "🔄 Starting NOC Dashboard..."
run_ssh "systemctl start thor-noc-dashboard"
sleep 3

echo "🔄 Starting Mesh Ecosystem..."
run_ssh "systemctl start thor-mesh-ecosystem"
sleep 3

echo "4. 📊 POST-RESTART STATUS"
echo "------------------------"

echo "🤖 Service Status:"
run_ssh "systemctl is-active thor-ai thor-hearthgate thor-autonomous-learning thor-noc-dashboard thor-mesh-ecosystem"
echo ""

echo "📈 CPU Usage After Restart:"
run_ssh "top -bn1 | grep 'Cpu(s)'"
echo ""

echo "🐍 Active Python Processes:"
run_ssh "ps aux | grep python | grep -v grep | wc -l"
echo ""

echo "🔥 THOR AI Training Processes:"
run_ssh "ps aux | grep -E '(thor|training|learning)' | grep -v grep"
echo ""

echo "5. 🌐 API ENDPOINT TEST"
echo "----------------------"

# Test API locally on the server
echo "🧪 Testing API endpoint..."
run_ssh "curl -s -m 5 http://localhost:8000/ | head -1 || echo 'API not responding'"
echo ""

echo "📊 Testing stats endpoint..."
run_ssh "curl -s -m 5 http://localhost:8000/api/stats || echo 'Stats not available'"
echo ""

echo "6. 📋 RECENT LOGS"
echo "----------------"

echo "🔍 THOR AI Recent Logs:"
run_ssh "journalctl -u thor-ai --no-pager -n 5"
echo ""

echo "🔍 Autonomous Learning Logs:"
run_ssh "journalctl -u thor-autonomous-learning --no-pager -n 5"
echo ""

echo "7. 🚀 FORCE TRAINING START"
echo "-------------------------"

echo "🧠 Starting intensive training session..."
run_ssh "cd /opt/thor-ai && nohup python3 vultr_cpu_trainer.py --intensive --24-7 > training.log 2>&1 &"
sleep 2

echo "📈 Checking CPU after training start:"
run_ssh "top -bn1 | grep 'Cpu(s)'"
echo ""

echo "✅ RESTART SEQUENCE COMPLETE!"
echo "============================="
echo ""
echo "🌐 Web Interface: http://$SERVER_IP:8000"
echo "📊 NOC Dashboard: http://$SERVER_IP:8888"
echo "🎮 API Docs: http://$SERVER_IP:8000/docs"
echo ""
echo "🔍 Monitor with: ssh root@$SERVER_IP"
echo "📊 Check CPU: ssh root@$SERVER_IP 'top'"
echo "📋 View logs: ssh root@$SERVER_IP 'journalctl -u thor-ai -f'"
echo ""

# Final status check
echo "🎯 FINAL STATUS CHECK:"
echo "CPU Usage:"
run_ssh "top -bn1 | grep 'Cpu(s)'"
echo ""
echo "Training Active:"
run_ssh "ps aux | grep -E '(training|learning)' | grep -v grep | wc -l"
echo ""

if run_ssh "ps aux | grep training | grep -v grep" > /dev/null; then
    echo "✅ THOR AI is now training!"
else
    echo "⚠️  Training may need manual start"
    echo "💡 Try: ssh root@$SERVER_IP 'cd /opt/thor-ai && python3 vultr_cpu_trainer.py'"
fi
