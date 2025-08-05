#!/usr/bin/env python3
"""
THOR AI DEMO - Shows full functionality with established reputation
"""

import sys
sys.path.append('/Users/dwido/TRINITY')

from trinity_unified import ThorAI, HearthGateReputation
import time

def demo_thor_ai():
    """Demo THOR AI with established reputation to show full functionality"""
    print("🚀 THOR AI DEMONSTRATION")
    print("=" * 60)
    
    # Initialize THOR
    thor = ThorAI()
    
    # Boost initial reputation for demo purposes (simulating an established user)
    print("🛡️ Setting up established user reputation for demo...")
    thor.hearthgate.gate_score = 5000  # Good standing user
    
    # Also update the contribution tracker's hearthgate reference
    thor.contribution_tracker.hearthgate.gate_score = 5000
    
    # Add some initial contribution history to show the system working
    print("🤝 Adding sample contribution history...")
    sample_users = ["dev_001", "gamer_pro", "content_creator", "beta_tester"]
    
    for i, user_id in enumerate(sample_users):
        # Various types of contributions
        contrib_types = [
            ("cpu", 4, 8),
            ("memory", 8, 6),
            ("development", 1, 4),
            ("gpu", 2, 12)
        ]
        
        for contrib_type, amount, duration in contrib_types:
            result = thor.process_user_contribution(user_id, contrib_type, amount, duration)
            if result:
                print(f"   ✅ {user_id}: {contrib_type} contribution registered (+{result['hearthgate_points']} points)")
    
    # Setup some FIVERR gigs
    print("\n🎯 Setting up FIVERR automation...")
    thor.fiverr_automation.auto_create_gigs()
    
    # Show initial status
    print(f"\n📊 DEMO SETUP COMPLETE:")
    status = thor.get_thor_comprehensive_status()
    print(f"   🛡️ HEARTHGATE: ⭐{status['hearthgate'].get('gate_score', 0)}/10,000")
    print(f"   🎯 FIVERR: {status['fiverr_automation']['active_gigs']} active gigs")
    print(f"   🤝 Contributions: {status['resource_contributions']['total_contributions']} processed")
    print(f"   🧠 THOR Memory: {status['thor_memory']['total_memories']} experiences")
    
    # Run a few demonstration cycles
    print(f"\n🎯 RUNNING THOR DEMONSTRATION CYCLES")
    print("=" * 60)
    
    results = []
    
    for cycle in range(1, 4):  # 3 demo cycles
        print(f"\n🔄 DEMO CYCLE {cycle}/3")
        print("-" * 40)
        
        # Run complete cycle
        cycle_result = thor.run_thor_complete_cycle()
        
        if cycle_result.get('status') != 'denied':
            results.append(cycle_result)
            
            # Show cycle summary
            print(f"\n📊 CYCLE {cycle} RESULTS:")
            print(f"   💰 Revenue: ${cycle_result['revenue']['current']:,.0f} ({cycle_result['revenue']['percentage']:.1f}%)")
            print(f"   🎯 FIVERR: {cycle_result['fiverr']['completed_projects']} projects completed")
            print(f"   👥 Community: +{cycle_result['acquisition']['community_conversions']} conversions")
            print(f"   🤝 Contributions: {cycle_result['contributions']['processed']} processed")
            print(f"   🧠 THOR Memories: {cycle_result['thor_memory_entries']} total")
            
            # Show some of THOR's learned insights
            if thor.thor_memory.get('insights'):
                print(f"   💡 Latest Insight: {thor.thor_memory['insights'][-1]['event']}")
        
        time.sleep(2)  # Brief pause between cycles
    
    # Final comprehensive report
    if results:
        final_status = thor.get_thor_comprehensive_status()
        
        print(f"\n🏁 THOR AI DEMONSTRATION COMPLETE")
        print("=" * 60)
        print(f"💰 Final Revenue: ${final_status['revenue']['current']:,.0f}")
        print(f"🎯 FIVERR Revenue: ${final_status['fiverr_automation']['total_revenue']:,.0f}")
        print(f"🛡️ HEARTHGATE Score: ⭐{final_status['hearthgate'].get('gate_score', 0)}/10,000")
        print(f"🤝 Total Contributions: {final_status['resource_contributions']['total_value_score']:,} value")
        print(f"🧠 THOR Memory Bank: {final_status['thor_memory']['total_memories']} learned experiences")
        print(f"🎮 Gaming Integration: {'✅ ACTIVE' if final_status['integration_health']['hearthgate_connected'] else '❌ OFFLINE'}")
        print(f"🎯 FIVERR Automation: {'✅ ACTIVE' if final_status['integration_health']['fiverr_active'] else '❌ OFFLINE'}")
        print(f"🤝 Contribution Tracking: {'✅ ACTIVE' if final_status['integration_health']['contributions_tracking'] else '❌ OFFLINE'}")
        
        # Show THOR's learning progression
        print(f"\n🧠 THOR's LEARNING PROGRESSION:")
        for category, memories in thor.thor_memory.items():
            if memories:
                print(f"   📚 {category.title()}: {len(memories)} experiences")
                if category == 'insights' and memories:
                    print(f"      💡 Latest: {memories[-1]['event']}")
        
        # Show resource contribution leaderboard
        print(f"\n🏆 TOP CONTRIBUTORS:")
        for user_id in sample_users[:3]:
            summary = thor.contribution_tracker.get_contributor_summary(user_id)
            if summary.get('tier'):
                print(f"   🥇 {user_id}: {summary['tier']} ({summary['lifetime_points']} points)")
                print(f"      🎁 Privileges: {summary['privileges'][:50]}...")
        
        print(f"\n✨ THOR AI is fully operational and learning from every interaction!")
        print(f"🎮 Bad actors can't use THOR due to HEARTHGATE reputation requirements")
        print(f"🎯 FIVERR automation generates passive income while THOR learns")
        print(f"🤝 Resource contributions power the network while rewarding users")
        print(f"🧠 THOR remembers everything and gets smarter with each cycle")
        
    else:
        print("❌ Demo failed - no successful cycles completed")

if __name__ == "__main__":
    demo_thor_ai()
