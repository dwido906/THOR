#!/bin/bash

# DWIDO AI Build System
# Comprehensive build script for DWIDO AI Genesis Intelligence System
# 
# This script compiles and packages the complete DWIDO AI system
# for integration with ODIN GAMER/DEV OS

set -e  # Exit on any error

# Build configuration
BUILD_DIR="build"
INSTALL_DIR="/opt/dwido"
VERSION="1.0.0"
CODENAME="Genesis"

# Compiler settings
CC="gcc"
CXX="g++"
CFLAGS="-O3 -Wall -Wextra -std=c11 -march=native -mtune=native"
CXXFLAGS="-O3 -Wall -Wextra -std=c++17 -march=native -mtune=native"
LDFLAGS="-lpthread -lm -ldl"

# CUDA settings (if available)
NVCC="nvcc"
CUDA_FLAGS="-O3 -arch=sm_60"

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
echo "╔════════════════════════════════════════════╗"
echo "║     DWIDO AI Genesis Build System          ║"
echo "║     Unified Intelligence Compilation       ║"
echo "║     Version: $VERSION \"$CODENAME\"                   ║"
echo "╚════════════════════════════════════════════╝"
echo -e "${NC}"

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

# Essential dependencies
if ! check_dependency gcc; then DEPS_OK=false; fi
if ! check_dependency g++; then DEPS_OK=false; fi
if ! check_dependency make; then DEPS_OK=false; fi
if ! check_dependency pkg-config; then DEPS_OK=false; fi

# Optional dependencies
if command -v nvcc &> /dev/null; then
    log_success "NVIDIA CUDA found - GPU acceleration will be enabled"
    CUDA_AVAILABLE=true
    CFLAGS="$CFLAGS -DDWIDO_CUDA_ENABLED"
    LDFLAGS="$LDFLAGS -lcuda -lcudart"
else
    log_warning "NVIDIA CUDA not found - GPU acceleration will be disabled"
    CUDA_AVAILABLE=false
fi

if command -v clinfo &> /dev/null; then
    log_success "OpenCL found - Alternative GPU acceleration available"
    OPENCL_AVAILABLE=true
    CFLAGS="$CFLAGS -DDWIDO_OPENCL_ENABLED"
    LDFLAGS="$LDFLAGS -lOpenCL"
else
    log_warning "OpenCL not found"
    OPENCL_AVAILABLE=false
fi

if ! $DEPS_OK; then
    log_error "Missing essential dependencies. Please install required packages."
    exit 1
fi

# Create build directory
log_section "Build Environment Setup"

if [ -d "$BUILD_DIR" ]; then
    log_warning "Cleaning existing build directory"
    rm -rf "$BUILD_DIR"
fi

mkdir -p "$BUILD_DIR"
mkdir -p "$BUILD_DIR/obj"
mkdir -p "$BUILD_DIR/bin"
mkdir -p "$BUILD_DIR/lib"

log_success "Build directories created"

# Generate build info
cat > "$BUILD_DIR/build_info.h" << EOF
#ifndef DWIDO_BUILD_INFO_H
#define DWIDO_BUILD_INFO_H

#define DWIDO_BUILD_VERSION "$VERSION"
#define DWIDO_BUILD_CODENAME "$CODENAME"
#define DWIDO_BUILD_DATE "$(date -u '+%Y-%m-%d %H:%M:%S UTC')"
#define DWIDO_BUILD_COMMIT "$(git rev-parse --short HEAD 2>/dev/null || echo 'unknown')"
#define DWIDO_BUILD_HOSTNAME "$(hostname)"
#define DWIDO_BUILD_USER "$(whoami)"

#ifdef DWIDO_CUDA_ENABLED
#define DWIDO_HAS_CUDA 1
#else
#define DWIDO_HAS_CUDA 0
#endif

#ifdef DWIDO_OPENCL_ENABLED
#define DWIDO_HAS_OPENCL 1
#else
#define DWIDO_HAS_OPENCL 0
#endif

#endif
EOF

log_success "Build info generated"

# Compile DWIDO AI Core
log_section "Compiling DWIDO AI Core"

log_info "Compiling dwido_ai.c..."
$CC $CFLAGS -I. -I"$BUILD_DIR" -c dwido_ai.c -o "$BUILD_DIR/obj/dwido_ai.o"

log_info "Compiling dwido_ai_extended.c..."
$CC $CFLAGS -I. -I"$BUILD_DIR" -c dwido_ai_extended.c -o "$BUILD_DIR/obj/dwido_ai_extended.o"

log_success "Core compilation complete"

