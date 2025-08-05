
🌐 CLOUDFLARE DNS SETUP GUIDE

Why Cloudflare?
✅ Free DNS management
✅ Faster propagation
✅ Better reliability than Vultr DNS
✅ Advanced features (CDN, security)
✅ Easy API management

SETUP STEPS:

1. 📧 Create Cloudflare Account
   - Go to cloudflare.com
   - Sign up with dwido906@gmail.com
   - Verify email

2. 🌐 Add Domain
   - Click "Add a site"
   - Enter: northbaystudios.io
   - Choose Free plan

3. 📝 Import DNS Records
   Cloudflare will scan and import existing records
   Verify these records:
   
   Type    Name    Content
   A       @       207.246.95.179
   A       www     207.246.95.179
   A       mail    207.246.95.179
   MX      @       mail.northbaystudios.io (Priority: 10)
   TXT     @       v=spf1 include:_spf.google.com ~all

4. 🔧 Update Nameservers
   Cloudflare will provide nameservers like:
   - ava.ns.cloudflare.com
   - leo.ns.cloudflare.com
   
   Update these in your domain registrar (not Vultr)

5. ✅ Verify Setup
   - Wait 24 hours for propagation
   - Test: nslookup northbaystudios.io
   - Verify website loads

6. 🚀 Enable Features
   - SSL/TLS: Full (strict)
   - Always Use HTTPS: On
   - Minify: CSS, HTML, JS
   - Brotli: On

BENEFITS:
💰 Cost: FREE (vs Vultr DNS complexity)
⚡ Speed: Faster propagation
🛡️ Security: DDoS protection
📊 Analytics: Traffic insights
🔧 API: Easy automation
        