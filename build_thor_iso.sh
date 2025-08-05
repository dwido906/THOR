#!/bin/bash
# THOR OS - ONE MAN ARMY EDITION - ISO Builder
# Complete Gaming & Development Operating System

ISO_NAME="THOR_OS_ONE_MAN_ARMY_EDITION"
ISO_VERSION="2025.07.16"
ISO_DIR="/tmp/thor_iso_build"
ISO_OUTPUT="/tmp/${ISO_NAME}_${ISO_VERSION}.iso"

echo "🔨 Building THOR OS - ONE MAN ARMY EDITION ISO"
echo "Target: $ISO_OUTPUT"

# Create ISO build directory structure
mkdir -p ${ISO_DIR}/{boot,isolinux,casper,preseed,.disk}

# Create THOR OS kernel configuration
cat > ${ISO_DIR}/boot/thor_kernel_config << 'THOR_KERNEL_EOF'
# THOR OS Kernel Configuration
# Optimized for Gaming & Development

CONFIG_LOCALVERSION="-thor-onemanarray"
CONFIG_LOCALVERSION_AUTO=y
CONFIG_DEFAULT_HOSTNAME="thor-battlestation"

# Gaming optimizations
CONFIG_PREEMPT=y
CONFIG_PREEMPT_VOLUNTARY=n
CONFIG_PREEMPT_NONE=n
CONFIG_HZ_1000=y
CONFIG_NO_HZ_FULL=y
CONFIG_HIGH_RES_TIMERS=y

# Gaming hardware support
CONFIG_DRM_AMDGPU=y
CONFIG_DRM_I915=y
CONFIG_DRM_NOUVEAU=y
CONFIG_SND_HDA_INTEL=y
CONFIG_SND_HDA_CODEC_REALTEK=y
CONFIG_USB_XHCI_HCD=y
CONFIG_GAMING_INPUT_DEVICES=y

# Development tools
CONFIG_FTRACE=y
CONFIG_KPROBES=y
CONFIG_DEBUG_INFO=y
CONFIG_GDB_SCRIPTS=y

# Network gaming optimizations
CONFIG_NET_SCH_FQ=y
CONFIG_NET_SCH_FQ_CODEL=y
CONFIG_TCP_CONG_BBR=y

# File system optimizations
CONFIG_EXT4_FS=y
CONFIG_BTRFS_FS=y
CONFIG_XFS_FS=y
CONFIG_F2FS_FS=y

# Memory management for large games
CONFIG_TRANSPARENT_HUGEPAGE=y
CONFIG_COMPACTION=y
CONFIG_MIGRATION=y
CONFIG_KSM=y

# Power management for gaming laptops
CONFIG_CPU_FREQ_DEFAULT_GOV_PERFORMANCE=y
CONFIG_CPU_FREQ_GOV_ONDEMAND=y
CONFIG_CPU_FREQ_GOV_CONSERVATIVE=y
THOR_KERNEL_EOF

# Create THOR system initialization
cat > ${ISO_DIR}/casper/thor_init.sh << 'THOR_INIT_EOF'
#!/bin/bash
# THOR OS System Initialization
# The One Man Army Awakens

set -e

echo "⚡ THOR OS - ONE MAN ARMY EDITION INITIALIZING"
echo "🎮 Ultimate Gaming & Development Platform"

# Set hostname
echo "thor-battlestation" > /etc/hostname

# Create THOR user with gaming privileges
useradd -m -s /bin/bash -G sudo,audio,video,input,plugdev thor
echo "thor:mjolnir2025" | chpasswd
echo "thor ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Gaming system optimizations
echo "# THOR Gaming Optimizations" >> /etc/sysctl.conf
echo "vm.swappiness=10" >> /etc/sysctl.conf
echo "vm.vfs_cache_pressure=50" >> /etc/sysctl.conf
echo "net.core.netdev_max_backlog=16384" >> /etc/sysctl.conf
echo "net.core.somaxconn=8192" >> /etc/sysctl.conf
echo "net.core.rmem_default=1048576" >> /etc/sysctl.conf
echo "net.core.rmem_max=16777216" >> /etc/sysctl.conf
echo "net.core.wmem_default=1048576" >> /etc/sysctl.conf
echo "net.core.wmem_max=16777216" >> /etc/sysctl.conf
echo "net.ipv4.tcp_rmem=4096 1048576 2097152" >> /etc/sysctl.conf
echo "net.ipv4.tcp_wmem=4096 1048576 2097152" >> /etc/sysctl.conf
echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf

# Audio optimizations for gaming
echo "@audio - rtprio 95" >> /etc/security/limits.conf
echo "@audio - memlock unlimited" >> /etc/security/limits.conf

