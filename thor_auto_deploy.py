#!/usr/bin/env python3
# 🤖 AI Agent Auto-Deployment Wrapper

import subprocess
import time

def thor_auto_deploy():
    print("🤖 THOR-AI initiating auto-deployment...")
    
    try:
        result = subprocess.run(['./auto_deploy.sh'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ THOR-AI deployment successful!")
            print(result.stdout)
        else:
            print("❌ THOR-AI deployment failed!")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ THOR-AI deployment error: {e}")

if __name__ == "__main__":
    thor_auto_deploy()
