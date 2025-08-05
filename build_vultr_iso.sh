#!/bin/bash

# ODIN OS with DWIDO AI - Vultr ISO Builder
# Creates bootable ISO for Vultr baremetal deployment
# 
# This script builds a complete ODIN GAMER/DEV OS ISO with DWIDO AI
# Ready for upload to Vultr and baremetal server deployment

set -e  # Exit on any error

# Build configuration
ISO_NAME="odin-dwido-ai"
ISO_VERSION="1.0.0"
ISO_CODENAME="Genesis"
BUILD_DIR="vultr_iso_build"
ISO_OUTPUT="$ISO_NAME-$ISO_VERSION.iso"

# System configuration
KERNEL_VERSION="6.8.0"
ARCH="x86_64"
ROOT_SIZE="8192"  # 8GB root filesystem
SWAP_SIZE="2048"  # 2GB swap

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_section() {
    echo -e "\n${PURPLE}=== $1 ===${NC}"
}

# Header
echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════════╗"
echo "║        ODIN OS + DWIDO AI ISO Builder                ║"
echo "║        Vultr Baremetal Deployment Ready              ║"
echo "║        Version: $ISO_VERSION \"$ISO_CODENAME\"                        ║"
echo "╚══════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   log_error "This script should not be run as root for security reasons"
   log_info "Please run as regular user with sudo access"
   exit 1
fi

# Check dependencies
log_section "Dependency Check"

check_dependency() {
    if command -v $1 &> /dev/null; then
        log_success "$1 found"
        return 0
    else
        log_error "$1 not found"
        return 1
    fi
}

DEPS_OK=true

# Essential dependencies for ISO creation
if ! check_dependency debootstrap; then DEPS_OK=false; fi
if ! check_dependency xorriso; then DEPS_OK=false; fi
if ! check_dependency grub-mkrescue; then DEPS_OK=false; fi
if ! check_dependency mksquashfs; then DEPS_OK=false; fi
if ! check_dependency chroot; then DEPS_OK=false; fi

# Check for sudo access
if ! sudo -n true 2>/dev/null; then
    log_warning "Sudo access required for some operations"
    log_info "You may be prompted for password during build"
fi

if ! $DEPS_OK; then
    log_error "Missing essential dependencies"
    log_info "Install with: sudo apt update && sudo apt install debootstrap xorriso grub-pc-bin grub-efi-amd64-bin squashfs-tools"
    exit 1
fi

# Clean previous build
log_section "Build Environment Setup"

if [ -d "$BUILD_DIR" ]; then
    log_warning "Cleaning existing build directory"
    sudo rm -rf "$BUILD_DIR"
fi

mkdir -p "$BUILD_DIR"/{chroot,iso,work}
mkdir -p "$BUILD_DIR/iso/boot/grub"
mkdir -p "$BUILD_DIR/iso/live"

log_success "Build directories created"

# Create base Debian system
log_section "Creating Base System"

log_info "Bootstrapping Debian base system..."
sudo debootstrap --arch=amd64 --variant=minbase bookworm \
    "$BUILD_DIR/chroot" http://deb.debian.org/debian/

log_success "Base system created"

# Configure base system
log_info "Configuring base system..."

# Create hostname
echo "odin-dwido" | sudo tee "$BUILD_DIR/chroot/etc/hostname" > /dev/null

# Create hosts file
sudo tee "$BUILD_DIR/chroot/etc/hosts" > /dev/null << EOF
127.0.0.1   localhost
127.0.1.1   odin-dwido
::1         localhost ip6-localhost ip6-loopback
ff02::1     ip6-allnodes
ff02::2     ip6-allrouters
EOF

# Create fstab
sudo tee "$BUILD_DIR/chroot/etc/fstab" > /dev/null << EOF
# ODIN OS Filesystem Table
UUID=odin-root /               ext4    defaults        0       1
UUID=odin-swap none            swap    sw              0       0
tmpfs          /tmp            tmpfs   defaults        0       0
EOF

# Configure network with DHCP
sudo mkdir -p "$BUILD_DIR/chroot/etc/systemd/network"
sudo tee "$BUILD_DIR/chroot/etc/systemd/network/20-dhcp.network" > /dev/null << EOF
[Match]
Name=en*

[Network]
DHCP=yes
EOF

