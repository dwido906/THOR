#!/usr/bin/env python3
"""
💳 SMS PRICING & SETUP GUIDE
Twilio pricing breakdown and setup instructions
"""

def sms_pricing_breakdown():
    """Explain SMS costs and setup"""
    
    print("💳 SMS PRICING BREAKDOWN")
    print("=" * 28)
    
    print("\n📱 TWILIO PRICING (Pay-per-use):")
    print("  💰 SMS (US/Canada): $0.0075 per message")
    print("  📞 Phone Number: $1.00/month")
    print("  🌍 International SMS: $0.05-0.20 per message")
    
    print("\n📊 MONTHLY ESTIMATES:")
    estimates = [
        ("Light usage (50 SMS/month)", 50, 0.0075),
        ("Medium usage (200 SMS/month)", 200, 0.0075),
        ("Heavy usage (500 SMS/month)", 500, 0.0075),
        ("Business usage (1000 SMS/month)", 1000, 0.0075)
    ]
    
    for desc, count, price in estimates:
        monthly_cost = (count * price) + 1.00  # +$1 for phone number
        print(f"  • {desc}: ${monthly_cost:.2f}/month")
        
    print("\n🚀 SETUP INSTRUCTIONS:")
    print("1. Sign up at twilio.com/try-twilio")
    print("2. Get $15 free credit (covers ~2000 messages)")
    print("3. Buy a phone number ($1/month)")
    print("4. Get your Account SID and Auth Token")
    print("5. Add to environment variables:")
    print("   export TWILIO_ACCOUNT_SID='your_account_sid'")
    print("   export TWILIO_AUTH_TOKEN='your_auth_token'")
    print("   export TWILIO_PHONE_NUMBER='+1234567890'")
    
    print("\n💡 COST OPTIMIZATION:")
    print("  ✅ Only send critical alerts")
    print("  ✅ Use email for non-urgent updates")
    print("  ✅ Batch multiple updates into one SMS")
    print("  ✅ Set up SMS budget alerts")
    
    print("\n🎯 FOR THOR-AI BUSINESS:")
    print("  📈 Revenue alerts: Essential ($5-10/month)")
    print("  🚨 System alerts: Critical ($3-5/month)")
    print("  💰 Deal notifications: High value ($2-3/month)")
    print("  📊 Total estimated cost: $10-18/month")
    print("  💵 ROI: Alerts help catch issues = Save $$$")

def main():
    sms_pricing_breakdown()
    
    print("\n🔗 QUICK SETUP LINKS:")
    print("📱 Twilio: https://twilio.com/try-twilio")
    print("💰 Pricing: https://twilio.com/sms/pricing")
    print("📚 Docs: https://twilio.com/docs/sms")

if __name__ == "__main__":
    main()
