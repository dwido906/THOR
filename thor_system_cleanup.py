#!/usr/bin/env python3
"""
🧹 THOR SYSTEM CLEANUP - FREE UP MEMORY ON MAC
"""

import os
import subprocess
import psutil
import time

class ThorSystemCleanup:
    """System memory and resource cleanup"""
    
    def __init__(self):
        self.memory_threshold = 85  # Cleanup when memory usage > 85%
        
    def get_memory_usage(self):
        """Get current memory usage"""
        memory = psutil.virtual_memory()
        return {
            'total_gb': round(memory.total / (1024**3), 2),
            'used_gb': round(memory.used / (1024**3), 2),
            'available_gb': round(memory.available / (1024**3), 2),
            'percent': memory.percent
        }
        
    def find_memory_hogs(self):
        """Find processes using most memory"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'memory_info']):
            try:
                memory_percent = proc.info.get('memory_percent')
                if memory_percent and memory_percent > 1.0:  # More than 1% memory
                    processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'memory_percent': round(memory_percent, 2),
                        'memory_mb': round(proc.info['memory_info'].rss / 1024 / 1024, 1)
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied, TypeError):
                pass
                
        return sorted(processes, key=lambda x: x['memory_percent'], reverse=True)[:20]
        
    def cleanup_safe_processes(self):
        """Cleanup safe-to-kill processes"""
        cleanup_targets = [
            'sirittsd',  # Siri TTS service
            'mds_stores',  # Spotlight indexing (safe to restart)
            'com.apple.dock.extra',  # Dock extras
        ]
        
        killed_processes = []
        
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] in cleanup_targets:
                    proc.terminate()
                    killed_processes.append(proc.info['name'])
                    print(f"🧹 Terminated: {proc.info['name']} (PID: {proc.info['pid']})")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
                
        return killed_processes
        
    def cleanup_system_caches(self):
        """Clean system caches"""
        cleanup_commands = [
            ['sudo', 'purge'],  # Free up memory
            ['sudo', 'sysctl', '-w', 'kern.maxvnodes=1000000'],  # Optimize file system
        ]
        
        for cmd in cleanup_commands:
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    print(f"✅ Executed: {' '.join(cmd)}")
                else:
                    print(f"⚠️ Warning: {' '.join(cmd)} - {result.stderr}")
            except subprocess.TimeoutExpired:
                print(f"⏰ Timeout: {' '.join(cmd)}")
            except Exception as e:
                print(f"❌ Error: {' '.join(cmd)} - {e}")
                
    def recommend_closures(self):
        """Recommend processes to close manually"""
        memory_hogs = self.find_memory_hogs()
        recommendations = []
        
        # Check for specific memory-heavy processes
        for proc in memory_hogs:
            if proc['memory_mb'] > 500:  # More than 500MB
                if 'ThorOS.py' in proc['name']:
                    recommendations.append(f"🎯 LARGE: ThorOS.py using {proc['memory_mb']}MB - Consider restarting")
                elif 'Spotify' in proc['name']:
                    recommendations.append(f"🎵 Spotify using {proc['memory_mb']}MB - Restart app if needed")
                elif 'Steam' in proc['name']:
                    recommendations.append(f"🎮 Steam using {proc['memory_mb']}MB - Close if not gaming")
                elif 'Code Helper' in proc['name']:
                    recommendations.append(f"💻 VS Code using {proc['memory_mb']}MB - Close unused extensions")
                    
        return recommendations
        
    def full_cleanup(self):
        """Perform full system cleanup"""
        print("🧹 THOR SYSTEM CLEANUP STARTING...")
        print("=" * 50)
        
        # Show initial memory usage
        memory_before = self.get_memory_usage()
        print(f"💾 Memory Before: {memory_before['used_gb']}GB / {memory_before['total_gb']}GB ({memory_before['percent']}%)")
        
        # Find memory hogs
        print("\n🔍 TOP MEMORY USERS:")
        memory_hogs = self.find_memory_hogs()
        for i, proc in enumerate(memory_hogs[:10]):
            print(f"   {i+1}. {proc['name']}: {proc['memory_mb']}MB ({proc['memory_percent']}%)")
            
        # Cleanup safe processes
        print("\n🧹 CLEANING UP SAFE PROCESSES:")
        killed = self.cleanup_safe_processes()
        if killed:
            print(f"   ✅ Terminated: {', '.join(killed)}")
        else:
            print("   ℹ️ No safe processes to clean")
            
        # Show recommendations
        print("\n💡 MANUAL CLEANUP RECOMMENDATIONS:")
        recommendations = self.recommend_closures()
        for rec in recommendations:
            print(f"   {rec}")
            
        # Wait for cleanup to take effect
        time.sleep(2)
        
        # Show final memory usage
        memory_after = self.get_memory_usage()
        print(f"\n💾 Memory After: {memory_after['used_gb']}GB / {memory_after['total_gb']}GB ({memory_after['percent']}%)")
        
        memory_freed = memory_before['used_gb'] - memory_after['used_gb']
        if memory_freed > 0:
            print(f"✅ Freed: {memory_freed:.2f}GB of memory!")
        else:
            print("ℹ️ Memory usage stable")
            
        print("\n🔥 CLEANUP COMPLETE!")

def main():
    """Run system cleanup"""
    cleanup = ThorSystemCleanup()
    cleanup.full_cleanup()
    
    print("\n🚀 READY FOR THOR-AI DOMINATION!")

if __name__ == "__main__":
    main()