# Graphics driver preparation
mkdir -p /opt/thor/drivers
echo "#!/bin/bash" > /opt/thor/drivers/gpu_setup.sh
echo "# GPU Driver Auto-Detection and Installation" >> /opt/thor/drivers/gpu_setup.sh
echo "lspci | grep -E 'VGA|3D'" >> /opt/thor/drivers/gpu_setup.sh
chmod +x /opt/thor/drivers/gpu_setup.sh

# Gaming package repositories
echo "deb http://deb.debian.org/debian/ bookworm main contrib non-free" > /etc/apt/sources.list
echo "deb http://deb.debian.org/debian/ bookworm-updates main contrib non-free" >> /etc/apt/sources.list
echo "deb http://security.debian.org/debian-security bookworm-security main contrib non-free" >> /etc/apt/sources.list

# Steam repository
wget -O - https://repo.steampowered.com/steam/archive/stable/steam.gpg | apt-key add -
echo "deb [arch=amd64,i386] https://repo.steampowered.com/steam/ stable steam" > /etc/apt/sources.list.d/steam.list

# Development repositories
curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
echo "deb [arch=amd64] https://download.docker.com/linux/debian bookworm stable" > /etc/apt/sources.list.d/docker.list

curl -fsSL https://deb.nodesource.com/setup_20.x | bash -

# Update package database
apt update

echo "✅ THOR OS Base System Initialized"
echo "🎮 Ready for Gaming & Development Packages"
THOR_INIT_EOF

# Create THOR package installation script
cat > ${ISO_DIR}/casper/thor_packages.sh << 'THOR_PACKAGES_EOF'
#!/bin/bash
# THOR OS Package Installation
# Gaming & Development Software Suite

echo "📦 Installing THOR OS Software Suite..."

# Core system packages
apt install -y \
    linux-image-generic \
    linux-headers-generic \
    firmware-linux \
    firmware-linux-nonfree \
    intel-microcode \
    amd64-microcode

# Gaming essentials
apt install -y \
    steam-installer \
    lutris \
    wine \
    winetricks \
    playonlinux \
    gamemode \
    mangohud \
    goverlay \
    discord \
    obs-studio \
    ffmpeg

# Graphics and drivers
apt install -y \
    mesa-vulkan-drivers \
    vulkan-tools \
    nvidia-driver \
    nvidia-cuda-toolkit \
    amdgpu-pro \
    intel-gpu-tools

# Development tools
apt install -y \
    git \
    vim \
    neovim \
    emacs \
    code \
    docker-ce \
    docker-compose \
    nodejs \
    npm \
    python3 \
    python3-pip \
    golang \
    rust-all \
    openjdk-17-jdk \
    maven \
    gradle

# Gaming peripherals
apt install -y \
    joystick \
    jstest-gtk \
    antimicro \
    qjoypad \
    input-utils

# Audio production
apt install -y \
    pulseaudio \
    pavucontrol \
    audacity \
    ardour \
    lmms \
    jack-audio-connection-kit

# Streaming and content creation
apt install -y \
    kdenlive \
    blender \
    gimp \
    inkscape \
    krita \
    handbrake

# System monitoring and tweaking
apt install -y \
    htop \
    iotop \
    nethogs \
    lm-sensors \
    psensor \
    cpu-x \
    hardinfo \
    gparted

# Gaming performance tools
apt install -y \
    cpufrequtils \
    thermald \
    tlp \
    powertop \
    irqbalance

echo "✅ THOR OS Software Suite Installation Complete"
echo "🎮 System ready for epic gaming and development!"
THOR_PACKAGES_EOF

# Create THOR desktop environment
cat > ${ISO_DIR}/casper/thor_desktop.sh << 'THOR_DESKTOP_EOF'
#!/bin/bash
# THOR Desktop Environment Setup

echo "🖥️ Setting up THOR Gaming Desktop Environment"

# Install KDE Plasma (optimized for gaming)
apt install -y \
    kde-plasma-desktop \
    plasma-workspace \
    plasma-nm \
    dolphin \
    konsole \
    kate \
    spectacle \
    gwenview \
    okular

# Gaming-specific desktop customization
mkdir -p /home/thor/.config/plasma-org.kde.plasma.desktop-appletsrc
cat > /home/thor/.config/plasma-org.kde.plasma.desktop-appletsrc << 'PLASMA_EOF'
[Containments][1][Applets][1]
plugin=org.kde.plasma.applicationlauncher

[Containments][1][Applets][2]
plugin=org.kde.plasma.systemtray

[Containments][1][Applets][3]
plugin=org.kde.plasma.digitalclock

[Containments][1][Applets][4]
plugin=org.kde.plasma.systemmonitor.cpu