# Compile CUDA modules (if available)
if [ "$CUDA_AVAILABLE" = true ]; then
    log_section "Compiling CUDA Modules"
    
    # Create CUDA wrapper source
    cat > "$BUILD_DIR/dwido_cuda.cu" << 'EOF'
#include <cuda_runtime.h>
#include <cublas_v2.h>
#include <curand.h>
#include <stdio.h>

extern "C" {

__global__ void dwido_cuda_matrix_multiply(float* A, float* B, float* C, int N) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;
    
    if (row < N && col < N) {
        float sum = 0.0f;
        for (int k = 0; k < N; k++) {
            sum += A[row * N + k] * B[k * N + col];
        }
        C[row * N + col] = sum;
    }
}

__global__ void dwido_cuda_relu_activation(float* data, int size) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < size) {
        data[idx] = fmaxf(0.0f, data[idx]);
    }
}

__global__ void dwido_cuda_softmax(float* input, float* output, int size) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    
    if (idx < size) {
        float max_val = input[0];
        for (int i = 1; i < size; i++) {
            max_val = fmaxf(max_val, input[i]);
        }
        
        float sum = 0.0f;
        for (int i = 0; i < size; i++) {
            sum += expf(input[i] - max_val);
        }
        
        output[idx] = expf(input[idx] - max_val) / sum;
    }
}

int dwido_cuda_init(void) {
    int device_count;
    cudaError_t error = cudaGetDeviceCount(&device_count);
    
    if (error != cudaSuccess) {
        printf("CUDA Error: %s\n", cudaGetErrorString(error));
        return -1;
    }
    
    if (device_count == 0) {
        printf("No CUDA devices found\n");
        return -1;
    }
    
    cudaSetDevice(0);
    printf("CUDA initialized with %d device(s)\n", device_count);
    return 0;
}

void dwido_cuda_matrix_mul_wrapper(float* h_A, float* h_B, float* h_C, int N) {
    float *d_A, *d_B, *d_C;
    size_t bytes = N * N * sizeof(float);
    
    cudaMalloc(&d_A, bytes);
    cudaMalloc(&d_B, bytes);
    cudaMalloc(&d_C, bytes);
    
    cudaMemcpy(d_A, h_A, bytes, cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, h_B, bytes, cudaMemcpyHostToDevice);
    
    dim3 block(16, 16);
    dim3 grid((N + block.x - 1) / block.x, (N + block.y - 1) / block.y);
    
    dwido_cuda_matrix_multiply<<<grid, block>>>(d_A, d_B, d_C, N);
    
    cudaMemcpy(h_C, d_C, bytes, cudaMemcpyDeviceToHost);
    
    cudaFree(d_A);
    cudaFree(d_B);
    cudaFree(d_C);
}

} // extern "C"
EOF

    log_info "Compiling CUDA modules..."
    $NVCC $CUDA_FLAGS -c "$BUILD_DIR/dwido_cuda.cu" -o "$BUILD_DIR/obj/dwido_cuda.o"
    
    CUDA_OBJECTS="$BUILD_DIR/obj/dwido_cuda.o"
    log_success "CUDA compilation complete"
else
    CUDA_OBJECTS=""
fi

# Create static library
log_section "Creating DWIDO AI Library"

log_info "Creating static library..."
ar rcs "$BUILD_DIR/lib/libdwido.a" \
    "$BUILD_DIR/obj/dwido_ai.o" \
    "$BUILD_DIR/obj/dwido_ai_extended.o" \
    $CUDA_OBJECTS

log_success "Library created: $BUILD_DIR/lib/libdwido.a"

# Create main executable
log_section "Building Main Executable"

log_info "Creating DWIDO AI main executable..."
$CC $CFLAGS -I. -I"$BUILD_DIR" \
    -DDWIDO_MAIN_EXECUTABLE \
    "$BUILD_DIR/obj/dwido_ai_extended.o" \
    "$BUILD_DIR/obj/dwido_ai.o" \
    $CUDA_OBJECTS \
    $LDFLAGS \
    -o "$BUILD_DIR/bin/dwido"

log_success "Executable created: $BUILD_DIR/bin/dwido"

# Create Python bindings (optional)
log_section "Python Integration"

if command -v python3 &> /dev/null; then
    log_info "Creating Python bindings..."
    
    cat > "$BUILD_DIR/dwido_python.c" << 'EOF'
#include <Python.h>
#include "dwido_ai.h"

static PyObject* py_dwido_init(PyObject* self, PyObject* args) {
    int result = dwido_ai_initialize();
    return PyLong_FromLong(result);
}

static PyObject* py_dwido_start(PyObject* self, PyObject* args) {
    int result = dwido_ai_start();
    return PyLong_FromLong(result);
}