log_success "Base system configured"

# Install essential packages
log_section "Installing Essential Packages"

# Create package installation script
sudo tee "$BUILD_DIR/chroot/install_packages.sh" > /dev/null << 'EOF'
#!/bin/bash
export DEBIAN_FRONTEND=noninteractive

# Update package lists
apt update

# Install kernel and bootloader
apt install -y linux-image-amd64 linux-headers-amd64 grub-pc grub-efi-amd64

# Install essential system packages
apt install -y \
    systemd systemd-sysv init \
    network-manager openssh-server \
    sudo curl wget nano vim \
    build-essential gcc g++ make \
    git python3 python3-pip \
    htop neofetch \
    firmware-linux firmware-linux-nonfree

# Install development tools for DWIDO AI
apt install -y \
    libc6-dev libpthread-stubs0-dev \
    pkg-config cmake autotools-dev \
    libssl-dev libcurl4-openssl-dev

# Install gaming-related packages
apt install -y \
    mesa-utils libgl1-mesa-dri \
    vulkan-tools mesa-vulkan-drivers \
    steam-installer

# Install NVIDIA drivers (if needed)
apt install -y nvidia-driver nvidia-cuda-toolkit || true

# Clean package cache
apt autoremove -y
apt autoclean
EOF

sudo chmod +x "$BUILD_DIR/chroot/install_packages.sh"

log_info "Installing packages in chroot..."
sudo chroot "$BUILD_DIR/chroot" /install_packages.sh

log_success "Essential packages installed"

# Create ODIN user and configure system
log_section "User and System Configuration"

sudo tee "$BUILD_DIR/chroot/configure_system.sh" > /dev/null << 'EOF'
#!/bin/bash

# Create ODIN user
useradd -m -s /bin/bash -G sudo,audio,video,plugdev odin
echo "odin:odin123" | chpasswd

# Create DWIDO service user
useradd -r -s /bin/false -d /opt/dwido dwido

# Configure sudo
echo "odin ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/odin

# Enable essential services
systemctl enable systemd-networkd
systemctl enable systemd-resolved
systemctl enable ssh
systemctl enable NetworkManager

# Configure SSH
sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Set timezone
ln -sf /usr/share/zoneinfo/UTC /etc/localtime

# Generate locales
echo "en_US.UTF-8 UTF-8" > /etc/locale.gen
locale-gen
echo "LANG=en_US.UTF-8" > /etc/locale.conf

# Configure kernel parameters for gaming
echo "vm.swappiness=10" >> /etc/sysctl.conf
echo "kernel.sched_migration_cost_ns=5000000" >> /etc/sysctl.conf
echo "kernel.sched_autogroup_enabled=0" >> /etc/sysctl.conf

# Create ODIN OS info
cat > /etc/os-release << EOL
NAME="ODIN GAMER/DEV OS"
VERSION="1.0.0 (Genesis)"
ID=odin
ID_LIKE=debian
VERSION_CODENAME=Genesis
PRETTY_NAME="ODIN GAMER/DEV OS 1.0.0"
HOME_URL="https://odin-os.com/"
SUPPORT_URL="https://odin-os.com/support"
BUG_REPORT_URL="https://odin-os.com/bugs"
EOL
EOF

sudo chmod +x "$BUILD_DIR/chroot/configure_system.sh"
sudo chroot "$BUILD_DIR/chroot" /configure_system.sh

log_success "System configuration complete"

# Build and install DWIDO AI
log_section "Building DWIDO AI"

log_info "Copying DWIDO AI source to chroot..."

# Copy DWIDO AI files
sudo cp dwido_ai.h "$BUILD_DIR/chroot/tmp/"
sudo cp dwido_ai.c "$BUILD_DIR/chroot/tmp/"
sudo cp dwido_ai_extended.c "$BUILD_DIR/chroot/tmp/"
sudo cp build_dwido_ai.sh "$BUILD_DIR/chroot/tmp/"

# Create DWIDO build script for chroot
sudo tee "$BUILD_DIR/chroot/build_dwido.sh" > /dev/null << 'EOF'
#!/bin/bash
cd /tmp

# Make build script executable
chmod +x build_dwido_ai.sh

# Run DWIDO AI build
./build_dwido_ai.sh

