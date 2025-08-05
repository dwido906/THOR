#!/bin/bash

# Quick ODIN OS ISO Builder for Vultr
# Simplified version for immediate deployment
# Creates a minimal ODIN OS with DWIDO AI for testing

set -e

ISO_NAME="odin-dwido-minimal"
ISO_VERSION="1.0.0"
BUILD_DIR="minimal_iso_build"
ISO_OUTPUT="$ISO_NAME-$ISO_VERSION.iso"

echo "🚀 Quick ODIN OS + DWIDO AI ISO Builder"
echo "======================================"

# Check if we have basic tools
if ! command -v genisoimage &> /dev/null && ! command -v mkisofs &> /dev/null; then
    echo "❌ Missing ISO creation tools"
    echo "Install with: brew install cdrtools (macOS) or sudo apt install genisoimage (Linux)"
    exit 1
fi

# Clean previous build
if [ -d "$BUILD_DIR" ]; then
    rm -rf "$BUILD_DIR"
fi

mkdir -p "$BUILD_DIR/iso"/{boot,system,dwido}

echo "📁 Creating ISO structure..."

# Create simple bootloader
cat > "$BUILD_DIR/iso/boot/grub.cfg" << 'EOF'
set timeout=5
set default=0

menuentry "ODIN OS + DWIDO AI" {
    linux /boot/vmlinuz root=/dev/ram0 init=/sbin/init
    initrd /boot/initrd.img
}

menuentry "ODIN OS Safe Mode" {
    linux /boot/vmlinuz root=/dev/ram0 init=/sbin/init single
    initrd /boot/initrd.img
}
EOF

# Create init system
cat > "$BUILD_DIR/iso/system/init" << 'EOF'
#!/bin/bash

echo "🧠 ODIN OS with DWIDO AI - Starting..."

# Mount essential filesystems
mount -t proc proc /proc
mount -t sysfs sysfs /sys
mount -t devtmpfs devtmpfs /dev

# Network setup
echo "🌐 Configuring network..."
dhclient eth0 &

# Start SSH
echo "🔑 Starting SSH server..."
/usr/sbin/sshd

# Create ODIN user
echo "👤 Creating ODIN user..."
useradd -m -s /bin/bash -G sudo odin
echo "odin:odin123" | chpasswd

# Start DWIDO AI
echo "🧠 Starting DWIDO AI..."
cd /opt/dwido && ./dwido start &

echo "✅ ODIN OS ready!"
echo "💻 Login: ssh odin@<server-ip> (password: odin123)"
echo "🧠 DWIDO AI: dwido status"

# Start shell
exec /bin/bash
EOF

chmod +x "$BUILD_DIR/iso/system/init"

# Copy DWIDO AI files
echo "🧠 Adding DWIDO AI to ISO..."
mkdir -p "$BUILD_DIR/iso/dwido"
cp dwido_ai.h "$BUILD_DIR/iso/dwido/"
cp dwido_ai.c "$BUILD_DIR/iso/dwido/"
cp dwido_ai_extended.c "$BUILD_DIR/iso/dwido/"
cp build_dwido_ai.sh "$BUILD_DIR/iso/dwido/"

# Create DWIDO installation script
cat > "$BUILD_DIR/iso/dwido/install_dwido.sh" << 'EOF'
#!/bin/bash
echo "🧠 Installing DWIDO AI..."

cd /tmp/dwido
chmod +x build_dwido_ai.sh
./build_dwido_ai.sh

# Simple installation
mkdir -p /opt/dwido
cp build/bin/dwido /opt/dwido/ 2>/dev/null || cp dwido /opt/dwido/
chmod +x /opt/dwido/dwido

echo "✅ DWIDO AI installed"
EOF

chmod +x "$BUILD_DIR/iso/dwido/install_dwido.sh"

# Create startup script
cat > "$BUILD_DIR/iso/boot/startup.sh" << 'EOF'
#!/bin/bash

echo "🚀 ODIN OS Boot Sequence Starting..."

# Basic system setup
export PATH="/bin:/sbin:/usr/bin:/usr/sbin"

# Install DWIDO AI
echo "📦 Installing DWIDO AI..."
cp -r /cdrom/dwido /tmp/
cd /tmp/dwido && ./install_dwido.sh

# Network configuration
echo "🌐 Setting up network..."
ip link set lo up
ip addr add 127.0.0.1/8 dev lo