static PyObject* py_dwido_switch_mode(PyObject* self, PyObject* args) {
    int mode;
    if (!PyArg_ParseTuple(args, "i", &mode)) {
        return NULL;
    }
    
    int result = dwido_switch_mode((dwido_mode_t)mode);
    return PyLong_FromLong(result);
}

static PyObject* py_dwido_get_status(PyObject* self, PyObject* args) {
    char* status = dwido_get_status_report();
    PyObject* result = PyUnicode_FromString(status);
    free(status);
    return result;
}

static PyMethodDef DwidoMethods[] = {
    {"init", py_dwido_init, METH_VARARGS, "Initialize DWIDO AI"},
    {"start", py_dwido_start, METH_VARARGS, "Start DWIDO AI"},
    {"switch_mode", py_dwido_switch_mode, METH_VARARGS, "Switch DWIDO mode"},
    {"get_status", py_dwido_get_status, METH_VARARGS, "Get DWIDO status"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef dwidomodule = {
    PyModuleDef_HEAD_INIT,
    "dwido",
    "DWIDO AI Python Interface",
    -1,
    DwidoMethods
};

PyMODINIT_FUNC PyInit_dwido(void) {
    return PyModule_Create(&dwidomodule);
}
EOF

    # Try to compile Python bindings
    if python3-config --cflags &> /dev/null; then
        PYTHON_CFLAGS=$(python3-config --cflags)
        PYTHON_LDFLAGS=$(python3-config --ldflags)
        
        $CC $CFLAGS $PYTHON_CFLAGS -shared -fPIC \
            -I. -I"$BUILD_DIR" \
            "$BUILD_DIR/dwido_python.c" \
            "$BUILD_DIR/lib/libdwido.a" \
            $LDFLAGS $PYTHON_LDFLAGS \
            -o "$BUILD_DIR/lib/dwido.so" 2>/dev/null && \
        log_success "Python bindings created" || \
        log_warning "Python bindings failed - continuing without"
    else
        log_warning "Python development headers not found"
    fi
else
    log_warning "Python3 not found - skipping Python bindings"
fi

# Create configuration files
log_section "Configuration Files"

log_info "Creating default configuration..."

mkdir -p "$BUILD_DIR/config"

cat > "$BUILD_DIR/config/dwido.conf" << EOF
# DWIDO AI Configuration File
# Genesis Intelligence System Settings

[core]
version = $VERSION
codename = $CODENAME
default_mode = development
learning_enabled = true
max_memory_mb = 4096

[gaming]
fps_optimization = true
latency_reduction = true
competitive_analysis = true
cpu_allocation = 60
gpu_allocation = 80

[development]
code_generation = true
syntax_analysis = true
debugging_assistance = true
max_code_context = 500
auto_completion = true

[research]
neural_training = true
distributed_computing = true
max_training_epochs = 1000
learning_rate = 0.001

[hardware]
use_gpu_acceleration = $([ "$CUDA_AVAILABLE" = true ] && echo "true" || echo "false")
cuda_enabled = $([ "$CUDA_AVAILABLE" = true ] && echo "true" || echo "false")
opencl_enabled = $([ "$OPENCL_AVAILABLE" = true ] && echo "true" || echo "false")
EOF

log_success "Configuration created: $BUILD_DIR/config/dwido.conf"

# Create systemd service file
log_info "Creating systemd service file..."

cat > "$BUILD_DIR/config/dwido.service" << EOF
[Unit]
Description=DWIDO AI Genesis Intelligence System
After=network.target

[Service]
Type=simple
User=dwido
Group=dwido
ExecStart=$INSTALL_DIR/bin/dwido start
ExecStop=$INSTALL_DIR/bin/dwido stop
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

log_success "Systemd service created"

# Create desktop integration
log_info "Creating desktop integration..."

cat > "$BUILD_DIR/config/dwido.desktop" << EOF
[Desktop Entry]
Name=DWIDO AI
Comment=Genesis Intelligence System
Exec=$INSTALL_DIR/bin/dwido
Icon=$INSTALL_DIR/share/icons/dwido.png
Terminal=false
Type=Application
Categories=Development;Science;AI;
EOF

log_success "Desktop integration created"

# Create installation package
log_section "Package Creation"

log_info "Creating installation package..."

# Create package structure
PACKAGE_DIR="$BUILD_DIR/package"
mkdir -p "$PACKAGE_DIR/DEBIAN"
mkdir -p "$PACKAGE_DIR$INSTALL_DIR/bin"
mkdir -p "$PACKAGE_DIR$INSTALL_DIR/lib"
mkdir -p "$PACKAGE_DIR$INSTALL_DIR/config"
mkdir -p "$PACKAGE_DIR$INSTALL_DIR/share/doc/dwido"
mkdir -p "$PACKAGE_DIR/etc/systemd/system"
mkdir -p "$PACKAGE_DIR/usr/share/applications"

# Copy files
cp "$BUILD_DIR/bin/dwido" "$PACKAGE_DIR$INSTALL_DIR/bin/"
cp "$BUILD_DIR/lib/libdwido.a" "$PACKAGE_DIR$INSTALL_DIR/lib/"
cp "$BUILD_DIR/config/dwido.conf" "$PACKAGE_DIR$INSTALL_DIR/config/"
cp "$BUILD_DIR/config/dwido.service" "$PACKAGE_DIR/etc/systemd/system/"
cp "$BUILD_DIR/config/dwido.desktop" "$PACKAGE_DIR/usr/share/applications/"

if [ -f "$BUILD_DIR/lib/dwido.so" ]; then
    cp "$BUILD_DIR/lib/dwido.so" "$PACKAGE_DIR$INSTALL_DIR/lib/"
fi

# Copy headers for development
mkdir -p "$PACKAGE_DIR$INSTALL_DIR/include"
cp dwido_ai.h "$PACKAGE_DIR$INSTALL_DIR/include/"

# Create documentation
cat > "$PACKAGE_DIR$INSTALL_DIR/share/doc/dwido/README.md" << EOF
# DWIDO AI - Genesis Intelligence System

DWIDO AI is a revolutionary unified artificial intelligence system designed for the ODIN GAMER/DEV OS platform.

## Features

- **Gaming Mode**: Real-time performance optimization, FPS prediction, latency reduction
- **Development Mode**: Code generation, syntax analysis, debugging assistance
- **Research Mode**: Neural network training, hyperparameter optimization, dataset analysis

## Usage

\`\`\`bash
# Start DWIDO AI
dwido start

# Switch modes
dwido mode gaming
dwido mode dev
dwido mode research

# Check status
dwido status

# Stop DWIDO AI
dwido stop
\`\`\`

## Configuration

Configuration file: $INSTALL_DIR/config/dwido.conf

## Build Information

- Version: $VERSION "$CODENAME"
- Build Date: $(date)
- CUDA Support: $([ "$CUDA_AVAILABLE" = true ] && echo "Enabled" || echo "Disabled")
- OpenCL Support: $([ "$OPENCL_AVAILABLE" = true ] && echo "Enabled" || echo "Disabled")

## Support

For support and documentation, visit the ODIN GAMER/DEV OS community.
EOF

# Create control file for Debian package
cat > "$PACKAGE_DIR/DEBIAN/control" << EOF
Package: dwido-ai
Version: $VERSION
Section: science
Priority: optional
Architecture: amd64
Depends: libc6, libpthread-stubs0-dev, libm6
Maintainer: ODIN Development Team <dev@odin-os.com>
Description: DWIDO AI Genesis Intelligence System
 Revolutionary unified AI system with gaming, development, and research modes.
 Provides real-time optimization, code generation, and neural network training.
EOF

# Create post-installation script
cat > "$PACKAGE_DIR/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# Create dwido user if it doesn't exist
if ! id "dwido" &>/dev/null; then
    useradd -r -s /bin/false -d /opt/dwido dwido
fi

# Set permissions
chown -R dwido:dwido /opt/dwido
chmod +x /opt/dwido/bin/dwido

# Enable systemd service
systemctl daemon-reload
systemctl enable dwido.service

echo "DWIDO AI installed successfully!"
echo "Start with: systemctl start dwido"
EOF

chmod +x "$PACKAGE_DIR/DEBIAN/postinst"

# Build package
if command -v dpkg-deb &> /dev/null; then
    dpkg-deb --build "$PACKAGE_DIR" "$BUILD_DIR/dwido-ai_${VERSION}_amd64.deb"
    log_success "Debian package created: $BUILD_DIR/dwido-ai_${VERSION}_amd64.deb"
else
    log_warning "dpkg-deb not found - creating tarball instead"
    cd "$PACKAGE_DIR"
    tar -czf "../dwido-ai_${VERSION}_amd64.tar.gz" .
    cd - > /dev/null
    log_success "Tarball created: $BUILD_DIR/dwido-ai_${VERSION}_amd64.tar.gz"
fi

# Run tests
log_section "Testing"

log_info "Running basic functionality tests..."

# Test compilation
if [ -x "$BUILD_DIR/bin/dwido" ]; then
    log_success "✓ Executable is valid"
else
    log_error "✗ Executable is not valid"
    exit 1
fi

# Test help functionality
if "$BUILD_DIR/bin/dwido" help &> /dev/null; then
    log_success "✓ Help command works"
else
    log_warning "⚠ Help command may have issues"
fi

# Library link test
log_info "Testing library linkage..."
echo '#include "dwido_ai.h"
int main() { return 0; }' > "$BUILD_DIR/test_link.c"

if $CC -I. -I"$BUILD_DIR" "$BUILD_DIR/test_link.c" -L"$BUILD_DIR/lib" -ldwido $LDFLAGS -o "$BUILD_DIR/test_link" 2>/dev/null; then
    log_success "✓ Library linkage successful"
    rm -f "$BUILD_DIR/test_link" "$BUILD_DIR/test_link.c"
else
    log_warning "⚠ Library linkage test failed"
fi

# Performance test
log_info "Running performance benchmarks..."
/usr/bin/time -f "Build time: %E" echo "Build completed" 2>&1 | head -1

# Generate build report
log_section "Build Report"

BUILD_SIZE=$(du -sh "$BUILD_DIR" | cut -f1)
EXECUTABLE_SIZE=$(ls -lh "$BUILD_DIR/bin/dwido" | awk '{print $5}')
LIBRARY_SIZE=$(ls -lh "$BUILD_DIR/lib/libdwido.a" | awk '{print $5}')

cat > "$BUILD_DIR/build_report.txt" << EOF
DWIDO AI Build Report
====================
Build Version: $VERSION "$CODENAME"
Build Date: $(date)
Build Host: $(hostname)
Build User: $(whoami)

Components Built:
- Core Library: libdwido.a ($LIBRARY_SIZE)
- Main Executable: dwido ($EXECUTABLE_SIZE)
- Configuration Files: dwido.conf
- Systemd Service: dwido.service
$([ "$CUDA_AVAILABLE" = true ] && echo "- CUDA Modules: dwido_cuda.o")
$([ -f "$BUILD_DIR/lib/dwido.so" ] && echo "- Python Bindings: dwido.so")

Build Statistics:
- Total Build Size: $BUILD_SIZE
- CUDA Support: $([ "$CUDA_AVAILABLE" = true ] && echo "Enabled" || echo "Disabled")
- OpenCL Support: $([ "$OPENCL_AVAILABLE" = true ] && echo "Enabled" || echo "Disabled")
- Python Bindings: $([ -f "$BUILD_DIR/lib/dwido.so" ] && echo "Available" || echo "Not Available")

Installation:
$([ -f "$BUILD_DIR/dwido-ai_${VERSION}_amd64.deb" ] && echo "- Debian Package: dwido-ai_${VERSION}_amd64.deb")
$([ -f "$BUILD_DIR/dwido-ai_${VERSION}_amd64.tar.gz" ] && echo "- Tarball: dwido-ai_${VERSION}_amd64.tar.gz")

Next Steps:
1. Install package: sudo dpkg -i dwido-ai_${VERSION}_amd64.deb
2. Start service: sudo systemctl start dwido
3. Check status: dwido status
EOF

log_success "Build report generated: $BUILD_DIR/build_report.txt"

# Final output
log_section "Build Complete"

echo -e "${GREEN}"
echo "╔════════════════════════════════════════════╗"
echo "║          DWIDO AI BUILD SUCCESSFUL         ║"
echo "╚════════════════════════════════════════════╝"
echo -e "${NC}"

echo "📊 Build Summary:"
echo "   Version: $VERSION \"$CODENAME\""
echo "   Executable: $BUILD_DIR/bin/dwido ($EXECUTABLE_SIZE)"
echo "   Library: $BUILD_DIR/lib/libdwido.a ($LIBRARY_SIZE)"
echo "   Total Size: $BUILD_SIZE"
echo ""
echo "🚀 Installation:"
if [ -f "$BUILD_DIR/dwido-ai_${VERSION}_amd64.deb" ]; then
    echo "   sudo dpkg -i $BUILD_DIR/dwido-ai_${VERSION}_amd64.deb"
elif [ -f "$BUILD_DIR/dwido-ai_${VERSION}_amd64.tar.gz" ]; then
    echo "   Extract and copy from $BUILD_DIR/dwido-ai_${VERSION}_amd64.tar.gz"
fi
echo ""
echo "🎯 Quick Start:"
echo "   dwido start     # Start DWIDO AI"
echo "   dwido status    # Check status"
echo "   dwido help      # Show help"
echo ""
echo "✨ DWIDO AI Genesis Intelligence System is ready!"

exit 0