# Install DWIDO AI
if [ -f "build/dwido-ai_1.0.0_amd64.deb" ]; then
    dpkg -i build/dwido-ai_1.0.0_amd64.deb || apt-get install -f -y
elif [ -d "build/bin" ]; then
    # Manual installation if package failed
    mkdir -p /opt/dwido/{bin,lib,config}
    cp build/bin/dwido /opt/dwido/bin/
    cp build/lib/libdwido.a /opt/dwido/lib/
    cp build/config/dwido.conf /opt/dwido/config/
    
    # Create systemd service
    cp build/config/dwido.service /etc/systemd/system/
    
    # Set permissions
    chown -R dwido:dwido /opt/dwido
    chmod +x /opt/dwido/bin/dwido
    
    # Enable service
    systemctl daemon-reload
    systemctl enable dwido.service
fi

# Clean up build files
rm -rf /tmp/build /tmp/dwido_ai* /tmp/build_dwido_ai.sh
EOF

sudo chmod +x "$BUILD_DIR/chroot/build_dwido.sh"

log_info "Building DWIDO AI in chroot environment..."
sudo chroot "$BUILD_DIR/chroot" /build_dwido.sh

log_success "DWIDO AI built and installed"

# Install desktop environment (lightweight)
log_section "Installing Desktop Environment"

sudo tee "$BUILD_DIR/chroot/install_desktop.sh" > /dev/null << 'EOF'
#!/bin/bash
export DEBIAN_FRONTEND=noninteractive

# Install lightweight desktop
apt update
apt install -y \
    xfce4 xfce4-goodies \
    lightdm lightdm-gtk-greeter \
    firefox-esr \
    thunar-archive-plugin \
    pulseaudio pavucontrol \
    network-manager-gnome

# Install gaming tools
apt install -y \
    lutris steam \
    gamemode mangohud \
    wine winetricks

# Enable desktop services
systemctl enable lightdm

# Configure auto-login for ODIN user
cat > /etc/lightdm/lightdm.conf << EOL
[Seat:*]
autologin-user=odin
autologin-user-timeout=0
user-session=xfce
EOL

# Create desktop shortcut for DWIDO AI
mkdir -p /home/odin/Desktop
cat > /home/odin/Desktop/DWIDO-AI.desktop << EOL
[Desktop Entry]
Version=1.0
Type=Application
Name=DWIDO AI
Comment=Genesis Intelligence System
Exec=gnome-terminal -- /opt/dwido/bin/dwido start
Icon=applications-development
Terminal=false
Categories=Development;Science;AI;
EOL

chmod +x /home/odin/Desktop/DWIDO-AI.desktop
chown odin:odin /home/odin/Desktop/DWIDO-AI.desktop
EOF

sudo chmod +x "$BUILD_DIR/chroot/install_desktop.sh"
sudo chroot "$BUILD_DIR/chroot" /install_desktop.sh

log_success "Desktop environment installed"

# Create Vultr cloud-init configuration
log_section "Vultr Cloud-Init Configuration"

sudo mkdir -p "$BUILD_DIR/chroot/etc/cloud"
sudo tee "$BUILD_DIR/chroot/etc/cloud/cloud.cfg" > /dev/null << 'EOF'
# ODIN OS Cloud Configuration for Vultr
users:
  - default
  - name: odin
    gecos: ODIN User
    sudo: ['ALL=(ALL) NOPASSWD:ALL']
    groups: [sudo, audio, video, plugdev]
    shell: /bin/bash

disable_root: true
ssh_pwauth: true

package_update: true
package_upgrade: false

runcmd:
  - systemctl start dwido.service
  - echo "ODIN OS deployed on Vultr - $(date)" >> /var/log/odin-deployment.log
  - /opt/dwido/bin/dwido status >> /var/log/odin-deployment.log

final_message: "ODIN GAMER/DEV OS with DWIDO AI is ready for use!"
EOF

# Install cloud-init
sudo chroot "$BUILD_DIR/chroot" apt install -y cloud-init

log_success "Vultr configuration created"

# Clean up chroot
log_section "Cleaning Up Chroot"

sudo rm -f "$BUILD_DIR/chroot/install_packages.sh"
sudo rm -f "$BUILD_DIR/chroot/configure_system.sh"
sudo rm -f "$BUILD_DIR/chroot/build_dwido.sh"
sudo rm -f "$BUILD_DIR/chroot/install_desktop.sh"