# Start DWIDO AI
echo "🧠 Starting DWIDO AI Genesis System..."
/opt/dwido/dwido start &

echo "✅ ODIN OS with DWIDO AI is ready!"
echo ""
echo "🎯 Quick Commands:"
echo "   /opt/dwido/dwido status    # Check DWIDO AI status"
echo "   /opt/dwido/dwido mode gaming  # Switch to gaming mode"
echo "   /opt/dwido/dwido mode dev     # Switch to development mode"
echo ""
echo "🔐 Default credentials:"
echo "   Username: odin"
echo "   Password: odin123"
echo ""

# Start interactive shell
exec /bin/bash
EOF

chmod +x "$BUILD_DIR/iso/boot/startup.sh"

# Create simple kernel (busybox-based)
echo "🔧 Creating minimal kernel setup..."

# Download busybox if not present
if [ ! -f "busybox" ]; then
    echo "📦 Downloading BusyBox..."
    if command -v curl &> /dev/null; then
        curl -L -o busybox https://busybox.net/downloads/binaries/1.35.0-x86_64-linux-musl/busybox
    elif command -v wget &> /dev/null; then
        wget -O busybox https://busybox.net/downloads/binaries/1.35.0-x86_64-linux-musl/busybox
    else
        echo "❌ Need curl or wget to download busybox"
        exit 1
    fi
fi

chmod +x busybox
cp busybox "$BUILD_DIR/iso/boot/"

# Create minimal filesystem
mkdir -p "$BUILD_DIR/iso/system"/{bin,sbin,usr/bin,usr/sbin,lib,etc,tmp,var,home,root}

# Copy busybox and create symlinks
cp busybox "$BUILD_DIR/iso/system/bin/"
cd "$BUILD_DIR/iso/system/bin"
for cmd in sh bash ls cp mv rm mkdir rmdir cat less more grep sed awk ps kill; do
    ln -sf busybox $cmd
done
cd - > /dev/null

# Create essential config files
cat > "$BUILD_DIR/iso/system/etc/passwd" << 'EOF'
root:x:0:0:root:/root:/bin/bash
odin:x:1000:1000:ODIN User:/home/odin:/bin/bash
EOF

cat > "$BUILD_DIR/iso/system/etc/group" << 'EOF'
root:x:0:
sudo:x:27:odin
odin:x:1000:
EOF

# Create ISO image
echo "💿 Creating ISO image..."

if command -v genisoimage &> /dev/null; then
    genisoimage -r -J -b boot/startup.sh -c boot/boot.cat \
        -V "ODIN_OS_DWIDO" -o "$ISO_OUTPUT" "$BUILD_DIR/iso/"
elif command -v mkisofs &> /dev/null; then
    mkisofs -r -J -b boot/startup.sh -c boot/boot.cat \
        -V "ODIN_OS_DWIDO" -o "$ISO_OUTPUT" "$BUILD_DIR/iso/"
else
    # Fallback: create tar.gz
    echo "⚠️ No ISO tools found, creating tar.gz instead..."
    cd "$BUILD_DIR"
    tar -czf "../$ISO_NAME-$ISO_VERSION.tar.gz" iso/
    cd ..
    echo "📦 Created: $ISO_NAME-$ISO_VERSION.tar.gz"
    exit 0
fi

# Verify ISO
if [ -f "$ISO_OUTPUT" ]; then
    ISO_SIZE=$(ls -lh "$ISO_OUTPUT" | awk '{print $5}')
    echo ""
    echo "✅ ISO Created Successfully!"
    echo "📀 File: $ISO_OUTPUT"
    echo "📊 Size: $ISO_SIZE"
    echo ""
    echo "🚀 Vultr Deployment Steps:"
    echo "1. Upload $ISO_OUTPUT to Vultr ISOs section"
    echo "2. Create new server with uploaded ISO"
    echo "3. Boot and access via console or SSH"
    echo ""
    echo "🔐 Default Login:"
    echo "   Username: odin"
    echo "   Password: odin123"
    echo ""
    echo "🧠 DWIDO AI Commands:"
    echo "   /opt/dwido/dwido status"
    echo "   /opt/dwido/dwido mode gaming"
    echo "   /opt/dwido/dwido help"
    echo ""
    echo "✨ Ready for Vultr deployment!"
else
    echo "❌ ISO creation failed"
    exit 1
fi
