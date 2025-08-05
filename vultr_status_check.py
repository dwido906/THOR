#!/usr/bin/env python3
"""
THOR/ODIN Status Dashboard and Access Portal
Check current Vultr deployments and provide access information
"""

import requests
import json
from datetime import datetime

def check_vultr_status(api_key: str):
    """Check current Vultr server status"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print("🔍 Checking your current Vultr deployments...")
    
    try:
        # Get account info
        response = requests.get("https://api.vultr.com/v2/account", headers=headers)
        if response.status_code == 200:
            account = response.json()
            print(f"✅ Account: {account.get('name', 'Unknown')}")
            print(f"💰 Balance: ${account.get('balance', 0)}")
            print(f"📧 Email: {account.get('email', 'Unknown')}")
        
        # Get instances
        response = requests.get("https://api.vultr.com/v2/instances", headers=headers)
        if response.status_code == 200:
            data = response.json()
            instances = data.get('instances', [])
            
            print(f"\n🌐 Current Servers: {len(instances)}")
            print("="*60)
            
            for i, instance in enumerate(instances, 1):
                print(f"\n🖥️ Server {i}: {instance.get('label', 'Unnamed')}")
                print(f"   📋 ID: {instance.get('id')}")
                print(f"   🌍 Region: {instance.get('region')}")
                print(f"   💻 Plan: {instance.get('plan')}")
                print(f"   🔌 Status: {instance.get('status')}")
                print(f"   ⚡ Power: {instance.get('power_status')}")
                print(f"   🌐 IP: {instance.get('main_ip', 'Provisioning...')}")
                print(f"   📅 Created: {instance.get('date_created')}")
                
                # Determine server type
                label = instance.get('label', '').lower()
                if 'thor' in label:
                    print(f"   🌱 Type: THOR Gamer/Developer Platform")
                    ip = instance.get('main_ip')
                    if ip:
                        print(f"   🎮 Dashboard: http://{ip}:8080")
                        print(f"   🚀 SSH Access: ssh root@{ip}")
                elif 'odin' in label:
                    print(f"   👁️ Type: ODIN Core Server OS")
                    ip = instance.get('main_ip')
                    if ip:
                        print(f"   👁️ Dashboard: http://{ip}:9090")
                        print(f"   🚀 SSH Access: ssh root@{ip}")
                else:
                    print(f"   ❓ Type: Unknown/Legacy Server")
                    ip = instance.get('main_ip')
                    if ip:
                        print(f"   🌐 Access: http://{ip}")
                        print(f"   🚀 SSH Access: ssh root@{ip}")
            
            if not instances:
                print("❌ No servers found. Need to deploy THOR/ODIN systems.")
                print("💡 To deploy, increase your Vultr monthly limit first.")
            
        else:
            print(f"❌ Failed to get instances: {response.status_code}")
            
    except Exception as e:
        print(f"💥 Error checking Vultr status: {e}")

def show_access_dashboard():
    """Show access dashboard for THOR/ODIN systems"""
    print(f"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                    🎯 THOR/ODIN ACCESS DASHBOARD 🎯                       ║
║                         NORTHBAY STUDIOS                                  ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  🌐 ACCESS YOUR SYSTEMS:                                                  ║
║                                                                           ║
║  📊 STATS & MONITORING:                                                   ║
║     • northbaystudios.io - Main Website                                  ║
║     • admin.northbaystudios.io - Admin Dashboard                         ║
║     • stats.northbaystudios.io - Analytics Dashboard                     ║
║                                                                           ║
║  🌱 THOR GAMER/DEVELOPER PLATFORMS:                                       ║
║     • thor.northbaystudios.io - THOR Main Interface                      ║
║     • [Your Vultr THOR IPs] - Direct Server Access                       ║
║                                                                           ║
║  👁️ ODIN CORE SERVER MONITORING:                                          ║
║     • odin.northbaystudios.io - ODIN Command Center                      ║
║     • [Your Vultr ODIN IPs] - Direct Server Access                       ║
║                                                                           ║
║  🎮 GAMING COMMUNITY:                                                     ║
║     • gaming.northbaystudios.io - Gaming Hub                             ║
║     • discord.northbaystudios.io - Discord Integration                   ║
║                                                                           ║
║  💡 TIP: Use the Vultr server IPs above for direct access                ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
    """)

def main():
    """Main function"""
    print("🚀 THOR/ODIN Status Check & Access Portal")
    print("="*50)
    
    # Get API key
    api_key = "5QPRJXTKJ5DKDDKMM7NRS32IFVPNGFG27CFA"
    
    # Check Vultr status
    check_vultr_status(api_key)
    
    # Show access dashboard
    show_access_dashboard()
    
    print("\n📋 NEXT STEPS:")
    print("1. 💰 Increase Vultr monthly limit to deploy more servers")
    print("2. 🌐 Access existing servers using IPs shown above")
    print("3. 🔧 Configure domain DNS to point to server IPs")
    print("4. 🚀 Deploy THOR/ODIN once limit is increased")
    
    print(f"\n⏰ Status checked at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