# Clean package cache and temporary files
sudo chroot "$BUILD_DIR/chroot" apt autoremove -y
sudo chroot "$BUILD_DIR/chroot" apt autoclean
sudo rm -rf "$BUILD_DIR/chroot/tmp/"*
sudo rm -rf "$BUILD_DIR/chroot/var/cache/apt/"*

log_success "Chroot cleaned"

# Create squashfs filesystem
log_section "Creating Compressed Filesystem"

log_info "Creating squashfs filesystem..."
sudo mksquashfs "$BUILD_DIR/chroot" "$BUILD_DIR/iso/live/filesystem.squashfs" \
    -comp xz -b 1M -Xdict-size 100% \
    -e boot

log_success "Squashfs filesystem created"

# Create boot configuration
log_section "Creating Boot Configuration"

# Copy kernel and initrd
sudo cp "$BUILD_DIR/chroot/boot/vmlinuz-"* "$BUILD_DIR/iso/boot/vmlinuz"
sudo cp "$BUILD_DIR/chroot/boot/initrd.img-"* "$BUILD_DIR/iso/boot/initrd.img"

# Create GRUB configuration
sudo tee "$BUILD_DIR/iso/boot/grub/grub.cfg" > /dev/null << EOF
set timeout=5
set default=0

menuentry "ODIN GAMER/DEV OS ($ISO_VERSION)" {
    linux /boot/vmlinuz boot=live quiet splash
    initrd /boot/initrd.img
}

menuentry "ODIN OS - Safe Mode" {
    linux /boot/vmlinuz boot=live single
    initrd /boot/initrd.img
}

menuentry "Memory Test" {
    linux16 /boot/memtest86+.bin
}
EOF

# Create BIOS/UEFI boot support
sudo mkdir -p "$BUILD_DIR/iso/EFI/BOOT"
sudo cp /usr/lib/grub/x86_64-efi/grubx64.efi "$BUILD_DIR/iso/EFI/BOOT/BOOTX64.EFI" 2>/dev/null || true

log_success "Boot configuration created"

# Create ISO metadata
sudo mkdir -p "$BUILD_DIR/iso/.disk"
sudo tee "$BUILD_DIR/iso/.disk/info" > /dev/null << EOF
ODIN GAMER/DEV OS $ISO_VERSION "$ISO_CODENAME" - Release amd64
EOF

echo "ODIN_OS" | sudo tee "$BUILD_DIR/iso/.disk/id" > /dev/null

# Generate ISO
log_section "Generating ISO Image"

log_info "Creating bootable ISO image..."

# Create hybrid ISO with BIOS and UEFI support
sudo grub-mkrescue -o "$ISO_OUTPUT" "$BUILD_DIR/iso" \
    --volid "ODIN_OS_$ISO_VERSION" \
    2>/dev/null || sudo xorriso -as mkisofs \
    -r -V "ODIN_OS_$ISO_VERSION" \
    -cache-inodes -J -l \
    -b boot/grub/grub_eltorito \
    -no-emul-boot -boot-load-size 4 -boot-info-table \
    -eltorito-alt-boot -e EFI/BOOT/BOOTX64.EFI -no-emul-boot \
    -o "$ISO_OUTPUT" "$BUILD_DIR/iso/"

log_success "ISO image created: $ISO_OUTPUT"

# Verify ISO
log_section "ISO Verification"

if [ -f "$ISO_OUTPUT" ]; then
    ISO_SIZE=$(ls -lh "$ISO_OUTPUT" | awk '{print $5}')
    ISO_MD5=$(md5sum "$ISO_OUTPUT" | awk '{print $1}')
    
    log_success "✓ ISO file exists: $ISO_OUTPUT ($ISO_SIZE)"
    log_success "✓ MD5 checksum: $ISO_MD5"
    
    # Test ISO mountability
    if sudo mount -o loop "$ISO_OUTPUT" /mnt 2>/dev/null; then
        sudo umount /mnt
        log_success "✓ ISO is mountable"
    else
        log_warning "⚠ ISO mount test failed"
    fi
else
    log_error "✗ ISO file not created"
    exit 1
fi

# Create deployment instructions
log_section "Deployment Instructions"

