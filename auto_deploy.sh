#!/bin/bash
# 🤖 TRINITY AI AUTO-DEPLOYMENT
# Automatically deploy to server without manual intervention

echo "🚀 TRINITY AI Auto-Deployment Starting..."

# Copy deployment script to server
echo "📄 Uploading deployment script..."
scp deploy_server.sh northbay-server:/tmp/

# Execute deployment on server
echo "⚡ Executing deployment..."
ssh northbay-server "bash /tmp/deploy_server.sh"

# Verify deployment
echo "✅ Verifying deployment..."
ssh northbay-server "systemctl status northbaystudios"

echo "🎮 Auto-deployment complete!"
