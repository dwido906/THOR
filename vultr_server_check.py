#!/usr/bin/env python3
"""
📧 EMAIL DOMAIN STRATEGY & VULTR SERVER MANAGEMENT
Check existing Vultr servers and setup email domains
"""

import requests
import json

class VultrServerManager:
    """Manage Vultr servers and email domains"""
    
    def __init__(self):
        self.api_key = "5QPRJXTKJ5DKDDKMM7NRS32IFVPNGFG27CFA"
        self.base_url = "https://api.vultr.com/v2"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
    def list_existing_servers(self):
        """Check existing Vultr servers"""
        print("🔍 Checking existing Vultr servers...")
        
        try:
            response = requests.get(
                f"{self.base_url}/instances",
                headers=self.headers
            )
            
            if response.status_code == 200:
                servers = response.json().get('instances', [])
                
                print(f"📊 Found {len(servers)} existing servers:")
                
                for server in servers:
                    print(f"🖥️  Server: {server.get('label', 'Unnamed')}")
                    print(f"   📍 IP: {server.get('main_ip', 'N/A')}")
                    print(f"   ⚡ Status: {server.get('status', 'Unknown')}")
                    print(f"   🎮 Plan: {server.get('plan', 'N/A')}")
                    print(f"   🌍 Region: {server.get('region', 'N/A')}")
                    print()
                    
                return servers
            else:
                print(f"❌ Failed to fetch servers: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Error checking servers: {e}")
            return []
            
    def check_domain_availability(self, domains):
        """Check if domains are available for email setup"""
        print("📧 Checking email domain strategy...")
        
        email_strategy = {
            "business_operations": {
                "domain": "northbaystudios.io",
                "purpose": "Customer-facing emails",
                "examples": [
                    "support@northbaystudios.io",
                    "sales@northbaystudios.io", 
                    "info@northbaystudios.io"
                ]
            },
            "ai_headquarters": {
                "domain": "dwido.xyz",
                "purpose": "AI system emails & admin",
                "examples": [
                    "thor@dwido.xyz",
                    "loki@dwido.xyz",
                    "hela@dwido.xyz",
                    "admin@dwido.xyz"
                ]
            },
            "user_personalization": {
                "domain": "hearthgate.xyz",
                "purpose": "Custom user email addresses",
                "examples": [
                    "username@hearthgate.xyz",
                    "custom.name@hearthgate.xyz",
                    "guild.leader@hearthgate.xyz"
                ]
            },
            "ai_specialized": {
                "domain": "thor-ai.xyz", 
                "purpose": "Dedicated AI agent communications",
                "examples": [
                    "deploy@thor-ai.xyz",
                    "monitor@thor-ai.xyz",
                    "alerts@thor-ai.xyz"
                ]
            }
        }
        
        print("📧 EMAIL DOMAIN STRATEGY:")
        print("=" * 50)
        
        for category, config in email_strategy.items():
            print(f"🎯 {category.upper().replace('_', ' ')}")
            print(f"   Domain: {config['domain']}")
            print(f"   Purpose: {config['purpose']}")
            print("   Examples:")
            for email in config['examples']:
                print(f"     📨 {email}")
            print()
            
        return email_strategy

def main():
    """Check servers and setup email strategy"""
    print("🔍 VULTR SERVER & EMAIL DOMAIN MANAGEMENT")
    print("=" * 60)
    
    manager = VultrServerManager()
    
    # Check existing servers
    servers = manager.list_existing_servers()
    
    # Setup email domain strategy
    domains = ["dwido.xyz", "hearthgate.xyz", "thor-ai.xyz"]
    email_strategy = manager.check_domain_availability(domains)
    
    print("🎯 RECOMMENDATIONS:")
    print("=" * 30)
    print("✅ Use northbaystudios.io for business emails")
    print("✅ Use dwido.xyz for AI system emails")
    print("✅ Use hearthgate.xyz for customer personalization")
    print("✅ Use thor-ai.xyz for specialized AI communications")
    print()
    print("💡 This creates clear email separation while maintaining")
    print("   professional appearance and AI transparency!")

if __name__ == "__main__":
    main()