cat > "${ISO_NAME}_vultr_deployment.txt" << EOF
ODIN OS + DWIDO AI - Vultr Deployment Instructions
==================================================

ISO File: $ISO_OUTPUT
Size: $ISO_SIZE
MD5: $ISO_MD5
Created: $(date)

Vultr Deployment Steps:
1. Upload ISO to Vultr:
   - Go to Vultr dashboard
   - Navigate to "ISOs" section
   - Click "Upload ISO"
   - Upload: $ISO_OUTPUT

2. Deploy Server:
   - Create new server instance
   - Select "Upload ISO" option
   - Choose uploaded ODIN OS ISO
   - Recommended specs:
     * CPU: 4+ cores
     * RAM: 8GB+ 
     * Storage: 80GB+ SSD

3. First Boot:
   - Server will boot from ISO
   - Auto-login as 'odin' user (password: odin123)
   - DWIDO AI will start automatically
   - SSH access available (change passwords!)

4. Post-Deployment:
   - Change default passwords immediately
   - Update system: sudo apt update && sudo apt upgrade
   - Configure firewall as needed
   - Start using DWIDO AI: dwido status

Default Credentials:
- Username: odin
- Password: odin123
- Root: disabled (use sudo)

DWIDO AI Commands:
- dwido start      # Start DWIDO AI
- dwido status     # Check status  
- dwido mode gaming    # Switch to gaming mode
- dwido mode dev       # Switch to development mode
- dwido mode research  # Switch to research mode

Network Configuration:
- DHCP enabled by default
- SSH server enabled
- Firewall: Not configured (configure as needed)

Security Notes:
- Change default passwords immediately
- Configure SSH keys for remote access
- Set up firewall rules
- Keep system updated

Support:
For technical support, refer to ODIN OS documentation.
EOF

log_success "Deployment instructions created: ${ISO_NAME}_vultr_deployment.txt"

# Create verification script
cat > "verify_${ISO_NAME}.sh" << 'EOF'
#!/bin/bash
echo "ODIN OS ISO Verification"
echo "======================="

if [ ! -f "$1" ]; then
    echo "Usage: $0 <iso_file>"
    exit 1
fi

ISO_FILE="$1"

echo "File: $ISO_FILE"
echo "Size: $(ls -lh "$ISO_FILE" | awk '{print $5}')"
echo "MD5: $(md5sum "$ISO_FILE" | awk '{print $1}')"

# Check if ISO is hybrid
if file "$ISO_FILE" | grep -q "DOS/MBR boot sector"; then
    echo "✓ Hybrid ISO (BIOS/UEFI compatible)"
else
    echo "⚠ Not a hybrid ISO"
fi

# Check filesystem
if 7z l "$ISO_FILE" >/dev/null 2>&1; then
    echo "✓ ISO filesystem accessible"
else
    echo "⚠ ISO filesystem check failed"
fi

echo ""
echo "Ready for Vultr upload!"
EOF

chmod +x "verify_${ISO_NAME}.sh"

# Final summary
log_section "Build Complete"

echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════════╗"
echo "║              ODIN OS ISO BUILD SUCCESSFUL            ║"
echo "╚══════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo "📀 ISO Details:"
echo "   File: $ISO_OUTPUT"
echo "   Size: $ISO_SIZE"
echo "   MD5: $ISO_MD5"
echo ""
echo "🚀 Ready for Vultr Deployment:"
echo "   1. Upload ISO to Vultr dashboard"
echo "   2. Create server with uploaded ISO"
echo "   3. Boot and enjoy ODIN OS + DWIDO AI!"
echo ""
echo "📋 Files Created:"
echo "   - $ISO_OUTPUT (bootable ISO)"
echo "   - ${ISO_NAME}_vultr_deployment.txt (deployment guide)"
echo "   - verify_${ISO_NAME}.sh (verification script)"
echo ""
echo "🔐 Default Login:"
echo "   Username: odin"
echo "   Password: odin123"
echo "   (Change immediately after deployment!)"
echo ""
echo "🧠 DWIDO AI:"
echo "   Status: Integrated and auto-starting"
echo "   Access: dwido command or desktop shortcut"
echo ""
echo "✨ Your ODIN GAMER/DEV OS with DWIDO AI is ready for deployment!"

exit 0