[Containments][1][Applets][5]
plugin=org.kde.plasma.systemmonitor.memory
PLASMA_EOF

# THOR wallpaper
mkdir -p /usr/share/pixmaps/thor
echo "# THOR Wallpaper would be here" > /usr/share/pixmaps/thor/wallpaper.jpg

# Gaming shortcuts
mkdir -p /home/thor/Desktop
cat > /home/thor/Desktop/Steam.desktop << 'STEAM_DESKTOP_EOF'
[Desktop Entry]
Name=Steam
Comment=Application for managing and playing games on Steam
Exec=steam %U
Icon=steam
Terminal=false
Type=Application
Categories=Network;FileTransfer;Game;
MimeType=x-scheme-handler/steam;
STEAM_DESKTOP_EOF

cat > /home/thor/Desktop/THOR-System-Monitor.desktop << 'MONITOR_DESKTOP_EOF'
[Desktop Entry]
Name=THOR System Monitor
Comment=Monitor your battlestation performance
Exec=htop
Icon=utilities-system-monitor
Terminal=true
Type=Application
Categories=System;Monitor;
MONITOR_DESKTOP_EOF

chown -R thor:thor /home/thor/Desktop
chmod +x /home/thor/Desktop/*.desktop

echo "✅ THOR Desktop Environment Ready"
THOR_DESKTOP_EOF

# Create isolinux boot configuration
cat > ${ISO_DIR}/isolinux/isolinux.cfg << 'ISOLINUX_EOF'
DEFAULT thor
TIMEOUT 300
PROMPT 1

LABEL thor
  MENU LABEL THOR OS - ONE MAN ARMY EDITION
  KERNEL /casper/vmlinuz
  APPEND initrd=/casper/initrd.img boot=casper quiet splash thor-mode=onemanarray

LABEL thorinstall
  MENU LABEL Install THOR OS to Hard Drive
  KERNEL /casper/vmlinuz
  APPEND initrd=/casper/initrd.img boot=casper only-ubiquity quiet splash

LABEL thormemtest
  MENU LABEL Memory Test
  KERNEL memtest86+

LABEL thorrescue
  MENU LABEL THOR Rescue Mode
  KERNEL /casper/vmlinuz
  APPEND initrd=/casper/initrd.img boot=casper rescue/enable=true
ISOLINUX_EOF

# Create disk info
echo "THOR OS - ONE MAN ARMY EDITION ${ISO_VERSION}" > ${ISO_DIR}/.disk/info
echo "https://northbaystudios.org" > ${ISO_DIR}/.disk/release_notes_url

# Create preseed for automated installation
cat > ${ISO_DIR}/preseed/thor.seed << 'PRESEED_EOF'
# THOR OS Automated Installation Configuration

d-i debian-installer/locale string en_US.UTF-8
d-i keyboard-configuration/xkb-keymap select us
d-i netcfg/choose_interface select auto
d-i netcfg/get_hostname string thor-battlestation
d-i netcfg/get_domain string local

d-i passwd/user-fullname string THOR User
d-i passwd/username string thor
d-i passwd/user-password password mjolnir2025
d-i passwd/user-password-again password mjolnir2025
d-i user-setup/allow-password-weak boolean true

d-i clock-setup/utc boolean true
d-i time/zone string US/Pacific

d-i partman-auto/method string regular
d-i partman-auto/choose_recipe select atomic
d-i partman/confirm_write_new_label boolean true
d-i partman/choose_partition select finish
d-i partman/confirm boolean true
d-i partman/confirm_nooverwrite boolean true

d-i grub-installer/only_debian boolean true
d-i grub-installer/with_other_os boolean true

d-i finish-install/reboot_in_progress note
PRESEED_EOF

echo "🔥 Creating THOR OS ISO image..."

# Generate ISO
genisoimage -r -V "THOR_OS_ONE_MAN_ARMY" \
    -cache-inodes -J -l \
    -b isolinux/isolinux.bin \
    -c isolinux/boot.cat \
    -no-emul-boot \
    -boot-load-size 4 \
    -boot-info-table \
    -o ${ISO_OUTPUT} \
    ${ISO_DIR}

# Make ISO bootable
isohybrid ${ISO_OUTPUT}

echo "✅ THOR OS ISO Creation Complete!"
echo "📁 ISO Location: ${ISO_OUTPUT}"
echo "💾 ISO Size: $(du -h ${ISO_OUTPUT} | cut -f1)"
echo "📊 Line Count: $(find ${ISO_DIR} -name "*.sh" -o -name "*.cfg" -o -name "*seed" | xargs wc -l | tail -1)"

echo ""
echo "🎮 THOR OS - ONE MAN ARMY EDITION Ready!"
echo "⚡ Boot this ISO to unleash the ultimate gaming battlestation"
